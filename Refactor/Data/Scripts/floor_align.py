import bge
from mathutils import Vector
from bge import render



scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()




own = cont.owner
sen = cont.sensors["MagRay"]


hitNormal = sen.hitNormal
if hitNormal: # check before if the ray hit something
    #render.drawLine(sen.hitPosition,own.worldPosition,(255,0,0))
    hitNormal = Vector(hitNormal) # transform in to Vector
    axisZ = own.worldOrientation.col[2]
    v1 = axisZ
    v2 = hitNormal
    rotDif = Vector(v1.rotation_difference(v2).to_euler())
    own["distToAlign"] = rotDif[0] + rotDif[1] + rotDif[2]
    if (abs(own["distToAlign"]) > 0.06):
        own["aligning"] = True
    else:
        own["aligning"] = False
    #print(own["aligning"])
    #print(sen.hitPosition)
   # currentRot = own.localOrientation.to_euler()
   # currentRot.x = 0
    #currentRot.y = 0
    #own.localOrientation = currentRot
    
    rot = own.worldAngularVelocity
    rot += rotDif *3 #"elasticity"
    rot *= 0.8 # inertia
    #print("wow")
    own.applyForce(-hitNormal*9.8)#gravity to the normal