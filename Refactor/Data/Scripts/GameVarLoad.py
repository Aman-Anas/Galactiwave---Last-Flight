import json
import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner


path = bge.logic.expandPath(r"//Saves\CurrentSave.txt")

with open(path, 'r+') as openFile:
    data = json.load(openFile)
    own["CurrentSave"] = data["CurrentSave"]

own["saveFile"] = "save"+(own["CurrentSave"])+".txt"

pathTwo = bge.logic.expandPath("//Saves\\"+(own["saveFile"]))

with open(pathTwo, 'r+') as openData:
    data = json.load(openData)
    own["TimeOfDay"] = data["TimeOfDay"]
