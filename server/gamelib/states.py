import json
import time
from pygame.math import Vector2

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
        
        self.map =[]
        
        self.loadMap("ce8d312982aa23a70bc954397e803050")
        
        self.dtime = 0
        self.lastTime = time.time()
        
        #print(self.map)
    
    def get_clients(self):
        return list(self.clients.values())
    
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
        

    def loadMap(self,mapId):
        
        maxCoord=78
        
        self.map = [[1 for x in range(maxCoord+1)] for y in range(maxCoord+1)] 
        
        with open(f"maps/{mapId}.json") as f:
            data=json.loads(f.read())
        for i in data:
            if i["key"]=="Collision":
                tilemap = i["tiles"]
        for t in tilemap:
            x = t["position"]["x"]
            y = t["position"]["y"]
            
            maxCoord = max(maxCoord,x)
            maxCoord = max(maxCoord,y)
            self.map[int(y)][int(x)]=0
        
    def print_map(self):  
        for l in self.map:
            print("".join([str(k) for k in l]))

        
game_state = GameState()