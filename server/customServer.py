from gamelib import *
from zombies import *

class gameServer (server_class):
    def __init__(self):
        super().__init__(1)
        
    async def start(self):
        await super().start()
        await self.spawnMonster()
        await self.spawnNPCS()
        
    async def update(self):
        return await super().update()
        
    async def update_tasks(self):
        await super().update_tasks()
        
        for e in game_state.enemies.values():
            e.target = e.getClosestClient()
            if(e.target!=None):
                e.path = SolvePathFinding(game_state.map,e.position,e.target.position)
    
    async def spawnNPCS(self):
        await self.spawnEntity (NPC,Vector2(40,30))


    async def spawnMonster(self):
        await self.spawnEntity (zombieA,Vector2(40,30))

if __name__=="__main__":
    gameServer()