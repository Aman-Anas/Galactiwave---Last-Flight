import json
import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner


path = bge.logic.expandPath(r"//..\SaveData\saveData.txt")

with open(path, 'r+') as fh:
    
    data = json.load(fh)
    own["Money"] = data["Money"]
    own["Name"] = data["Name"]
    own["EnemiesAlive"] = data["EnemiesAlive"]
    own["CurrentShip"] = data["CurrentShip"]
    own["CurrentLander"] = data["CurrentLander"]
    
        

