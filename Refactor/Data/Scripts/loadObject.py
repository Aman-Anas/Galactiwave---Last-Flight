import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner

#set paths for libload files
filePath = bge.logic.expandPath(own["filePath"])
#make sure it's not already loaded
if ((filePath) in bge.logic.LibList()) == False:
    #load libload files, 'Scene' is the mode argument for LibLoad (I think)
    bge.logic.LibLoad(filePath, 'Scene')

objName = own["objName"]
for obj in own.scene.objectsInactive:
    if (obj.name == objName):
        newObj = own.scene.addObject(obj, own, 0.0) 
        #object, reference, and time (time = 0 makes it last forever)
        if (own.parent != None):
            newObj.setParent(own.parent)
            if "terminal" in newObj:
                if (newObj["terminal_gui"] == "weapons") or (newObj["terminal_gui"] == "pilot"):
                    for childObj in newObj.children:
                        if "align" in childObj:
                            childObj.worldPosition = own.children[0].worldPosition
                    own.children[0].endObject()
                #if (newObj["terminal_gui"] == "pilot"):
                    
        
        own.endObject()
        
    
    

