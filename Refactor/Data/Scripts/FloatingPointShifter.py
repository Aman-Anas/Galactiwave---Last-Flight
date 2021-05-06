def updateLogic(cont):
    own = cont.owner
    scene = own.scene
    
    
    
    playerHit = own 
    for object in scene.objects:
        if "onlyPlayer" in object:
            playerHit = object
    
    print(playerHit.worldPosition)
    #print(own.getVectTo(playerHit)[0] )\
    
    #ok so it checks if the player is in terminal mode, because for SOME reason
    #AND I HAVE NO IDEA WHY
    #the player gets yeeted out of a flying ship if the interior is a separate object
    #from the hitbox/exterior.
    #so, this just avoids that problem, and works well enough for now I guess
    #it should shift as soon as the player is on aa terminal (and distance is great enough)
    floorSen = playerHit.sensors["touchFloor"]
    if (own.getVectTo(playerHit)[0] > 100.0) and (floorSen.positive == False):
        
        #playerHit["floorParent"] = False
        #if (floorSen.positive):
            #playerHit.setParent(floorSen.hitObject)
            #playerHit["floorParent"] = True
        playerHit.suspendDynamics(True)
        playerPos = [playerHit.worldPosition.x, playerHit.worldPosition.y, playerHit.worldPosition.z]
        #diffX = playerHit.worldPosition.x - own.worldPosition.x
        #diffY = playerHit.worldPosition.y - own.worldPosition.y
        #diffZ = playerHit.worldPosition.z - own.worldPosition.z
        own.scene.suspend()
        
        #playerHit.suspendDynamics(True)
        #diffX = playerHit.worldPosition.x - own.worldPosition.x
        # diffY = playerHit.worldPosition.y - own.worldPosition.y
        #  diffZ = playerHit.worldPosition.z - own.worldPosition.z
        #   playerHit.worldPosition.x = diffX
        #    playerHit.worldPosition.y = diffY
        # playerHit.worldPosition.z = diffZ
        # playerHit.restoreDynamics()
        
        for obj in scene.objects:
            if ("freezeObject" in obj) == False:
                obj["unParent"] = False
                #obj.suspendDynamics(True)
                if (obj.parent == None): 
                    
                    obj["currentVelo"] = obj.worldLinearVelocity
                    
                    if (obj != playerHit):
                        obj.setParent(own)
                        obj["unParent"] = True
                    #else:
                        
                        #print("justshifted")
                    
                    #print(str(diffX)+" "+str(diffY)+" "+str(diffZ))
                    
                    
                    
                #obj.restoreDynamics()
               
                    
        #sun = own.scene.objects["MainSun"]
        #sun.updateShadow()
        
        own.scene.resume()
        
        own.worldPosition.x = -playerPos[0]
        own.worldPosition.y = -playerPos[1]
        own.worldPosition.z = -playerPos[2]
        playerHit.worldPosition.x = 0
        playerHit.worldPosition.y = 0
        playerHit.worldPosition.z = 0
        for obj in scene.objects:
            if ("unParent" in obj):
                if (obj["unParent"] == True):
                    obj.removeParent()
                    #if (obj.getPhysicsId() != 0):
                        #obj.worldLinearVelocity = obj["currentVelo"]
        
        own.worldPosition.x = 0
        own.worldPosition.y = 0
        own.worldPosition.z = 0
        #if (playerHit["floorParent"] == True):
          #  playerHit.removeParent()
        #playerHit.localPosition.z += 0.2
        floorSen = playerHit.sensors["touchFloor"]
        if (floorSen.positive == False):
            playerHit.restoreDynamics()
        
        
        
        #own.worldPosition.x = playerHit.worldPosition.x
        #own.worldPosition.y = playerHit.worldPosition.y
       # own.worldPosition.z = playerHit.worldPosition.z
       # playerHit.localLinearVelocity.y = 0
        #playerHit.localLinearVelocity.x = 0
        #playerHit.localLinearVelocity.z = 0
        #playerHit.restoreDynamics()
       # if ("mag" in playerHit):
           # playerHit.worldPosition = own["mag"].worldPosition + own["dispFromMag"]
        #playerHit.worldLinearVelocity = [0,0,0]
        

#NOTE: TURNING ON DEBUG MODE FOR SOME REASON MAKES EVERYTHING
#REALLY WACK BUT IT'S ALL GOOD IF YOU JUST LEAVE IT OFF