import json
import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner

path = bge.logic.expandPath(r"//Saves\CurrentSave.txt")

with open(path, 'r+') as openFile:
    data = json.load(openFile)
    own["CurrentSave"] = data["CurrentSave"]

own["saveFile"] = "save"+(own["CurrentSave"])+".txt"


pathTwo = bge.logic.expandPath("//..\Saves\\"+(own["saveFile"]))

dicData = {
    "TimeOfDay": own["TimeOfDay"], 
}

with open(pathTwo, 'w+') as fileBoi:
    json.dump(dicData, fileBoi)

