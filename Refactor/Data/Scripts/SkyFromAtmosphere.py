	######################################################
	# changed by HG1 to Blender 2.6x 20.08.2012																										
	######################################################

#	import bge
import math

def runShader(cont):
	#bge.logic.setLogicTicRate(60.0)
	 
	# -------------------------------------
	#cont = bge.logic.getCurrentController()
	own = cont.owner
	objlist = own.scene.objects
	obj = own
	camera = own.scene.active_camera
	lamp = objlist['MainSun']
	target = own.parent
	radius = own.parent.worldScale
	ownPos = own.worldPosition
	objpos = obj.position
	camerapos = (camera.worldPosition - objpos) / radius[0] * obj.worldOrientation
	lightpos = lamp.getAxisVect([0.0,0.0,1.0])
	lightpos.normalize()
	lightpos = lightpos * obj.worldOrientation
	cameraDistance = camerapos.length#/ own.parent.scaling[0]
	lightDistance = 1.0

	m_fOuterRadius = 10.25
	m_fInnerRadius = 10.00

	#xOffset = objpos[0] - camerapos[0]
	#yOffset = objpos[1] - camerapos[1]
	#zOffset = objpos[2] - camerapos[2]
	#dSquared = xOffset**2 + yOffset**2 + zOffset**2
	#cameraDistance = math.sqrt(dSquared)
	#cameraDistanceSq = dSquared

	#xOffset1 =  objpos[0] - lightpos[0]
	#yOffset1 =  objpos[1] - lightpos[1]
	#zOffset1 =  objpos[2] - lightpos[2]
	#dSquared1 = xOffset1**2 + yOffset1**2 + zOffset1**2
	#lightDistance = math.sqrt(dSquared1)

	own["r"] = radius[0]
	own["d"] = cameraDistance#/ own.parent.scaling[0]

	fExposure = own["fExposure"]

	m_ESun = 15.0
	m_Km = 0.0015
	m_Kr = 0.0025

	PI = 3.14159265
	#PI = math.pi

	m_Km4PI = m_Km*4.0*PI
	m_Kr4PI = m_Kr*4.0*PI

	m_fRayleighScaleDepth = 0.25

	m_nSamples = own["samples"]
	 
	MaterialIndexList = [0] # material index
	GlobalAmbient = [0.39,0.35,0.32,1]
	AmbF = 0.5
	# -------------------------------------
	 
	 
	VertexShader = """

	//
	// Atmospheric scattering vertex shader
	//
	// Author: Sean O'Neil
	//
	// Copyright (c) 2004 Sean O'Neil
	//



	uniform vec3 v3CameraPos;	   // The camera's current position
	uniform vec3 v3LightPos;		// The direction vector to the light source
	uniform vec3 m_fWavelength;	 // 1 / pow(wavelength, 4) for the red, green, and blue channels
	uniform float fCameraHeight;	// The camera's current height
	uniform float fCameraHeight2;   // fCameraHeight^2
	uniform float fOuterRadius;	 // The outer (atmosphere) radius
	uniform float fOuterRadius2;	// fOuterRadius^2
	uniform float fInnerRadius;	 // The inner (planetary) radius
	uniform float fInnerRadius2;	// fInnerRadius^2
	uniform float fKrESun;		  // Kr * ESun
	uniform float fKmESun;		  // Km * ESun
	uniform float fKr4PI;		   // Kr * 4 * PI
	uniform float fKm4PI;		   // Km * 4 * PI
	uniform float fScale;		   // 1 / (fOuterRadius - fInnerRadius)
	uniform float fScaleDepth;	  // The scale depth (i.e. the altitude at which the atmosphere's average density is found)
	uniform float fScaleOverScaleDepth; // fScale / fScaleDepth
	//uniform float worldPosX;
	//uniform float worldPosY;
	//uniform float worldPosZ;
	uniform int nSamples;
	uniform float fSamples;



	varying vec3 v3Direction, v, Vert;
	varying float depth;

	float scale(float fCos)
	{
		float x = 1.0 - fCos;
		return fScaleDepth * exp(-0.00287 + x*(0.459 + x*(3.83 + x*(-6.80 + x*5.25))));
	}

	void main(void)
	{

		vec3 v3InvWavelength;
		
		v3InvWavelength.x = 1.0/pow(m_fWavelength.x, 4.0);
		v3InvWavelength.y = 1.0/pow(m_fWavelength.y, 4.0);
		v3InvWavelength.z = 1.0/pow(m_fWavelength.z, 4.0);


		// Get the ray from the camera to the vertex, and its length (which is the far point of the ray passing through the atmosphere)
		vec3 v3Pos = gl_Vertex.xyz; //vec3(worldPosX,worldPosY,worldPosZ) idk
		vec3 v3Ray = v3Pos - v3CameraPos;
		float fFar = length(v3Ray);
		v3Ray /= fFar;

		// Calculate the ray's starting position, then calculate its scattering offset
		vec3 v3Start = v3CameraPos;
		float fHeight = length(v3Start);
		float fDepth = exp(fScaleOverScaleDepth * (fInnerRadius - fCameraHeight));
		float fStartAngle = dot(v3Ray, v3Start) / fHeight;
		float fStartOffset = fDepth*scale(fStartAngle);


		float fStartDepth = exp(fScaleOverScaleDepth * (fInnerRadius - fCameraHeight));
		depth = clamp(fStartDepth*scale(fStartAngle),0.0,1.0);

		// Initialize the scattering loop variables
		//gl_FrontColor = vec4(0.0, 0.0, 0.0, 0.0);
		float fSampleLength = fFar / fSamples;
		float fScaledLength = fSampleLength * fScale;
		vec3 v3SampleRay = v3Ray * fSampleLength;
		vec3 v3SamplePoint = v3Start + v3SampleRay * 0.5;

		// Now loop through the sample rays
		vec3 v3FrontColor = vec3(0.0, 0.0, 0.0);
		vec3 v3Attenuate = vec3(0.0, 0.0, 0.0);
		for(int i=0; i<nSamples; i++)
		{
			float fHeight = length(v3SamplePoint);
			float fDepth = exp(fScaleOverScaleDepth * (fInnerRadius - fHeight));
			float fLightAngle = dot(v3LightPos, v3SamplePoint) / fHeight;
			float fCameraAngle = dot(v3Ray, v3SamplePoint) / fHeight;
			float fScatter = (fStartOffset + fDepth*(scale(fLightAngle) - scale(fCameraAngle)));
			vec3 v3Attenuate = exp(-fScatter * (v3InvWavelength * fKr4PI + fKm4PI));
			v3FrontColor += v3Attenuate * (fDepth * fScaledLength);
			v3SamplePoint += v3SampleRay;
		}

		// Finally, scale the Mie and Rayleigh colors and set up the varying variables for the pixel shader
		gl_FrontSecondaryColor.rgb = v3FrontColor * fKmESun;
		gl_FrontColor.rgb = v3FrontColor * (v3InvWavelength * fKrESun);
		gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
		v3Direction = v3CameraPos - v3Pos;
	}

	"""
	 
	 
	 
	FragmentShader = """

	//
	// Atmospheric scattering fragment shader
	//
	// Author: Sean O'Neil
	//
	// Copyright (c) 2004 Sean O'Neil
	//

	uniform vec3 v3LightPos;
	const float g = -0.98;
	const float g2 = (-0.98)*(-0.98);

	uniform float fCameraHeight, fOuterRadius, fScaleDepth;
	uniform float fExposure;
	varying vec3 v3Direction;
	varying float depth;

	void main (void)
	{

		float fCos = dot(v3LightPos, v3Direction) / length(v3Direction);
		float fRayleighPhase = 0.75 * (1.0 + (fCos*fCos));
		float fMiePhase = 1.5 * ((1.0 - g2) / (2.0 + g2)) * (1.0 + fCos*fCos) / pow(1.0 + g2 - 2.0*g*fCos, 1.5);
		
		float sun = 2.0*((1.0 - 0.2) / (2.0 + 0.2)) * (1.0 + fCos*fCos) / pow(1.0 + 0.2 - 2.0*(-0.2)*fCos, 1.0);
		
		vec4 f4Ambient = (sun * depth + (fOuterRadius - fCameraHeight))*vec4(0.05, 0.05, 0.1,1.0);
		
		vec4 f4Color = (fRayleighPhase * gl_Color + fMiePhase * gl_SecondaryColor)+f4Ambient;
		vec4 HDR = 1.0 - exp(f4Color * -fExposure);
		float nightmult = clamp(max(HDR.x, max(HDR.y, HDR.z))*1.5,0.0,1.0);

		//gl_FragColor = vec4(ambient);
		gl_FragColor = HDR;
		gl_FragColor.a = nightmult+(fOuterRadius - fCameraHeight);

	}
	"""
	 
	 
	 
	mesh = own.meshes[0]
	for mat in mesh.materials:
		shader = mat.getShader()
		if shader != None:
			if not shader.isValid():
				shader.setSource(VertexShader, FragmentShader, 1)
			shader.setUniform3f('v3CameraPos',camerapos[0],camerapos[1], camerapos[2])
			shader.setUniform3f('v3LightPos', (lightpos[0])/lightDistance, (lightpos[1])/lightDistance, (lightpos[2])/lightDistance)
			shader.setUniform3f('m_fWavelength', own.parent["R"], own.parent["G"], own.parent["B"])
			shader.setUniform1f('fCameraHeight', cameraDistance)
			#shader.setUniform1f('fCameraHeight2', cameraDistance*cameraDistance)
			shader.setUniform1f('fInnerRadius', m_fInnerRadius);
			#shader.setUniform1f('fInnerRadius2', m_fInnerRadius*m_fInnerRadius)
			shader.setUniform1f('fOuterRadius', m_fOuterRadius)
			#shader.setUniform1f('fOuterRadius2', m_fOuterRadius*m_fOuterRadius)
			shader.setUniform1f('fKrESun', m_Kr*m_ESun)
			shader.setUniform1f('fKmESun', m_Km*m_ESun)
			shader.setUniform1f('fKr4PI', m_Kr4PI)
			shader.setUniform1f('fKm4PI', m_Km4PI)
			shader.setUniform1f('fScale',1.0 / (m_fOuterRadius - m_fInnerRadius))
			shader.setUniform1f('fScaleDepth', m_fRayleighScaleDepth)
			shader.setUniform1f('fScaleOverScaleDepth',(1.0 / (m_fOuterRadius - m_fInnerRadius))/ m_fRayleighScaleDepth)
			shader.setUniform1f('fExposure', fExposure)
			shader.setUniform1i("nSamples", m_nSamples)
			shader.setUniform1f("fSamples", m_nSamples)
			#vec3 v3Pos = vec3(worldPosX,worldPosY,worldPosZ);
			#shader.setUniform1f("worldPosX", target.worldPosition[0])
		#	shader.setUniform1f("worldPosY", target.worldPosition[1])
		#	shader.setUniform1f("worldPosZ", target.worldPosition[2])