from gamelib import *

class zombieA(Monster):
    def __init__(self, id,vPosition=Vector2(0,0)):
        super().__init__(id,ZOMBIE,vPosition)
        
    def start(self):
        return
    
    def OnCollision(self, other):
        super().OnCollision(other)
        other.TakeDamage(self.damage)
    
    def update(self,dtime=0):
        #print(f"Pos {self.position} Path: {self.path}")
        if (len(self.path) > 1):
            #move to next step
            if position2tile(self.position)==self.path[1]:
                self.path.pop(1)
            
        if (len(self.path) > 1 and self.target!=None):
            destination = self.path[1]
            if position2tile(self.target.position) == destination:
                destination = self.target.position
            self.moveTo(self.path[1],dtime)
            
        Entity.sync_send_to_all(self.getInfoUpdatePacket())
        