from .client import *
from .weapon import *

class Player(Client):
    def __init__(self, reader, writer, id):
        super().__init__(reader, writer, id)
        self.inventory = [Weapon(60) , Weapon(), Weapon(),Weapon(),]
        self.currentWeapon = self.inventory[0]
            
    def TakeDamage(self,amount):
        currt=time.time()
        if (currt - self.lastTimeHit < self.iframeTime):
            return
        self.lastTimeHit = currt
        self.health-=amount
        self.sync_send(MsgPlayerStats(id=self.id,health=self.health))
    
    def handle_player_info(self, msg):
        self.position = Vector2(msg.x, msg.y)
        self.rotation = msg.rotation
        #print("replicating movement")
        Entity.sync_send_to_all(self.getInfoUpdatePacket(),ignoreClients=[self])
        

    def handle_shoot(self, msg):
        Entity.sync_send_to_all(msg,ignoreClients=[self])
        self.currentWeapon.shoot(msg)
            
