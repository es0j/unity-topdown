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
        
        


game_state = GameState()