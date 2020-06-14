import json
import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner
path = bge.logic.expandPath("//..\SaveData\saveData.txt")
dicData = {
"Money": own["Money"], 
"Name": own["Name"],
"EnemiesAlive": own["EnemiesAlive"],
"CurrentShip": own["CurrentShip"],
"CurrentLander": own["CurrentLander"]
}

with open(path, 'w+') as fileBoi:
    json.dump(dicData, fileBoi)




    


