from .states import game_state

from .entities import *
from .libmath import do_raycast
import time 

#Base class for conected player
class Client(Entity):
    def __init__(self, reader, writer,id):
        Entity.__init__(self,id,OPERATOR)
        self.error = False
        self.reader = reader
        self.writer = writer
        game_state.clients[self.id] = self
        self.iframeTime = 0.5
        self.lastTimeHit = 0
        
    async def send(self, json):
        self.sync_send(json)
        await self.writer.drain()
    
    @staticmethod
    async def send_to_all(msg,ignoreClients=[]):
        Entity.sync_send_to_all(msg,ignoreClients)
        for c in game_state.clients.values():
            await c.writer.drain()
        
        
    def sync_send(self, json):
        self.writer.write((json.json() + "\n").encode())
       
        
    async def init(self):
        #replicate every other entity
        for e in game_state.entities.values():
            if e == self:
                continue
            await self.send(MsgPlayerEnter(id=e.id,gid=e.gid)) 
            await self.send(e.getInfoUpdatePacket()) 
        await self.send(self.getStatUpdatePacket()) 

    def parsePacket(self,message):
        if message.type == MsgType.PlayerInfo:
            self.handle_player_info(message)
        if message.type == MsgType.Shoot:
            self.handle_shoot(message)
        if message.type == MsgType.PlayerWeapon:
            self.handle_player_weapon(message)
    
    def send_error(self, msg, disconnect=True):
        self.sync_send(MsgError(msg=msg))
        self.error = disconnect
    
    async def loop(self):
        
        try:
            while not self.error:
                data = await self.reader.readline()
                if not data:
                    break                  
                
            
                #print("data recived: ",data)
            
                message = Msg.parse_raw(data, content_type="application/json").root
                
                self.parsePacket(message)
                
                await self.writer.drain()
                
        except ConnectionResetError:
                print("[Client Disconected]")


            