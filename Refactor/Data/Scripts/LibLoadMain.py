import bge.logic
cont = bge.logic.getCurrentController()
own = cont.owner

#set paths for libload files
playerController = bge.logic.expandPath("//Models\PlayerController.blend")


#load libload files, 'Scene' is the mode argument for LibLoad (I think)
bge.logic.LibLoad(playerController, 'Scene')
