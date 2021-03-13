#import bpy
def updateVal (cont):
    own = cont.owner
    w = cont.sensors["W"]
    s = cont.sensors["S"]
    d = cont.sensors["D"]
    a = cont.sensors["A"]
    
    terminalCol = cont.sensors["terminalCol"]
    e = cont.sensors["E"]
    camAct = cont.actuators["SetCam"]
    
    if (e.positive):
        if (own["player_mode"] == "ACTIVE"):
            if (terminalCol.positive):    
                terminal = terminalCol.hitObject
                own["player_mode"] = "TERMINAL"
                camAct.camera["active"] = False
                #The order goes camera is parented to the axis thing is parented to the aligner
                #so it accesses the children in reverse order
                if (terminal["terminal_gui"] == "weapons"):
                    camAct.camera = terminal.children[0].children[0].children[0]
                
                camAct.camera.parent["active"] = True
                    
        elif (own["player_mode"] == "TERMINAL"):
            own["player_mode"] = "ACTIVE"
            #This child is the camera which has the terminal as its parent
            #setting active to false so that it doesn't move around when player is not on it
            camAct.camera.parent["active"] = False
            camAct.camera = "PlayerCam"
            camAct.camera["active"] = True
                
    
                
            
            
            
    
    jumpTime = 0.2
    jumpForce = 0.7
    jumpIncrement = 0.1
    
    
    if w.positive or s.positive or d.positive or a.positive:
        own["wasdPressed"] = True
    else:
        own["wasdPressed"] = False
    
    space = cont.sensors["Space"]
    if (space.positive and own["jumpTimer"] > 0) and (own["moveActive"] == True):
        
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