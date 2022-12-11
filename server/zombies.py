from gamelib import *

class zombieA(Monster):
    def __init__(self, id,gid=1):
        super().__init__(id)
        
    def start(self):
        return
    
    def update(self,dtime=0):
        #print(f"Pos {self.position} Path: {self.path}")
        if (len(self.path) > 1):
            #move to next step
            if position2tile(self.position)==self.path[1]:
                self.path.pop(1)
            
        if (len(self.path) > 1):
            destination = self.path[1]
            if position2tile(self.target.position) == destination:
                destination = self.target.position
            self.moveTo(self.path[1],dtime)
            
        self.server_send_position()