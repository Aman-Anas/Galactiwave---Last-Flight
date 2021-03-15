from mathutils import Vector
def updateVal (cont):
    own = cont.owner
    w = cont.sensors["W"]
    s = cont.sensors["S"]
    d = cont.sensors["D"]
    a = cont.sensors["A"]
    t = cont.sensors["T"]
    f = cont.sensors["F"]
    
    
    
    
    
    
    player = cont.sensors["playerCol"]
    hitTerminal = cont.sensors["hitTerminal"]
    
    
    
    floor = cont.sensors["floorRay"]
    touchFloor = cont.sensors["touchFloor"]
    
    
    if (player.positive) and (t.positive):
        if own["player_mode"] == "ACTIVE":
            own["player_mode"] = "FINDTERMINAL"
            
        elif own["player_mode"] == "FINDTERMINAL":
            own["player_mode"] = "ACTIVE"
    
    if (player.positive) and (f.positive):
        if own["player_mode"] == "ACTIVE":
            if own["follow"] == False:
                own["follow"] = True
            else:
                own["follow"] = False
            
    if (own["player_mode"] == "ACTIVE"):
        own["autoBump"] = True
        
        for obj in own.scene.objects:
            if "onlyPlayer" in obj:
                vec = own.getVectTo(obj)
                #own.localLinearVelocity.x = 0
                #own.localLinearVelocity.y = 0
                #own.localLinearVelocity.z = 0
                #own.localAngularVelocity.x = 0
                #own.localAngularVelocity.y = 0
                #own.localAngularVelocity.z = 0
                #if floor.positive:
                   # own.worldOrientation.col[2] *= floor.hitObject.worldOrientation.col[2]
                
                #own.alignAxisToVect((vec[1]), 1, 1.0)
                #print(rotDif.x)
                
                #own.localAngularVelocity.x = 0
                #own.localAngularVelocity.z = 0
        if own["follow"] == True:
            if ((player.positive) == False):
                rotDif = Vector(vec[1].rotation_difference(own.worldOrientation.col[1]).to_euler())
                own.worldAngularVelocity = (own.worldAngularVelocity -rotDif)*0.8
                own.applyMovement((0,0.01*vec[0],0),True)
                own["distTo"] = vec[0]
                #if (vec[0] > 0.4):
                 #   own["wasdPressed"] = True
            
    elif (own["player_mode"] == "FINDTERMINAL"):
        own["autoBump"] = False
        closest = 999999
        closeObj = own
        for obj in own.scene.objects:
            if "terminalTar" in obj:
                vec = own.getVectTo(obj)
                #print(vec[0])
                if (vec[0] < closest):
                    closest = vec[0]
                    closeObj = obj
                own["distTo"] = vec[0]
        #print(closeObj)
        own.worldOrientation = closeObj.worldOrientation            
        if ((hitTerminal.positive) == False):       
            if (closeObj != own):
                #own.alignAxisToVect((own.getVectTo(closeObj)[1]), 1, 0.5)
                own.worldPosition = closeObj.worldPosition
                
                #own.applyMovement((0,0.02*own.getVectTo(closeObj)[0],0),True)           
    else:            
        own["autoBump"] = False
        
    
   
    
    #self-correct position to stay out of the way of things
    if (own["moveActive"] == True): 
        #Only enable auto-correction if this is true, controlled by state
        if (own["autoBump"] == True):
            if w.positive:
                own.applyMovement((0,own["maxSpeed"],0),True)
                
            if s.positive:
                own.applyMovement((0,-own["maxSpeed"],0),True)
              
            if d.positive:
                own.applyMovement((own["maxSpeed"],0,0),True)
            
            if a.positive:
                own.applyMovement((-own["maxSpeed"],0,0),True)
            
    jumpTime = 0.2
    jumpForce = 0.7
    jumpIncrement = 0.1
    
    
    if w.positive or s.positive or d.positive or a.positive:
        own["wasdPressed"] = True
    else:
        own["wasdPressed"] = False
    
    space = cont.sensors["Space"]
    if (space.positive and own["jumpTimer"] > 0):
        
        own["jumpTimer"] -= jumpIncrement
        own.localLinearVelocity.z +=jumpForce
    
    if (space.positive == False and own.localLinearVelocity.z > 0):
        own["jumpTimer"] = 0
        own.localLinearVelocity.z = 0 
    
    if (space.positive and (own.localLinearVelocity.z > 0)):
        own["jumping"] = True            
    else:
        
        own["jumping"] = False
       
    
    
    #print(own["jumping"])
    #print(own["jumpTimer"])
    if own["onFloor"] == True:
        own["jumpTimer"] = jumpTime
    
   # if(own.localLinearVelocity.z > 0.1):
   #     own["timeTillStop"] -= 0.1
    #elif own["onFloor"] == True:
   #     own["timeTillStop"] = jumpStop
    
    #if own["timeTillStop"] < 0:
   #     
    #    if (own.localLinearVelocity.z > 0):
    #        own.localLinearVelocity.z += own["timeTillStop"]*20 
    #if (own.localLinearVelocity.z) < -12:
    #    own.localLinearVelocity.z = 0
    #print(own["timeTillStop"])
    #print("jumpTimer"+str(own["jumpTimer"]))
    
    if (space.positive == False) and (touchFloor.positive):
        if (own["onFloor"] == True):
            own.worldLinearVelocity = floor.hitObject.worldLinearVelocity
            
            #ownOrient = own.worldOrientation - floor.hitObject.worldOrientation
            #ownPosDif = own.worldPosition - floor.hitObject.worldPosition
            #ownOrient -= floor.hitObject.worldOrientation .to_euler()
           # ownOrient.y += floor.hitObject.worldAngularVelocity.y
           # ownOrient.z += floor.hitObject.worldAngularVelocity.z
            #if (own.localLinearVelocity.z < 0.1):
                #rotDif = Vector(v1.rotation_difference(v2).to_euler())
           #     own.worldOrientation = floor.hitObject.worldOrientation + ownOrient
           # if (abs(own.localLinearVelocity.y < 0.1)):
           #     own.worldPosition = floor.hitObject.worldPosition + ownPosDif
    if floor.positive == False and own["player_mode"] == "FINDTERMINAL":
        own["player_mode"] = "ACTIVE"    #print(
    
    if floor.positive == False and own["follow"] == True:
        own["follow"] = False
    #if touchFloor.positive:
        #own.worldLinearVelocity = touchFloor.hitObject.worldLinearVelocity 
    #own.localLinearVelocity.x = 0
    #own.localLinearVelocity.y = 0