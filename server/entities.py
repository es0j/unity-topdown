import asyncio
import socket
import time
import sys
import random

from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field
from vec import Vector2
from typing import Literal, Union

from packets import *

ZOMBIE = 1
PLAYER = 0

#onyl players
clients = {}

#eneryEntity
entities ={}

#only enemies
enemies ={}


def position2tile(pos):
    x, y = pos
    if x < 0:
        x -= 1
    if y < 0:
        y -= 1
    return tuple((int(x), int(y)))


class Entity:
    def __init__(self,id,gid):
        self.position = Vector2(0,0)
        self.health = 100
        self.damage = 10
        self.id = id
        self.gid = gid
        entities[self.id] = self

        
    async def init(self):
        #tell everyone that you are here
        await self.send_to_all(MsgPlayerEnter(id=self.id, x=self.position.x, y=self.position.y,gid=self.gid),ignoreClients=[self])


    async def remove(self):
        await self.send_to_all(MsgPlayerLeave(id=self.id))

    async def send_to_all(self, msg,ignoreClients=[]):
        for c in clients.values():
            if c in ignoreClients:
                continue
            await c.send_json(msg.json())

    async def send_json(self, json):
        print("sent: ",json)
        self.writer.write((json + "\n").encode())
        await self.writer.drain()


class Monster(Entity):
    def __init__(self,id):
        super().__init__(id,ZOMBIE)
        enemies[self.id]=self

    def update(self):
        self.position=Vector2(  self.position.x + random.random() , self.position.y + random.random())
        


class Client(Entity):
    def __init__(self, reader, writer,id,gid):
        Entity.__init__(self,id,gid)
        self.error = False
        self.reader = reader
        self.writer = writer
        clients[self.id] = self


        
    async def init(self):
        await self.send_json(MsgServerHello(name="Server 1.0", id=self.id).json())
        await super().init()

        #replicate every other entity
        for e in entities.values():
            if e == self:
                continue
            await self.send_json(MsgPlayerEnter(id=e.id, x=e.position.x, y=e.position.y,gid=e.gid).json()) 
    

    async def send_error(self, msg, disconnect=True):
        await self.send_json(MsgError(msg=msg).json())
        self.error = disconnect

    async def loop(self):
        while not self.error:
            data = await self.reader.readline()
            print("data recived: ",data)
            if not data:
                break            
            message = Msg.parse_raw(data, content_type="application/json").__root__
            if message.type == MsgType.PlayerInfo:
                await self.handle_player_info(message)
            if message.type == MsgType.Shoot:
                await self.handle_shoot(message)

    async def handle_player_info(self, msg):
        if msg.id != self.id:
            await self.send_error("Wrong player ID")
            return

        self.position = Vector2(msg.x, msg.y)
        #print("replicating movement")
        await self.send_to_all(MsgPlayerInfo(id=self.id, x=msg.x, y=msg.y),ignoreClients=[self])
        

    async def handle_shoot(self, msg):
        if msg.id != self.id:
            await self.send_error("Wrong player ID")
            return
        await self.send_to_all(MsgShoot(id=self.id),ignoreClients=[self])
