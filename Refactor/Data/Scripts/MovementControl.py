#import bpy
from mathutils import Vector
def updateVal (cont):
    own = cont.owner
    w = cont.sensors["W"]
    s = cont.sensors["S"]
    d = cont.sensors["D"]
    a = cont.sensors["A"]
    
    terminalCol = cont.sensors["terminalCol"]
    r = cont.sensors["R"]
    camAct = cont.actuators["SetCam"]
    shift = cont.sensors["Shift"]
    
    if shift.positive:
        own["maxSpeed"] = own["maxRun"]
    else:
        own["maxSpeed"] = own["maxWalk"]
    
    if (w.positive) and (s.positive == False):
        if (own["yDisp"] < own["maxSpeed"]):
            own["yDisp"] += own["increment"]
        else:
            own["yDisp"] = own["maxSpeed"]
    else:
        if (own["yDisp"] > 0):
            own["yDisp"] = 0
    
    if (s.positive) and (w.positive == False):
        if (own["yDisp"] > -own["maxSpeed"]):
            own["yDisp"] -= own["increment"]
        else:
            own["yDisp"] = -own["maxSpeed"]
    else:
        if (own["yDisp"] < 0):
            own["yDisp"] = 0
    ########
    if (d.positive) and (a.positive == False):
        if (own["xDisp"] < own["maxSpeed"]):
            own["xDisp"] += own["increment"]
        else:
            own["xDisp"] = own["maxSpeed"]
    else:
        if (own["xDisp"] > 0):
            own["xDisp"] = 0
    
    if (a.positive) and (d.positive == False):
        if (own["xDisp"] > -own["maxSpeed"]):
            own["xDisp"] -= own["increment"]
        else:
            own["xDisp"] = -own["maxSpeed"]
    else:
        if (own["xDisp"] < 0):
            own["xDisp"] = 0
    
    if (own["moveActive"] == True):
        own.applyMovement((own["xDisp"],own["yDisp"],0),True)
    
    if (own["currentTerminal"] == 0):
        own["currentTerminal"] = own
    if (r.positive) or (own.getVectTo(own["currentTerminal"])[0] > 2):
        if (own["player_mode"] == "ACTIVE"):
            if (terminalCol.positive):    
                own["currentTerminal"] = terminalCol.hitObject
                own["player_mode"] = "TERMINAL"
                camAct.camera["active"] = False
                own.suspendDynamics(True)
                #The order goes camera is parented to the axis thing is parented to the aligner
                #so it accesses the children in reverse order
                
                own["dif"]= own.worldPosition - own["currentTerminal"].worldPosition
               
                
                if (own["currentTerminal"]["terminal_gui"] == "weapons"):
                    for obj in own["currentTerminal"].children:
                        if "align" in obj:
                            camAct.camera = obj.children[0].children[0]
                    camAct.camera.parent["active"] = True
                elif (own["currentTerminal"]["terminal_gui"] == "pilot"):
                    for obj in own["currentTerminal"].children:
                        if "align" in obj:
                            camAct.camera = obj.children[0].children[0].children[0]
                    camAct.camera.parent.parent["active"] = True
                
                
                    
        elif (own["player_mode"] == "TERMINAL"):
            own.restoreDynamics()
            #This child is the camera which has the terminal as its parent
            #setting active to false so that it doesn't move around when player is not on it
            if (own["currentTerminal"]["terminal_gui"] == "weapons"):
                camAct.camera.parent["active"] = False
            elif (own["currentTerminal"]["terminal_gui"] == "pilot"):
                
                camAct.camera.parent.parent["active"] = False
                
            #camAct.camera.parent["active"] = False
            camAct.camera = "PlayerCam"
            camAct.camera["active"] = True
            own["player_mode"] = "ACTIVE"  
            own["currentTerminal"] = own
            
                
            
            
            
    
    jumpTime = 0.2
    jumpForce = 0.7
    jumpIncrement = 0.1
    
    floor = cont.sensors["floorRay"]
    
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
    touchFloor = cont.sensors["touchFloor"]      
    if ((space.positive == False) and (touchFloor.positive)) and (floor.positive):
        if (own["onFloor"] == True):
            #own.setParent(floor.hitObject)
            own.worldLinearVelocity = floor.hitObject.worldLinearVelocity
            #own.applyForce(own.getVectTo(floor.hitPosition)[1],True)
            #own.worldAngularVelocity = floor.hitPosition.worldAngularVelocity
            
            #own.localAngularVelocity.z = 0
            #own.localLinearVelocity.z = 0
            
                
    
    if own["player_mode"] == "TERMINAL": 
       
        if "dif" in own: 
            
            #print(own["dif2"])
            #own.localPosition = own["currentTerminal"].localPosition - own["dif2"]
            if floor.positive:
                #vect = floor.hitObject.getLinearVelocity(False)
                own.worldOrientation = floor.hitObject.worldOrientation
                own.worldLinearVelocity = floor.hitObject.worldLinearVelocity
                #own.localLinearVelocity.y = 0
                #own.localLinearVelocity.x = 0
                #own.worldOrientation = floor.hitObject.worldOrientation
                #hit = cont.sensors["MagRay"]
                dist = own.getVectTo(own["currentTerminal"])
                
                for obj in own["currentTerminal"].children:
                    if "terminalTar" in obj:
                        own.worldOrientation = obj.worldOrientation
                        own.worldPosition = obj.worldPosition
                #rotDif = Vector(own.worldOrientation.col[1].rotation_difference(dist[1]).to_euler())
                #own.worldAngularVelocity = floor.hitObject.worldAngularVelocity #* rotDif
                
                #own.alignAxisToVect((dist[1]), 1, 0.2)
                #own.applyForce((0,100*dist[0],0),True) 
                #own.alignAxisToVect(dist[1],2,0.1)
                
                #own.applyMovement(dist[1]*0.1*dist[0],False)
                
            #print(own["currentTerminal"])           
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
    