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

        #packets to be sent to server
        self.packetsQueue=[]
        
        self.gameObjects=[]
        
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
        

game_state = GameState()