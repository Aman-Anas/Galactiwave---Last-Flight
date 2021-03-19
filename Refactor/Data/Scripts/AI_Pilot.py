from math import degrees
from math import radians
from mathutils import Matrix, Vector, Euler

def updateLook(cont):
    own = cont.owner
    cam = own.children[0]
    maxY = own["maxY"]
    minY = own["minY"]
    ship = own.parent.parent.parent
    
    npc = cont.sensors["NPC"]
    
    pilotCam = own.children[0].children[0]
    dist = own.getVectTo(pilotCam)[0]
    if (dist < ship["camZoom"]):
        pilotCam.applyMovement((0,0,ship["camZoom"]-dist),True)
    elif (dist > ship["camZoom"]):
        pilotCam.applyMovement((0,0,ship["camZoom"]-dist),True)
    
    
    if (((npc.positive) and (npc.hitObject["NPC"] == "alive")) and (npc.hitObject["player_mode"] == "FINDTERMINAL")):
        own["AI_enabled"] = True
    else:
        own["AI_enabled"] = False
    
    if (own["active"] == False):
        if (own["AI_enabled"] == True):
            #print(own)
            cont.deactivate(cont.actuators["X"])
            cont.deactivate(cont.actuators["Y"])
            #print(maxY)
            #print(minY)
            
            deg = degrees(own.localOrientation.to_euler()[0])
            #print(deg)
            
            camOrient = cam.localOrientation.to_euler()
            camOrient.x = 0#radians(90)
            camOrient.y = 0
            camOrient.z = 0
            cam.localOrientation = camOrient
            own["target_track"] = "none"
            for obj in own.scene.objects:
                if "selected_tar" in obj:
                    if (obj["selected_tar"] == True):
                        #cont.actuators["TrackX"].object = obj
                        #cont.actuators["TrackY"].object = obj
                        own["target_track"] = obj
                        
            
            
            if ((deg >= minY) and (deg <= maxY)):
                if (own["target_track"] != "none"):
                    own.alignAxisToVect((own.getVectTo(own["target_track"])[1]),1,0.5)
              #  cont.activate(cont.actuators["TrackY"])
                #cont.deactivate(cont.actuators["TrackY"])
                currentRot = own.localOrientation.to_euler()
                #parentRot = own.parent.localOrientation.to_euler()
                currentRot.y = radians(0)
                #print(degrees(currentRot.y))
                own.localOrientation = currentRot
                #cam.alignAxisToVect((cam.getVectTo(ting)[1]), 2, 1)
                
            if (deg < minY):
             #   cont.deactivate(cont.actuators["TrackY"])
                #own.applyRotation((radians(minY - deg),0,0),True)
                nowRot = own.localOrientation.to_euler()
                nowRot.x = radians(minY) + radians(0.5)
                own.localOrientation = nowRot
                #print(minY - deg)
                
            if (deg > maxY):
                #cont.deactivate(cont.actuators["TrackY"])
                #own.applyRotation((radians(maxY - deg),0,0),True)
                nowRot = own.localOrientation.to_euler()
                nowRot.x = radians(maxY) - radians(0.5)
                own.localOrientation = nowRot
                #print(maxY - deg)
            own["angleReset"] = False
            own["savedAngle"] = own.localOrientation.to_euler()
            #cont.activate(cont.actuators["TrackX"])
        else:
            
            cont.deactivate(cont.actuators["TrackY"])
            #cont.deactivate(cont.actuators["TrackX"])
    else:
        if (own["angleReset"] == False):
            if ("savedAngle" in own):
                curOrient = cam.localOrientation.to_euler()
                curOrient.x = own["savedAngle"].x #+ radians(90)
                cam.localOrientation = curOrient
                own["angleReset"] = True
        cont.deactivate(cont.actuators["TrackY"])
        #cont.deactivate(cont.actuators["TrackX"])
        deg = degrees(cam.localOrientation.to_euler()[0]) #- 90
        #print(deg)
        
        cont.activate(cont.actuators["X"])
        
        if ((deg >= minY) and (deg <= maxY)):
            cont.activate(cont.actuators["Y"])
            
        if (deg < minY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(minY) +radians(1)
            cam.localOrientation = cur
            #print(cur)
            #cam.applyRotation((radians(minY - deg),0,0),True)
            #print(deg < minY)
        if (deg > maxY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(maxY) + radians(-1)
            cam.localOrientation = cur
            #print(cur)
            #cam.applyRotation((radians(maxY - deg),0,0),True)
        
        w = cont.sensors["W"]
        a = cont.sensors["A"]
        s = cont.sensors["S"]
        d = cont.sensors["D"]
        shift = cont.sensors["Shift"]
        ctrl = cont.sensors["Ctrl"]
        q = cont.sensors["Q"]
        e = cont.sensors["E"]
        #Move ship code
        
        #speed
        if (shift.positive) and (ctrl.positive == False):
            if (ship["currentSpeed"] < ship["maxSpeed"]):
                ship["currentSpeed"] += ship["accelSpeed"]
            elif (ship["currentSpeed"] > ship["maxSpeed"]):
                ship["currentSpeed"] = ship["maxSpeed"]
        if (ctrl.positive) and (shift.positive == False):
            if (ship["currentSpeed"] > -ship["maxSpeed"]):
                ship["currentSpeed"] -= ship["accelSpeed"]
            elif (ship["currentSpeed"] < -ship["maxSpeed"]):
                ship["currentSpeed"] = -ship["maxSpeed"]
        #pitch
        if (s.positive) and (w.positive == False):
            if (ship["pitch"] < ship["maxTurn"]):
                ship["pitch"] += ship["accelTurn"]
            elif (ship["pitch"] > ship["maxTurn"]):
                ship["pitch"] = ship["maxTurn"]
        else:
            if (ship["pitch"] > 0):
                ship["pitch"] = 0
    
        if (w.positive) and (s.positive == False):
            if (ship["pitch"] > -ship["maxTurn"]):
                ship["pitch"] -= ship["accelTurn"]
            elif (ship["pitch"] < -ship["maxTurn"]):
                ship["pitch"] = -ship["maxTurn"]
        else:
            if (ship["pitch"] < 0):
                ship["pitch"] = 0
        #yaw
        if (a.positive) and (d.positive == False):
            if (ship["yaw"] < ship["maxTurn"]):
                ship["yaw"] += ship["accelTurn"]
            elif (ship["yaw"] > ship["maxTurn"]):
                ship["yaw"] = ship["maxTurn"]
        else:
            if (ship["yaw"] > 0):
                ship["yaw"] = 0
        
        if (d.positive) and (a.positive == False):
            if (ship["yaw"] > -ship["maxTurn"]):
                ship["yaw"] -= ship["accelTurn"]
            elif (ship["yaw"] < -ship["maxTurn"]):
                ship["yaw"] = -ship["maxTurn"]
        else:
            if (ship["yaw"] < 0):
                ship["yaw"] = 0
        #roll
        if (e.positive) and (q.positive == False):
            if (ship["roll"] < ship["maxTurn"]):
                ship["roll"] += ship["accelTurn"]
            elif (ship["roll"] > ship["maxTurn"]):
                ship["roll"] = ship["maxTurn"]
        else:
            if (ship["roll"] > 0):
                ship["roll"] = 0
        
        if (q.positive) and (e.positive == False):
            if (ship["roll"] > -ship["maxTurn"]):
                ship["roll"] -= ship["accelTurn"]
            elif (ship["roll"] < -ship["maxTurn"]):
                ship["roll"] = -ship["maxTurn"]
        else:
            if (ship["roll"] < 0):
                ship["roll"] = 0
    
    
    if (own["active"] == True) or (own["AI_enabled"] == True):
        ship.setAngularVelocity((ship["pitch"],ship["roll"],ship["yaw"]),True)
    else:
        ship.setAngularVelocity((0,0,0),True)
    if (ship.localLinearVelocity.y < ship["currentSpeed"]):
        #if ship["currentSpeed"] <= 0:
         #   ship.localLinearVelocity.y = 0
        ship.localLinearVelocity.y += ship["accelSpeed"]*2
    if (ship.localLinearVelocity.y > ship["currentSpeed"]):
       # if ship["currentSpeed"] >= 0:
       #     ship.localLinearVelocity.y = 0
        ship.localLinearVelocity.y -= ship["accelSpeed"]*2
    #ship.localLinearVelocity.y = ship["currentSpeed"]
    
    if (ship.localLinearVelocity.y > ship["maxSpeed"]):
        ship.localLinearVelocity.y = ship["maxSpeed"]
    if (ship.localLinearVelocity.y < -ship["maxSpeed"]):
        ship.localLinearVelocity.y = -ship["maxSpeed"]
        
        
    if (ship.localLinearVelocity.z < 0):
        ship.localLinearVelocity.z += 10
    ship.localLinearVelocity.z = 0
    ship.localLinearVelocity.x = 0
    #ship.localLinearVelocity.y = 200
    #print(ship.worldAngularVelocity)