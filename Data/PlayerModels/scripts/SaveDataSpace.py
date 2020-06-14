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

own["Space"] = 1


    


