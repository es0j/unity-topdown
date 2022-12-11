import asyncio
import socket
import time
import sys
import random

from states import game_state

from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field

from pygame.math import Vector2
from typing import Literal, Union

from packets import *
from libmath import position2tile


ZOMBIE = 1
OPERATOR = 0


class GameObject:
    def __init__(self) -> None:
        self.position = Vector2(0,0)
        game_state.gameObjects.append(self)
        self.radius = 1.2
        
    def checkCollision(self, pos):
        if (self.position - pos).length() < self.radius:
            print("returned true for pos ",pos)
            return True
        return False
        

class Entity(GameObject):
    def __init__(self,id,gid):
        super().__init__()
        self.rotation = 0
        self.health = 100
        self.damage = 10
        self.id = id
        self.gid = gid
        game_state.entities[self.id] = self
        
    async def init(self):
        #tell everyone that you are here and send them your position
        await self.send_to_all(MsgPlayerEnter(id=self.id,gid=self.gid),ignoreClients=[self])
        await self.send_to_all(self.getInfoUpdatePacket() ,ignoreClients=[self])


    async def remove(self):
        await self.send_to_all(MsgPlayerLeave(id=self.id))

    async def send_to_all(self, msg,ignoreClients=[]):
        for c in game_state.clients.values():
            if c in ignoreClients:
                continue
            await c.send_json(msg.json())

    async def send_json(self, json):
        print("sent: ",json)
        self.writer.write((json + "\n").encode())
        await self.writer.drain()
        
    async def send_to_client(self, msg):
        await self.send_json(msg.json())

    def addPacketToQueue(self,p):
        game_state.packetsQueue.append(p)

    def server_send_position(self):
        self.addPacketToQueue(self.getInfoUpdatePacket())

    def getInfoUpdatePacket(self):
        return MsgPlayerInfo(id=self.id, x=self.position.x, y=self.position.y,rotation=self.rotation)
    
    def getStatUpdatePacket(self):
        return MsgPlayerStats(id=self.id, health=self.health)
    
    def update(self):
        return

class Monster(Entity):
    def __init__(self,id):
        super().__init__(id,ZOMBIE)
        game_state.enemies[self.id]=self        
        
    def update(self):
        self.position=Vector2(  self.position.x + random.random() , self.position.y + random.random())
        self.server_send_position()
        
    

class NPC(Entity):
    def __init__(self,id):
        super().__init__(id,OPERATOR)
        game_state.npcs[self.id]=self
           

    def update(self):
        self.position=Vector2(  self.position.x + random.random() , self.position.y + random.random())
        self.server_send_position()
        self.addPacketToQueue(MsgShoot(id=self.id,
                                       start_x=self.position.x,
                                       start_y=self.position.y,
                                       end_x=self.position.x+100,
                                       end_y=self.position.y))

        
