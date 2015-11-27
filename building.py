import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images

aircmdAnimation = None
gcnstAnimation = None

def initBuildingAnimations():
	global aircmdAnimation, gcnstAnimation
	aircmdAnimation = AirCmdAnimation()
	gcnstAnimation = GcnstAnimation()

class Building(Unit):
	def __init__(self,owner,animationset):
		super(Building,self).__init__(owner,animationset)

class AirCmd(Building):
	def __init__(self,owner):
		animationset = aircmdAnimation
		super(AirCmd,self).__init__(owner,animationset)
		self.size = 3
		self.fullHP = 1000
		self.HP = self.fullHP
		
class Gcnst(Building):
	def __init__(self,owner):
		animationset = gcnstAnimation
		super(Gcnst,self).__init__(owner,animationset)
		self.size = 4
		self.fullHP = 3000
		self.HP = self.fullHP

class AirCmdAnimation(AnimationSet):
	def __init__(self):
		super(AirCmdAnimation,self).__init__()
		image = images["aircmd"]
		offsetx,offsety = 91,171
		self.originalAnimation = "build"
		width,height = 282,243
		owneroffset = 486
		
		x,y,m,n = 0,243,25,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%owner,animation)
			y += owneroffset
		
		x,y,m,n = 0,0,6,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%owner,animation)
			self.getAnimation("build_%d"%owner).next = animation
			y += owneroffset
		
		x,y,m,n = 1692,0,6,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%owner,animation)
			y += owneroffset
			
class GcnstAnimation(AnimationSet):
	def __init__(self):
		super(GcnstAnimation,self).__init__()
		image = images["gcnst"]
		offsetx,offsety = 198,234
		self.originalAnimation = "build"
		width,height = 426,339
		owneroffset = 2034
		
		x,y,i0,j0,left,right,count = 0,1356,0,0,0,20,29
		for owner in range(2):
			animation = Animation()
			animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%owner,animation)
			y += owneroffset
		
		x,y,m,n = 0,0,20,2
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%owner,animation)
			self.getAnimation("build_%d"%owner).next = animation
			y += owneroffset
		
		x,y,m,n = 0,678,20,2
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%owner,animation)
			y += owneroffset