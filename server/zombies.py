from gamelib import *
import random

class zombieA(Monster):
    def __init__(self, id,vPosition=Vector2(0,0)):
        super().__init__(id,ZOMBIE,vPosition)
        self.speed = random.uniform(1, 2.5)
        self.target=None
        self.vTarget=None
        self.path=[]
        
        
        
        
    def start(self):
        return
    
    def OnCollision(self, other):
        super().OnCollision(other)
        other.TakeDamage(self.damage)
    
    def canSee(self,target):
        t,_ = do_raycast(self.position,target.position,[target],100,game_state.collisionMap)
        return t!=None
    
    def get_visible_player(self):
        t = None
        for p in game_state.get_clients():
            if(self.canSee(p)):
                t = p
                break
        return t
        
    def update_AI(self):
        self.vTarget=None
        #do i have a target?
        if (self.target!=None):
            
            #am i close enough?
            distance = (self.target.position - self.position).length()
            if(distance < 0.1):
                self.path=[]
                self.vTarget=None
                return
            
            #can i see my current target?
            if(self.canSee(self.target)):
                self.vTarget=self.target.position
                return
                
        #can i see any other target?
        if self.get_visible_player()!=None:
            self.target = self.get_visible_player()
            self.vTarget = self.target.position
            return
            
        #do i have a path?
        if len(self.path)==0:
            self.target = self.get_closest_client()
            if(self.target!=None):
                self.path = SolvePathFinding(game_state.map,self.position,
                                             self.target.position,game_state.mapMultiplier)
                return
            
            
    def update(self,dtime=0):
        
        if(self.vTarget!=None):
            self.moveTo(self.vTarget,dtime)
           
        #follow a path
        elif (len(self.path) > 0):
            #move to next step
            if position2tile(self.position)==self.path[0]:
                self.path.pop(0)
            if (len(self.path) > 0 and self.target!=None):
                self.moveTo(self.path[0],dtime)
            
        Entity.sync_send_to_all(self.getInfoUpdatePacket())
        