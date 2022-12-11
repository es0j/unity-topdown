import pygame
import sys
import math
#from vec import Vector2
from pygame.math import Vector2

pygame.init()

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = ((SCREEN_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS


player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi


MAP = (
     '########'
     '#   ## #'
     '#      #'
     '#    ###'
     '##     #'
     '#   #  #'
     '#   #  #'
     '########'
)


win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Raycasting by Network Skeleton")

clock = pygame.time.Clock()

def position2tile(pos):
    x, y = pos
    if x < 0:
        x -= 1
    if y < 0:
        y -= 1
    return tuple((int(x), int(y)))


def draw_map():
    for row in range(8):
        for col in range(8):
            square = row * MAP_SIZE + col

            pygame.draw.rect(
                win,
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)

                )
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (player_x -
                     math.sin(player_angle) * 50, player_y + math.cos(player_angle) * 50), 3)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (player_x - math.sin(
        player_angle - HALF_FOV) * 50, player_y + math.cos(player_angle - HALF_FOV) * 50), 3)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (player_x - math.sin(
        player_angle + HALF_FOV) * 50, player_y + math.cos(player_angle + HALF_FOV) * 50), 3)


def cast_rays(vPlayer,vMouseCell,map):

        vRayStart = vPlayer
        vRayDir = (vMouseCell - vPlayer).normalize()
        
        print("vRayStart ",vRayStart)
        print("vMouseCell ",vMouseCell)

        vRayUnitStepSize = Vector2(math.sqrt(1+(vRayDir.y/vRayDir.x)**2), math.sqrt(1+(vRayDir.x/vRayDir.y)**2))
        
        vMapCheck = Vector2(int(vRayStart.x), int(vRayStart.y))
        vRayLength1D = Vector2(0.0, 0.0)
        vStep = Vector2(0, 0)

        if (vRayDir.x < 0):
            vStep.x = -1
            vRayLength1D.x = (vRayStart.x - vMapCheck.x) * vRayUnitStepSize.x
        else:
            vStep.x = 1
            vRayLength1D.x = ((vMapCheck.x + 1) -
                              vRayStart.x) * vRayUnitStepSize.x

        if (vRayDir.y < 0):
            vStep.y = -1
            vRayLength1D.y = (vRayStart.y - vMapCheck.y) * vRayUnitStepSize.y
        else:
            vStep.y = 1
            vRayLength1D.y = ((vMapCheck.y + 1) - vRayStart.y) * vRayUnitStepSize.y

        bTileFound = False
        fMaxDistance = 100.0
        fDistance = 0.0
        while (not bTileFound and (fDistance < fMaxDistance)):
            # Walk along shortest path
            if (vRayLength1D.x < vRayLength1D.y):
                vMapCheck.x += vStep.x
                fDistance = vRayLength1D.x
                vRayLength1D.x += vRayUnitStepSize.x
            else:
                vMapCheck.y += vStep.y
                fDistance = vRayLength1D.y
                vRayLength1D.y += vRayUnitStepSize.y

            idx = int(vMapCheck.y * MAP_SIZE + vMapCheck.x)
            #print("checking ",vMapCheck)
            
            if(idx < len(map)):
                
                if (map[idx] == "#"):
                    bTileFound = True
                    print("point found",vMapCheck.x,vMapCheck.y,idx)
                    pygame.draw.rect(win,(0,0,255),(vMapCheck.x * TILE_SIZE,
                                            vMapCheck.y * TILE_SIZE,
                                            20,
                                            20))
                    
                pygame.draw.rect(win,(255,0,0),(vMapCheck.x * TILE_SIZE,
                                            vMapCheck.y * TILE_SIZE,
                                            15,
                                            15))
                    
            
        
            
        
        # Calculate intersection location
        vIntersection = Vector2(0,0)
        if (bTileFound):
            vIntersection = vRayStart + vRayDir * fDistance
            pygame.draw.rect(win,(0,255,0),(vIntersection.x * TILE_SIZE,
                                            vIntersection.y * TILE_SIZE,
                                            10,
                                            10))
            

forward = True


while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit(0)
          
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col
    (player_y / TILE_SIZE) * MAP_SIZE + player_x / TILE_SIZE 
    if MAP[square] == '#':
            if forward == True:
                player_x -= -math.sin(player_angle) * 5
                player_y -= math.cos(player_angle) * 5
            else:
                player_x += -math.sin(player_angle) * 5
                player_y += math.cos(player_angle) * 5

     
          
    pygame.draw.rect(win,(0,0,0),(0,0,SCREEN_HEIGHT,SCREEN_HEIGHT))
    
    pygame.draw.rect(win,(100,0,0),(480,SCREEN_HEIGHT / 2,SCREEN_HEIGHT,SCREEN_HEIGHT))
    pygame.draw.rect(win,(200,0,0),(480,-SCREEN_HEIGHT / 2,SCREEN_HEIGHT,SCREEN_HEIGHT))      
    
    
    draw_map()
    
    start_angle = player_angle - HALF_FOV
    depth = 40
    vPlayer = Vector2(player_x/ TILE_SIZE, player_y/ TILE_SIZE)
    vMouseCell = Vector2(vPlayer.x - math.sin(start_angle)
                            * depth, vPlayer.y + math.cos(start_angle) * depth)
    
    pygame.draw.line(win, (255,255,0),(player_x,player_y),(vMouseCell.x * TILE_SIZE,vMouseCell.y * TILE_SIZE))
    cast_rays(vPlayer,vMouseCell,MAP)
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5
    
    clock.tick(30)    
    
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255,255,255))
    win.blit(textsurface,(0,0))
    pygame.display.flip()