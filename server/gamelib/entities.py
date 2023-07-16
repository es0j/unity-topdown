import random



from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field

from typing import Literal, Union

from .packets import *
from .libmath import *
from .states import game_state

ZOMBIE = 1
OPERATOR = 0

#base class for every object present on server memory. All server-side are syncronous
class GameObject:
    def __init__(self) -> None:
        self.position = Vector2(0,0)
        game_state.gameObjects.append(self)
        self.radius = 1.2
        
    def checkCollision(self, pos):
        if (self.position - pos).length() < self.radius:
            #print("returned true for pos ",pos)
            return True
        return False
    
    def OnCollision(self,other):
        return
    
    def start(self):
        return
    
    def update(self,dtime=0):
        return

#Base class for every network object
class Entity(GameObject):
    def __init__(self,id,gid,vPosition=Vector2(0,0)):
        super().__init__()
        self.rotation = 0
        self.health = 100
        self.damage = 10
        self.speed = 0.5
        self.id = id
        self.gid = gid
        game_state.entities[self.id] = self
        self.position = vPosition
        
        #tell everyone that you are here and send them your position
        Entity.sync_send_to_all(MsgPlayerEnter(id=self.id,gid=self.gid),ignoreClients=[self])
        Entity.sync_send_to_all(self.getInfoUpdatePacket() ,ignoreClients=[self])
        
        self.start()

    def TakeDamage(self,amount):
        self.health-=amount
        if self.health < 0:
            self.remove()

    def remove(self):
        Entity.sync_send_to_all(MsgPlayerLeave(id=self.id))
        game_state.Destroy(self)
    
    @staticmethod
    def sync_send_to_all(msg,ignoreClients=[]):
        for c in game_state.clients.values():
            if c in ignoreClients:
                continue
            c.sync_send(msg)

    def getInfoUpdatePacket(self):
        return MsgPlayerInfo(id=self.id, x=self.position.x, y=self.position.y,rotation=self.rotation)
    
    def getStatUpdatePacket(self):
        return MsgPlayerStats(id=self.id, health=self.health)
    
    def moveTo(self,target : Vector2, dtime):
        direction = target - self.position
        if direction==Vector2(0,0):
            return
        maxDirection = direction.normalize() * self.speed *dtime
        if (direction.length() < maxDirection.length()):
            self.position = target
        else:
            self.position = self.position + maxDirection

    def get_closest_entity(self,entityList):
        entityListCopy = entityList[::]
        if self in entityListCopy:
            entityListCopy.remove(self)
        
        distances = [ i.position.length() for i in entityListCopy]
        if len(distances) >0:
            mindis = min(distances)
            return list(entityListCopy)[distances.index(mindis)] 
        return None
    
#base class for enemy AI
class Monster(Entity):
    def __init__(self,id,gid,vPosition):
        super().__init__(id,gid,vPosition)
        game_state.enemies[self.id]=self       
    
    def get_closest_client(self):
        return self.get_closest_entity(game_state.get_clients())
            

#base class for friendly AI
class NPC(Entity):
    def __init__(self,id,gid,vPosition):
        super().__init__(id,gid,vPosition=vPosition)
        game_state.npcs[self.id]=self
           

    def update(self,dtime=0):
        self.position=Vector2(  self.position.x + random.random() , self.position.y + random.random())
        
        Entity.sync_send_to_all(self.getInfoUpdatePacket())
        Entity.sync_send_to_all(MsgShoot(id=self.id,
                                       start_x=self.position.x,
                                       start_y=self.position.y,
                                       end_x=self.position.x+100,
                                       end_y=self.position.y))

        
