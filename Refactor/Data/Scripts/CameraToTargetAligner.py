def updateAlign(cont):
    own = cont.owner
    scene = own.scene
    aligner = own.parent
    vectorToAligner = own.getVectTo(aligner)
    own.alignAxisToVect(-vectorToAligner[1], 2, 1.0)
    #print("wao")
    