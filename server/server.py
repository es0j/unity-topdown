#!/usr/bin/python3
import asyncio
import socket
import time
import sys
import random

from packets import *
from entities import *
from client import *

from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field
from vec import Vector2
from typing import Literal, Union

from states import game_state





def inf_counter(start):
    i = start
    while True:
        yield i
        i += 1


class server_class():
    def __init__(self):
        self.id_counter = inf_counter(1)

        self.listen_adress = "127.0.0.1"
        self.port = 9090
        asyncio.run(self.main())


    async def server_mainloop(self):
        await self.spawnMonster()
        await self.spawnNPCS()
        while 1:

            for e in game_state.entities.values():
                e.update()
            for p in game_state.packetsQueue:
                await self.send_to_all(p)
            game_state.packetsQueue.clear()
            #game_state.print()
            await asyncio.sleep(4)
            
            

            

            
    async def spawnNPCS(self):
        npc = NPC(next(self.id_counter))
        await npc.init()

    async def spawnMonster(self):
        monster = Monster(next(self.id_counter))
        await monster.init()

    async def send_to_all(self, msg,ignore=[]):
        for client in game_state.clients.values():
            await client.send_json(msg.json())

    async def main(self):
        await asyncio.gather(self.server_mainloop(),self.start_server())

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.listen_adress, self.port)

        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs} port {self.port}")

        async with server:
            await server.serve_forever()
    
        self.server_mainloop()

    async def handle_client(self,reader, writer):
        try:
            data = await reader.readline()
            print("data: ",data)
            hello = MsgClientHello.parse_raw(data, content_type="application/json")


            client = Client(reader, writer,next(self.id_counter),0)
            await client.init()
            #clients[client.id] = client
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


server_class()