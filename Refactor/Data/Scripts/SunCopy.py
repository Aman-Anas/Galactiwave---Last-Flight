def updateSun(cont):
    own = cont.owner
    mainSun = own.scene.objects["MainSun"]
    playerSun = own.children[0]
    playerSun.energy = mainSun.energy/2
    playerSun.color = mainSun.color
    own.worldOrientation = mainSun.worldOrientation
    own.worldPosition = own.scene.objects["Player_Hitbox"].worldPosition