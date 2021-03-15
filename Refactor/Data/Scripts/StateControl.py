from mathutils import Vector
def updateState (cont):
    own = cont.owner
    scene = own.scene
    floor = cont.sensors["floorRay"]
    
    normalVect = own.getVectTo(floor.hitPosition)
    own["distanceToFloor"] = normalVect[0]
    
    if own["distanceToFloor"] < 2.0:
        own["onFloor"] = True
    else:
        own["onFloor"] = False
    
    
    if (own["player_mode"] == "ACTIVE"):
        own["moveActive"] = True
        if own["onFloor"] == False:
            if own["jumping"] == True:
                    own["player_state"] = "JUMPING"
            else:
                own["player_state"] = "FALLING"
        else:     
            if own["wasdPressed"] == True:
                own["player_state"] = "MOVING"
            else:
                own["player_state"] = "STATIONARY"
    
    if ("follow" in own):
        if ((own["follow"] == True) or (own["player_mode"] == "FINDTERMINAL")):
            if (own.localLinearVelocity.y > 0.1):
                own["player_state"] = "MOVING"
            else:
                own["player_state"] = "STATIONARY"
    
    if own["player_mode"] == "TERMINAL":
        own["player_state"] = "FROZEN"
        own["moveActive"] = False
    
   # if (own["player_state"] == "FROZEN") and (floor.positive):
       # own.worldLinearVelocity = floor.hitObject.worldLinearVelocity
       # own.worldOrientation = floor.hitObject.worldOrientation
    