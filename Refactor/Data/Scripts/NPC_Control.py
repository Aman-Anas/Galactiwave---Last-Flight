from mathutils import Vector
def updateVal (cont):
    own = cont.owner
    w = cont.sensors["W"]
    s = cont.sensors["S"]
    d = cont.sensors["D"]
    a = cont.sensors["A"]
    t = cont.sensors["T"]
    f = cont.sensors["F"]
    
    
    
    
    for obj in own.scene.objects:
        if "onlyPlayer" in obj:
            onlyPlayer = obj
            if onlyPlayer["player_mode"] == "TERMINAL":
                 own["follow"] = False
    player = cont.sensors["playerCol"]
    hitTerminal = cont.sensors["hitTerminal"]
    
    if (own["lastTerminal"] == 0):
        own["lastTerminal"] = own
    
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
        own.restoreDynamics()
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
        terminal = closeObj.parent
        if terminal != None:
            #own.worldAngularVelocity = terminal.worldAngularVelocity    
            for object in terminal.children:
                if "align" in object:
                    #print(terminal.children)
                    
                    object.children[0]["AI_enabled"] = False
                    own["lastTerminal"] = object
        
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
        if (own["follow"] == True):
            own.removeParent()
            own.restoreDynamics()
            if ((player.positive) == False):
                rotDif = Vector(vec[1].rotation_difference(own.worldOrientation.col[1]).to_euler())
                own.worldAngularVelocity = (own.worldAngularVelocity -rotDif)*0.8
                own.applyMovement((0,0.01*vec[0],0),True)
                own["distTo"] = vec[0]
        else:
            own.suspendDynamics(True)
            own.setParent(touchFloor.hitObject)
                #if (vec[0] > 0.4):
                     #   own["wasdPressed"] = True
            #
    elif (own["player_mode"] == "FINDTERMINAL"):
        own.suspendDynamics(True)
        own.removeParent()
        own["follow"] = False
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
        terminal = closeObj.parent
        
        for object in terminal.children:
            if "align" in object:
                #print(terminal.children)
                
                object.children[0]["AI_enabled"] = True
                own["lastTerminal"] = object
        own.worldOrientation = closeObj.worldOrientation
        own.worldPosition = closeObj.worldPosition        
        #print(closeObj)
                
       # if ((hitTerminal.positive) == False):       
          #  if (closeObj != own):
                #own.alignAxisToVect((own.getVectTo(closeObj)[1]), 1, 0.5)
                
                
                #own.applyMovement((0,0.02*own.getVectTo(closeObj)[0],0),True)           
    else:            
        own["autoBump"] = False
        
    
   
    space = cont.sensors["Space"]
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
                
            #if space.positive:
                
    #own.localLinearVelocity.z += 1       
    jumpTime = 0.2
    jumpForce = 0.7
    jumpIncrement = 0.1
    
    
    if w.positive or s.positive or d.positive or a.positive:
        own["wasdPressed"] = True
    else:
        own["wasdPressed"] = False
    
    
    if (space.positive and own["jumpTimer"] > 0):
        
        own["jumpTimer"] -= jumpIncrement
        #own.localLinearVelocity.z +=jumpForce
        own.applyMovement((0,0,own["maxSpeed"]),True)
        
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
    magRay = cont.sensors["MagRay"]
    if (touchFloor.positive):
        if (floor.positive) and own["follow"] == False:
            own.worldLinearVelocity = floor.hitObject.worldLinearVelocity
            
            if (own["player_mode"] != "FINDTERMINAL"):
                own.alignAxisToVect(-own.getVectTo(magRay.hitPosition)[1],2,9.0)
                
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
    
    #if (own["distanceToFloor"] > 3) and own["follow"] == True:
       # own["follow"] = False
    #if touchFloor.positive:
        #own.worldLinearVelocity = touchFloor.hitObject.worldLinearVelocity 
    #own.localLinearVelocity.x = 0
    #own.localLinearVelocity.y = 0