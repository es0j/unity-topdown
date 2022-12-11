
from pygame.math import Vector2
import math
import sys





def position2tile(pos : Vector2):
    x, y = pos.x,pos.y
    if x < 0:
        x -= 1
    if y < 0:
        y -= 1
    return tuple((int(x), int(y)))

#based on https://github.com/OneLoneCoder/Javidx9/blob/master/PixelGameEngine/SmallerProjects/OneLoneCoder_PGE_RayCastDDA.cpp
#Do a DDA raycast
def do_raycast(vPlayer :Vector2 ,vTarget : Vector2,gameObjectList : list,fMaxDistance : float):

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

        checkedPoint = vRayStart + vRayDir * fDistance
        
        for e in gameObjectList:
             #check if element is present on list
            if (e.checkCollision(checkedPoint)):
                # Calculate intersection location and return the gameObject collided with
                return  e,checkedPoint
            
    return None,Vector2(0,0)



if __name__=="__main__":
    
    g1 = GameObject()
    print(type(g1.position))
    g1.position.x=50
    g1.position.y=0.2
    print(do_raycast(
        Vector2(0,0),
        Vector2(100,0.1),
        [g1],100
    ))