def updateVal (cont):
    own = cont.owner
    w = cont.sensors["W"]
    s = cont.sensors["S"]
    d = cont.sensors["D"]
    a = cont.sensors["A"]
    
    #self-correct position to stay out of the way of things
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