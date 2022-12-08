#!/usr/bin/python3
import asyncio
import socket
import time
import sys
import random

from packets import *
from entities import *

from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field
from vec import Vector2
from typing import Literal, Union







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
        while 1:

            #print("running game logic")
            #print(clients)
            await asyncio.sleep(4)
            #await self.spawnMonster()
            
            for m in enemies.values():
                m.update()
                await self.send_to_all(MsgPlayerInfo(id=m.id, x=m.position.x, y=m.position.y))

            

            


    async def spawnMonster(self):
        monster = Monster(next(self.id_counter))
        await monster.init()

    async def send_to_all(self, msg,ignore=[]):
        for client in clients.values():
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
            
  
        except Exception as e:
            print(e)
            raise e
        finally:
            try:
                await client.remove()
            except Exception as e:
                pass
            del clients[client.id]
            del entities[client.id]
            writer.close()


server_class()