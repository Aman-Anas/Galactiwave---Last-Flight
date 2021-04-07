from math import degrees
from math import radians
from mathutils import Matrix, Vector, Euler

def updateAim(cont):
    own = cont.owner
    cam = own.children[0]
    maxY = own["maxY"]
    minY = own["minY"]
    
    npc = cont.sensors["NPC"]
    
    #if (((npc.positive) and (npc.hitObject["NPC"] == "alive")) and (npc.hitObject["player_mode"] == "FINDTERMINAL")):
       # own["AI_enabled"] = True
   # else:
     #   own["AI_enabled"] = False
    
    if (own["active"] == False):
        cont.deactivate(cont.actuators["X"])
        cont.deactivate(cont.actuators["Y"])
        
        if (own["AI_enabled"] == True):
            #print(own)
            cont.deactivate(cont.actuators["X"])
            cont.deactivate(cont.actuators["Y"])
            #print(maxY)
            #print(minY)
            #maxY = own["minY"]
            #minY = own["maxY"]
            deg = -degrees(cam.localOrientation.to_euler()[1])
            #print(deg)
            
            camOrient = cam.localOrientation.to_euler()
            camOrient.x = radians(90)
            camOrient.y = radians(180)
            camOrient.z = radians(0) - own.parent.localOrientation.to_euler().y 
            cam.localOrientation = camOrient
            own["target_track"] = "none"
            for obj in own.scene.objects:
                if "selected_tar" in obj:
                    if (obj["selected_tar"] == True):
                        #cont.actuators["TrackX"].object = obj
                        cont.actuators["TrackY"].object = obj
                        own["target_track"] = obj
                        #print(own["target_track"])
            
            
           # if ((deg >= minY) and (deg <= maxY)):
            if (own["target_track"] != "none"):
                cam.alignAxisToVect((own.getVectTo(own["target_track"])[1]),1,0.14)
              #  cont.activate(cont.actuators["TrackY"])
                #cont.deactivate(cont.actuators["TrackY"])
                currentRot = cam.localOrientation.to_euler()
                #parentRot = own.parent.localOrientation.to_euler()
                currentRot.y = radians(0)
                #print(degrees(parentRot.y))
                own.localOrientation = currentRot
                #cam.alignAxisToVect((cam.getVectTo(ting)[1]), 2, 1)
                
           # if (deg < minY):
             #   cont.deactivate(cont.actuators["TrackY"])
             #   curRot = cam.localOrientation.to_euler()
             ##   curRot.x = radians(minY) + radians(0.01)
             #   cam.localOrientation = curRot
                #own.applyRotation((radians(minY - deg),0,0),True)
                #print(minY - deg)
                
           # if (deg > maxY):
           #     cont.deactivate(cont.actuators["TrackY"])
             #   curRot = cam.localOrientation.to_euler()
             #   curRot.x = radians(maxY) - radians(0.01)
             #   cam.localOrientation = curRot
                #own.applyRotation((radians(maxY - deg),0,0),True)
                #print(maxY - deg)
            own["angleReset"] = False
            own["savedAngle"] = own.localOrientation.to_euler()
            #cont.activate(cont.actuators["TrackX"])
        else:
            #cont.deactivate(cont.actuators["X"])
            #cont.deactivate(cont.actuators["Y"])
            cont.deactivate(cont.actuators["TrackY"])
            orientNow = own.localOrientation.to_euler()
            orientNow.z = radians(0)
            #orientNow.y = radians(180)
            #orientNow.x = radians(0)
            #orientNow.y = radians(0)
            own.localOrientation = orientNow
            #own["angleReset"] = False
           # own["savedAngle"] = own.localOrientation.to_euler()
            #cont.deactivate(cont.actuators["TrackX"])
            
    else:
        
        
        if (own["angleReset"] == False):
            if ("savedAngle" in own):
                camOrient = cam.localOrientation.to_euler()
                camOrient.x = radians(90)
                camOrient.y = radians(0) 
                camOrient.z = radians(0) - own.parent.localOrientation.to_euler().y 
                cam.localOrientation = camOrient
                curOrient = cam.localOrientation.to_euler()
                curOrient.x = own["savedAngle"].x + radians(90)
                cam.localOrientation = curOrient
                own["angleReset"] = True
        cont.deactivate(cont.actuators["TrackY"])
        #cont.deactivate(cont.actuators["TrackX"])
        deg = degrees(cam.localOrientation.to_euler()[0]) - 90
        #print(deg)
        
        cont.activate(cont.actuators["X"])
        
        if ((deg >= minY) and (deg < maxY)):
            cont.activate(cont.actuators["Y"])
            
        if (deg < minY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(minY) +radians(91)
            cam.localOrientation = cur
            #print(cur)
            #cam.applyRotation((radians(minY - deg),0,0),True)
            #print(deg < minY)
        if (deg > maxY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(maxY) + radians(89)
            cam.localOrientation = cur
            
            ##print(cur)
            #cam.applyRotation((radians(maxY - deg),0,0),True)