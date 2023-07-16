import json
import time
from .libmath import Vector2

class GameState:
    def __init__(self) -> None:
        #only players
        self.clients = {}

        #eneryEntity
        self.entities ={}

        #only enemies
        self.enemies ={}

        #only NPCs
        self.npcs ={}

        #packets to be sent from server
        self.packetsQueue=[]
        
        self.gameObjects=[]
        
        
        #self.map = self.loadMap("Pathfinding",22,19)
        self.map = self.loadMap("Collision",100,100)
        self.mapMultiplier=4
        self.collisionMap = self.loadMap("Collision",100,100)
        self.spawners = self.loadTiles("Spawner")
        
        self.dtime = 0
        self.lastTime = time.time()
        
    
    def get_clients(self):
        return list(self.clients.values())+list(self.npcs.values())
    
    def updateDtime(self):
        currTime = time.time()
        self.dtime = currTime - self.lastTime
        self.lastTime = currTime
        
    def print(self):
        print("------ game state -------")
        print("clients:",self.clients)
        print("entities:",self.entities)
        print("enemies:",self.enemies)
        print("npcs:",self.npcs)
        print("gameObjects:",self.gameObjects)
        print("packetsQueue:",self.packetsQueue)
        print("------ end of game state -------")
    
    def tryRemoveFromDict(self,dict,gObject):
        for id, val in dict.items():
            if val==gObject:
                del dict[id]
                break         
    def tryRemoveFromList(self,list,gObject):
       if gObject in list:
            list.remove(gObject)
            
    def Destroy(self,gObject):
        self.tryRemoveFromDict(self.clients,gObject)
        self.tryRemoveFromDict(self.entities,gObject)
        self.tryRemoveFromDict(self.enemies,gObject)
        self.tryRemoveFromDict(self.npcs,gObject)
        self.tryRemoveFromList(self.gameObjects,gObject)
        
    def loadTiles(self,key):
        vecList = []
        
        with open(f"maps/gamemap.json") as f:
            data=json.loads(f.read())
        for i in data:
            if i["key"]==key:
                tilemap = i["tiles"]
        for t in tilemap:
            x = t["position"]["x"]
            y = t["position"]["y"]
            vecList.append(Vector2(x,y))
        return vecList
        
    def loadMap(self,key,max_x,max_y):
        
        map = [[1 for x in range(max_x)] for y in range(max_y)] 
        vecList = self.loadTiles(key)
        for v in vecList:
            map[int(v.y)][int(v.x)]=0
        
        #self.print_map()
        return map
        
    def print_map(self):  
        for l in self.map:
            print("".join([str(k) for k in l]))

        
game_state = GameState()