def updateLogic(cont):
    own = cont.owner
    scene = own.scene
    
    
    
    playerHit = own 
    for object in scene.objects:
        if "onlyPlayer" in object:
            playerHit = object
    
    
    #print(own.getVectTo(playerHit)[0] )\
    
    #ok so it checks if the player is in terminal mode, because for SOME reason
    #AND I HAVE NO IDEA WHY
    #the player gets yeeted out of a flying ship if the interior is a separate object
    #from the hitbox/exterior.
    #so, this just avoids that problem, and works well enough for now I guess
    #it should shift as soon as the player is on aa terminal (and distance is great enough)
    if (own.getVectTo(playerHit)[0] > 100.0) and (playerHit["player_mode"] == "TERMINAL"):
        currentVelo = playerHit.worldLinearVelocity
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
                obj.suspendDynamics(True)
                if (obj.parent == None):  
                    diffX = obj.worldPosition.x - own.worldPosition.x
                    diffY = obj.worldPosition.y - own.worldPosition.y
                    diffZ = obj.worldPosition.z - own.worldPosition.z
                    #print(str(diffX)+" "+str(diffY)+" "+str(diffZ))
                    obj.worldPosition.x = diffX
                    obj.worldPosition.y = diffY
                    obj.worldPosition.z = diffZ
                    obj.restoreDynamics()
                    #print("justshifted")
        sun = own.scene.objects["MainSun"]
        sun.updateShadow()
        own.worldPosition.x = playerHit.worldPosition.x
        own.worldPosition.y = playerHit.worldPosition.y
        own.worldPosition.z = playerHit.worldPosition.z
        
        #playerHit.suspendDynamics(True)
        own.scene.resume()
        playerHit.restoreDynamics()
       # playerHit.localLinearVelocity.y = 0
        #playerHit.localLinearVelocity.x = 0
        #playerHit.localLinearVelocity.z = 0
        #playerHit.restoreDynamics()
       # if ("mag" in playerHit):
           # playerHit.worldPosition = own["mag"].worldPosition + own["dispFromMag"]
        #playerHit.worldLinearVelocity = [0,0,0]
        

#NOTE: TURNING ON DEBUG MODE FOR SOME REASON MAKES EVERYTHING
#REALLY WACK BUT IT'S ALL GOOD IF YOU JUST LEAVE IT OFF