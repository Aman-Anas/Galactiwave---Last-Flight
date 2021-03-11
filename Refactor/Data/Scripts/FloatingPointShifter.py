def updateLogic(cont):
    own = cont.owner
    scene = own.scene
    for obj in scene.objects:
        if "reset" in obj:
            diffX = obj.worldPosition.x - own.worldPosition.x
            diffY = obj.worldPosition.y - own.worldPosition.y
            diffZ = obj.worldPosition.z - own.worldPosition.z
            #print(str(diffX)+" "+str(diffY)+" "+str(diffZ))
            obj.worldPosition.x = diffX
            obj.worldPosition.y = diffY
            obj.worldPosition.z = diffZ
    own.worldPosition.x = 0
    own.worldPosition.y = 0
    own.worldPosition.z = 0

#NOTE: TURNING ON DEBUG MODE FOR SOME REASON MAKES EVERYTHING
#REALLY WACK BUT IT'S ALL GOOD IF YOU JUST LEAVE IT OFF