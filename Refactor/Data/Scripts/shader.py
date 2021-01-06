# This script grab the shader text from the the Filter2D actuator,
# this way we can have code high lighting for the GLSL shader.
from bge import logic, render
#from bgl import *

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
own = cont.owner
bufA = scene.filterManager.addFilter(0, logic.RAS_2DFILTER_CUSTOMFILTER, cont.actuators["BufferA"].shaderText)
if 'ran' not in own:
    own['ran']=True
    own["iFrame"] = -1

    
    bufA.addOffScreen(1, hdr=render.HDR_FULL_FLOAT)
    image = scene.filterManager.addFilter(2, logic.RAS_2DFILTER_CUSTOMFILTER, cont.actuators["Image"].shaderText)

    def run(cont):
    	own = cont.owner

    	if (own["iFrame"] >= 0):
     
    		# Setup textures 
    #		id = bufA.offScreen.colorBindCodes[0]
    #		glBindTexture(GL_TEXTURE_2D, id)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            image.setTexture(0, bufA.offScreen.colorBindCodes[0], "iChannel0")
                   
    		# Setup textures 
    #		id = bufA.offScreen.colorBindCodes[0]
    #		glBindTexture(GL_TEXTURE_2D, id)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    #		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            bufA.setTexture(1, bufA.offScreen.colorBindCodes[0], "iChannel0")
                    
            
    	       
    	own["iFrame"] += 1
