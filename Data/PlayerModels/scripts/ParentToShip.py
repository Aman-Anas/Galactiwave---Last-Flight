import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner
scene = bge.logic.getCurrentScene()
hitbox = scene.objects["Hitbox"]
own.setParent(hitbox, True, True)
own.worldTransform = hitbox.worldTransform