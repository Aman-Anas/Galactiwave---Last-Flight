import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner
scene = bge.logic.getCurrentScene()

def updateLogic():
    diffX = own.worldPosition
    