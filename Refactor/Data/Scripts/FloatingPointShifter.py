def updateLogic(cont):
    own = cont.owner
    scene = own.scene
    
    
    
    playerHit = own 
    for object in scene.objects:
        if "onlyPlayer" in object:
            playerHit = object
    
    
    #print(own.getVectTo(playerHit)[0] )
    if (own.getVectTo(playerHit)[0] > 100.0):   
        for obj in scene.objects:
            if ("freezeObject" in obj) == False:
                if (obj.parent == None):  
                    diffX = obj.worldPosition.x - own.worldPosition.x
                    diffY = obj.worldPosition.y - own.worldPosition.y
                    diffZ = obj.worldPosition.z - own.worldPosition.z
                    #print(str(diffX)+" "+str(diffY)+" "+str(diffZ))
                    obj.suspendDynamics(True)
                    obj.worldPosition.x = diffX
                    obj.worldPosition.y = diffY
                    obj.worldPosition.z = diffZ
                    obj.restoreDynamics()
                    #print("justshifted")
        own.worldPosition.x = playerHit.worldPosition.x
        own.worldPosition.y = playerHit.worldPosition.y
        own.worldPosition.z = playerHit.worldPosition.z
    

#NOTE: TURNING ON DEBUG MODE FOR SOME REASON MAKES EVERYTHING
#REALLY WACK BUT IT'S ALL GOOD IF YOU JUST LEAVE IT OFF