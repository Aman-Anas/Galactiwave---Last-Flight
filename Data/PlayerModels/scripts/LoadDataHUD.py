import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner

own.resolution = 5.0
original = bge.logic.getSceneList()['Original']
data = original.objects["GameControl"]
own["Money"] = data["Money"]
own["Name"] = data["Name"]
own["EnemiesAlive"] = data["EnemiesAlive"]
own["CurrentLander"] = data["CurrentLander"]

        
