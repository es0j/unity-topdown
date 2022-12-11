#!/usr/bin/python3
import asyncio
import socket
import time


from .packets import *
from .entities import *
from .client import *
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


class server_class():
    def __init__(self,sleepTime=0.01):
        self.id_counter = inf_counter(1)
        self.lastTime = time.time()
        self.listen_adress = "127.0.0.1"
        self.port = 9090
        self.sleepTime = sleepTime
        self.permanentTasks = []
        asyncio.run(self.main())
      
    #overwrite to implement game logic  
    async def start(self):
        return

    #overwrite to implement game logic
    async def update(self):
        #update all entities
        for e in game_state.entities.values():
            e.update(game_state.dtime)
            
        #send all packets on the list
        for p in game_state.packetsQueue:
            await self.send_to_all(p)
        game_state.packetsQueue.clear()

    async def update_tasks(self):
        return
    
    async def task_mainloop(self):
        while 1:
            await self.update_tasks()
            await asyncio.sleep(5)
            
    async def update_mainloop(self):
        #await self.spawnMonster()
        #await self.spawnNPCS()
        await self.start()
        
        while 1:
            game_state.updateDtime()
            
            await self.update()
            
            #game_state.print()
            await asyncio.sleep(self.sleepTime)
              
    async def send_to_all(self, msg,ignore=[]):
        for client in game_state.clients.values():
            await client.send_json(msg.json())

    async def main(self):
        await asyncio.gather(self.update_mainloop(),self.task_mainloop(),self.start_server())

    async def start_server(self):
        server = await asyncio.start_server(self.__handle_client, self.listen_adress, self.port)

        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs} port {self.port}")

        async with server:
            await server.serve_forever()
    
        self.server_mainloop()

    async def __handle_client(self,reader, writer):
        try:
            data = await reader.readline()
            #print("data: ",data)
            hello = MsgClientHello.parse_raw(data, content_type="application/json")


            client = Client(reader, writer,next(self.id_counter),0)
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

    async def spawnEntity(self, entity_class, vPosition=Vector2(0,0)):
        entity = entity_class(next(self.id_counter))
        await entity.init(vPosition)
        
if __name__ == "__main__":
    server_class()