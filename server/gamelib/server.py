#!/usr/bin/python3
import asyncio
import socket
import time


from .packets import *
from .entities import *
from .player import *
from .states import game_state

from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field
from typing import Literal, Union



import time



def inf_counter(start):
    i = start
    while True:
        yield i
        i += 1

class Task:
    def __init__(self,task):
        self.taskTime=0
        self.task=task
        self.lastTime = 0
        self.isFinished=False
    def try_task(self):
        #print("trying task")
        currentTime = time.time()
        if (currentTime - self.lastTime) > self.taskTime and not self.isFinished :
            self.taskTime = next(self.task())
            if(self.taskTime==-1):
                self.isFinished = True
            self.lastTime = currentTime

class server_class():
    def __init__(self,sleepTime=0.01):
        self.id_counter = inf_counter(1)
        self.lastTime = time.time()
        self.listen_adress = "127.0.0.1"
        self.port = 9090
        self.sleepTime = sleepTime
        self.tasks = []
        asyncio.run(self.main())
        
    def AddTasks(self,t):
        self.tasks.append(t)
        
    def checkCollision(self):
        for c in game_state.get_clients():
            for e in game_state.enemies.values():
                distance = (e.position - c.position).length()
                if distance < (e.radius + c.radius)*0.7:
                    e.OnCollision(c)
                    
    #implements example of courotine for a task      
    def update_enemyAI(self):
        while 1:
            for e in game_state.enemies.values():
                e.target = e.get_closest_client()
                if(e.target!=None):
                    e.path = SolvePathFinding(game_state.map,e.position,e.target.position)
            yield 2
    
    #overwrite to implement game logic  
    def start(self):
        return

    #overwrite to implement game logic
    def update(self):
        #update all entities
        for e in game_state.entities.values():
            e.update(game_state.dtime)
        
        for t in self.tasks:
            t.try_task()
            if t.isFinished:
                self.tasks.remove(t)
            
        self.checkCollision()
            
    
    async def flushPacketQueue(self):
        #send all packets on the list
        for p in game_state.packetsQueue:
            await Entity.send_to_all(p)
        game_state.packetsQueue.clear()
        
        for c in game_state.clients.values():
            await c.writer.drain()

    async def server_loop(self):
        self.start()
        await self.flushPacketQueue()
        
        while 1:
            game_state.updateDtime()
            self.update()
            await self.flushPacketQueue()
            
            #game_state.print()
            await asyncio.sleep(self.sleepTime)
              
    async def main(self):
        await asyncio.gather(self.server_loop(),self.start_server())

    async def start_server(self):
        server = await asyncio.start_server(self.__handle_client, self.listen_adress, self.port)

        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs} port {self.port}")

        async with server:
            await server.serve_forever()
    
        #self.server_mainloop()

    async def __handle_client(self,reader, writer):
        try:
            client_id = next(self.id_counter)
            
            # do this step before creating Client object to ensure first handshake before other packets
            data = await reader.readline()
            hello = MsgClientHello.parse_raw(data, content_type="application/json")
            writer.write((MsgServerHello(name="Server 1.0", id=client_id).json() + "\n").encode())
            await writer.drain()
        
            client = Player(reader, writer,client_id)
            await client.init()
            addr = writer.get_extra_info("peername")
            print(f"{addr!r} connected, got id: {client.id}")
            await client.loop()
            print(f"Closed: {client.id}")
            game_state.Destroy(client)     
                  
        except Exception as e:
            print(e)
            raise e
        finally:
            try:
                await client.remove()
            except Exception as e:
                pass
            game_state.Destroy(client) 
            writer.close()
        
        
if __name__ == "__main__":
    server_class()