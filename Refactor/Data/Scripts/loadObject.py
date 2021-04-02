import bge.logic
def loadObj(cont):
    own = cont.owner
    
    
    #set paths for libload files
    if (own["loaded"] == False):
        own.scene.suspend()
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
                                    #print("ok")
                                    childObj.worldPosition = own.children[0].worldPosition
                                    childObj.worldOrientation = own.children[0].worldOrientation
                                    #if (newObj["terminal_gui"] == "weapons"):
                                        #print("wao")
                                        #childObj.children[0].worldOrientation += own.worldOrientation
                        
                            #own.children[0].endObject()
                        #if (newObj["terminal_gui"] == "pilot"):
        own["loaded"] = True
        own.scene.resume()
    #print("wao")
#own.endObject()

