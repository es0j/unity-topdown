from states import game_state

from entities import *
from libmath import do_raycast

class Client(Entity):
    def __init__(self, reader, writer,id,gid):
        Entity.__init__(self,id,gid)
        self.error = False
        self.reader = reader
        self.writer = writer
        game_state.clients[self.id] = self
        
        
    async def init(self):
        await self.send_json(MsgServerHello(name="Server 1.0", id=self.id).json())
        await super().init()

        #replicate every other entity
        for e in game_state.entities.values():
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
            
            #print("message parsed!",message)
            if message.type == MsgType.PlayerInfo:
                await self.handle_player_info(message)
            if message.type == MsgType.Shoot:
                await self.handle_shoot(message)

    async def handle_player_info(self, msg):
        if msg.id != self.id:
            await self.send_error("Wrong player ID")
            return

        self.position = Vector2(msg.x, msg.y)
        self.rotation = msg.rotation
        #print("replicating movement")
        await self.send_to_all(self.getInfoUpdatePacket(),ignoreClients=[self])
        

    async def handle_shoot(self, msg):
        if msg.id != self.id:
            await self.send_error("Wrong player ID")
            return
        await self.send_to_all(MsgShoot(id=self.id),ignoreClients=[self])
        #resolve collision
        do_raycast(self.position, Vector2(self.position.x+100,self.position.y),[],100 )
        
