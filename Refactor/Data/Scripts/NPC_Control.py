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
        if own["follow"] == True:
            if ((player.positive) == False):
                
                for obj in own.scene.objects:
                    if "onlyPlayer" in obj:
                        vec = own.getVectTo(obj)
                        own.alignAxisToVect((vec[1]), 1, 0.2)
                        own.applyForce((0,20*vec[0],0),True)
    elif (own["player_mode"] == "FINDTERMINAL"):
        if ((hitTerminal.positive) == False):
            for obj in own.scene.objects:
                    if "terminal" in obj:
                        vec = own.getVectTo(obj)
                        own.alignAxisToVect((vec[1]), 1, 0.2)
                        own.applyForce((0,20*vec[0],0),True)
    else:            
        own["autoBump"] = False
        
    
   
    
    #self-correct position to stay out of the way of things
    if (own["moveActive"] == True): 
        #Only enable auto-correction if this is true, controlled by state
        if (own["autoBump"] == True):
            if w.positive:
                cont.activate(cont.actuators["Forward"])
            else:
                cont.deactivate(cont.actuators["Forward"])
                
            if s.positive:
                cont.activate(cont.actuators["Back"])
            else:
                cont.deactivate(cont.actuators["Back"])
                
            if d.positive:
                cont.activate(cont.actuators["Right"])
            else:
                cont.deactivate(cont.actuators["Right"])
                
            if a.positive:
                cont.activate(cont.actuators["Left"])
            else:
                cont.deactivate(cont.actuators["Left"])
        
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
    own.localLinearVelocity.x = 0
    own.localLinearVelocity.y = 0