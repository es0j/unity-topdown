
from pygame.math import Vector2
import math

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def position2tile(pos : Vector2):
    x, y = pos.x,pos.y
    if x < 0:
        x -= 1
    if y < 0:
        y -= 1
    return Vector2(int(x), int(y))


def SolvePathFinding(matrix,vstart : Vector2, vend : Vector2):
    
    
    grid = Grid(matrix=matrix)
    last_matrix_index = len(matrix)-1


    start = grid.node(int(vstart.x), int(vstart.y))
    end = grid.node(int(vend.x), int(vend.y))


    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    #print('operations:', runs, 'path length:', len(path))
    #print(grid.grid_str(path=path, start=start, end=end))
    #print(path)
    
    return [Vector2(i[0],i[1]) for i in path]+[vend]




#based on https://github.com/OneLoneCoder/Javidx9/blob/master/PixelGameEngine/SmallerProjects/OneLoneCoder_PGE_RayCastDDA.cpp
#Do a DDA raycast
def do_raycast(vPlayer :Vector2 ,vTarget : Vector2,gameObjectList : list,fMaxDistance : float,tilemap : list):

    vRayStart = vPlayer
    vRayDir = (vTarget - vPlayer).normalize()

    #avoid 0 division, small number, small error
    if (vRayDir.x==0):
        vRayDir.x = 0.0001
    if (vRayDir.y==0):
        vRayDir.y = 0.0001
        
    vRayUnitStepSize = Vector2(math.sqrt(1+(vRayDir.y/vRayDir.x)**2), math.sqrt(1+(vRayDir.x/vRayDir.y)**2))
    
    vMapCheck = Vector2(int(vRayStart.x), int(vRayStart.y))
    vRayLength1D = Vector2(0.0, 0.0)
    vStep = Vector2(0, 0)
    
    

    #set up initial conditions 
    if (vRayDir.x < 0):
        vStep.x = -1
        vRayLength1D.x = (vRayStart.x - vMapCheck.x) * vRayUnitStepSize.x
    else:
        vStep.x = 1
        vRayLength1D.x = ((vMapCheck.x + 1) -vRayStart.x) * vRayUnitStepSize.x

    if (vRayDir.y < 0):
        vStep.y = -1
        vRayLength1D.y = (vRayStart.y - vMapCheck.y) * vRayUnitStepSize.y
    else:
        vStep.y = 1
        vRayLength1D.y = ((vMapCheck.y + 1) - vRayStart.y) * vRayUnitStepSize.y

    fDistance = 0.0
    while (fDistance < fMaxDistance):
        # Walk along shortest path
        if (vRayLength1D.x < vRayLength1D.y):
            vMapCheck.x += vStep.x
            fDistance = vRayLength1D.x
            vRayLength1D.x += vRayUnitStepSize.x
        else:
            vMapCheck.y += vStep.y
            fDistance = vRayLength1D.y
            vRayLength1D.y += vRayUnitStepSize.y


        #vMapCheck.x
        checkedPoint = vRayStart + vRayDir * fDistance
        
        if (tilemap[int(vMapCheck.y)][int(vMapCheck.x)]==0):
            return None,checkedPoint
        
        for e in gameObjectList:
             #check if element is present on list
            if (e.checkCollision(checkedPoint)):
                # Calculate intersection location and return the gameObject collided with
                return  e,checkedPoint
            
    return None,Vector2(0,0)



