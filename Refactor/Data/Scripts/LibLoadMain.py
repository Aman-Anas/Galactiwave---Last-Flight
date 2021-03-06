import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner
own.scene.suspend()
#set paths for libload files
playerController = bge.logic.expandPath("//Models\PlayerController.blend")
area = bge.logic.expandPath("//Models\Areas\BetterPlanetArea.blend")


#load libload files, 'Scene' is the mode argument for LibLoad (I think)
if ((playerController) in bge.logic.LibList()) == False:
    #load libload files, 'Scene' is the mode argument for LibLoad (I think)
    bge.logic.LibLoad(playerController, 'Scene')

if ((area) in bge.logic.LibList()) == False:
    #load libload files, 'Scene' is the mode argument for LibLoad (I think)
    bge.logic.LibLoad(area, 'Scene')
own.scene.resume()