from .states import game_state
from .libmath import Vector2
from .libmath import do_raycast

class Weapon:
    def __init__(self,damage=10):
        self.damage=damage
        self.ammo=100
        self.cooldown=0
        
    def shoot(self,msg):
        collidersGO = game_state.enemies.values()
        startPos = Vector2(msg.start_x,msg.start_y)
        endPos = Vector2(msg.end_x,msg.end_y)
        
        #print(f"handle collision {startPos} -> {endPos}",[e.position for e in collidersGO])
        
        collided,position= do_raycast(startPos, endPos,collidersGO,100,game_state.collisionMap)
        #print(collided,position)
        if collided!=None:
            self.shoot_enemy(collided)
            
    def shoot_enemy(self,target):
        print("Shooting enemy",self.damage)
        target.TakeDamage(self.damage)
        
        