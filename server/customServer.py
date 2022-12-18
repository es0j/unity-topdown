from gamelib import *
from zombies import *

class gameServer (server_class):
    def __init__(self):
        super().__init__(0.1)
        
        
    def start(self):
        super().start()
        self.AddTasks(Task(self.update_enemyAI))
        self.spawn_Monster()
        #self.spawn_NPC()
        
    def update(self):
        super().update()

    
    def spawn_NPC(self):
        NPC(next(self.id_counter),OPERATOR,Vector2(40,30))
        

    def spawn_Monster(self):
        zombieA(next(self.id_counter),Vector2(40,30))

if __name__=="__main__":
    gameServer()