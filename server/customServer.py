from gamelib import *
from zombies import *
from random import sample
class Game_server (Base_server):
    def __init__(self):
        self.max_enemies = 600
        self.requiredPlayers=2
        
        super().__init__(1/10)
        
        
        
    def start(self):
        super().start()
        
        self.AddTasks(Task(self.update_enemyAI))
        self.AddTasks(Task(self.task_spawn_monster))
        #self.spawn_Monster()
        #NPC(next(self.id_counter),OPERATOR,Vector2(0,0))
        
    def update(self):
        super().update()
        
    def task_spawn_monster(self):
        while 1:
            toSpawn = min(10,self.max_enemies-len(game_state.enemies))
            #print(f"spawning {toSpawn} monsters ")
            for i in range(toSpawn):
                sp = sample(game_state.spawners,1)[0]
                zombieA(next(self.id_counter),sp)
            yield 5
    
    #implements example of courotine for a task      
    def update_enemyAI(self):
        while 1:
            print("updating enemy AI")
            for e in game_state.enemies.values():
                e.update_AI()
            yield 0.2
    
            
if __name__=="__main__":
    Game_server()