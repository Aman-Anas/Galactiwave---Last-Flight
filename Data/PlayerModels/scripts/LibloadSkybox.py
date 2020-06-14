import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner

skybox = bge.logic.expandPath("//..\LevelData\Skyboxes\Skybox1.blend")
bge.logic.LibLoad(skybox, 'Scene')