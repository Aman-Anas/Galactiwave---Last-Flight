from math import degrees
from math import radians
def updateAim(cont):
    own = cont.owner
    cam = own.children[0]
    maxY = own["maxY"]
    minY = own["minY"]
    if (own["active"] == False):
        if (own["AI_enabled"] == True):
            cont.deactivate(cont.actuators["X"])
            cont.deactivate(cont.actuators["Y"])
            #print(maxY)
            #print(minY)
            
            deg = degrees(cam.localOrientation.to_euler()[0]) - 90
            #print(deg)
            for obj in own.scene.objects:
                if "selected_tar" in obj:
                    if (obj["selected_tar"] == True):
                        cont.actuators["TrackX"].object = obj
                        cont.actuators["TrackY"].object = obj
            #print()
            if ((deg >= minY) and (deg <= maxY)):
                cont.activate(cont.actuators["TrackY"])
                
            if (deg < minY):
                cont.deactivate(cont.actuators["TrackY"])
                own.applyRotation((radians(minY - deg),0,0),True)
                #print(minY - deg)
                
            if (deg > maxY):
                cont.deactivate(cont.actuators["TrackY"])
                own.applyRotation((radians(maxY - deg),0,0),True)
                #print(maxY - deg)
            #own["angleReset"] = False
            
            cont.activate(cont.actuators["TrackX"])
        else:
            
            cont.deactivate(cont.actuators["TrackY"])
            cont.deactivate(cont.actuators["TrackX"])
    else:
        cont.deactivate(cont.actuators["TrackY"])
        cont.deactivate(cont.actuators["TrackX"])
        deg = degrees(cam.localOrientation.to_euler()[0]) - 90
        print(deg)
        cont.activate(cont.actuators["X"])
        if ((deg >= minY) and (deg <= maxY)):
            cont.activate(cont.actuators["Y"])
            
        if (deg < minY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(minY) +radians(90)
            cam.localOrientation = cur
            #cam.applyRotation((radians(minY - deg),0,0),True)
            #print(deg < minY)
        if (deg > maxY):
            cont.deactivate(cont.actuators["Y"])
            cur = cam.localOrientation.to_euler()
            cur.x = radians(maxY) + radians(90)
            cam.localOrientation = cur
            #cam.applyRotation((radians(maxY - deg),0,0),True)