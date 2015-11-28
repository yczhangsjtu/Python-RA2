import pygame

from unit import Unit
from map import getAbsPos, getGridPos, getGridCenter
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *


vehicleRect = pygame.Rect(0,0,100,50)
mcvAnimation = None
directions = ["n","nw","w","sw","s","se","e","ne"]

def initVehicleAnimations():
	global bloodbarimg, vehicleHealthBlood, vehicleHurtBlood, vehicleDangerBlood
	global mcvAnimation
	bloodbarimg = images["bloodbar"]
	vehicleHealthBlood = bloodbarimg.subsurface(0,0,73,5)
	vehicleHurtBlood = bloodbarimg.subsurface(0,4,73,5)
	vehicleDangerBlood = bloodbarimg.subsurface(0,8,73,5)
	mcvAnimation = MCVAnimation()

class Vehicle(Unit):
	def __init__(self,owner,animationset,animation=None):
		super(Vehicle,self).__init__(owner,animationset,animation)
		self.expandInto = None
		self.replace = None
		self.rect = vehicleRect
	
	def get_rect(self):
		self.rect.center = (self.x,self.y)
		return self.rect
	
	def drawBloodBar(self,screen):
		if self.HP >= self.fullHP/2:
			ngrid = self.HP * 24 / self.fullHP
			screen.blit(vehicleHealthBlood.subsurface(0,0,ngrid*3+1,5),(self.x-36,self.y-50))
		elif self.HP >= self.fullHP/4:
			ngrid = self.HP * 24 / self.fullHP
			screen.blit(vehicleHurtBlood.subsurface(0,0,ngrid*3+1,5),(self.x-36,self.y-50))
		else:
			ngrid = self.HP * 24 / self.fullHP
			screen.blit(vehicleDangerBlood.subsurface(0,0,ngrid*3+1,5),(self.x-36,self.y-50))
			
	def step(self,map,characters):
		super(Vehicle,self).step(map,characters)
		if self.target != None:
			if isinstance(self.target,tuple):
				x,y = self.target
				self.moveTo(x,y,characters)
			else:
				x,y = self.target.offsetx,self.target.offsety
				if dist(self.offsetx,self.offsety,x,y) > self.range:
					self.moveTo(x,y,characters)
		else:
			if self.animation == "expand_%d"%(self.owner) and self.end:
				oldsize = self.size
				self.size = sizeofunit[self.expandInto]
				offsetx,offsety = getGridCenter(self.offsetx,self.offsety)
				offsetx += modify[self.expandInto][0]
				offsety += modify[self.expandInto][1]
				if characters.unitSet.available(self,offsetx,offsety):
					self.replace = self.expandInto
				else:
					self.size = oldsize
	
	def expand(self):
		oldsize = self.size
		self.size = sizeofunit[self.expandInto]
		offsetx,offsety = getGridCenter(self.offsetx,self.offsety)
		offsetx += modify[self.expandInto][0]
		offsety += modify[self.expandInto][1]
		container = self.container.getTopContainer()
		if container.available(self,offsetx,offsety):
			self.startAnimation("expand_%d"%(self.owner))
		self.size = oldsize
		
class MCV(Vehicle):
	def __init__(self,owner,animation=None):
		animationset = mcvAnimation
		super(MCV,self).__init__(owner,animationset,animation)
		self.speed = 5
		self.size = sizeofunit["MCV"]
		self.range = 0
		self.fullHP = 3000
		self.HP = self.fullHP
		self.expandInto = "Gcnst"
	
	def get_rect(self):
		self.rect.center = (self.x,self.y-20)
		return self.rect
		
	def onDoubleClick(self):
		self.expand()
classmap["MCV"] = MCV

class MCVAnimation(AnimationSet):
	def __init__(self):
		super(MCVAnimation,self).__init__()
		image = images["mcv"]
		offsetx,offsety = 94,77
		self.originalAnimation = "standne"
		width,height = 188,154
		owneroffset = 154
		
		y,m,n = 0,1,1
		for owner in range(2):
			x = 0
			for direction in ["w","sw","s","se","e","ne","n","nw"]:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				self.addAnimation("stand%s_%d"%(direction,owner),animation)
				x += width * m * 2
			y += owneroffset
		
		y,m,n = 0,1,1
		for owner in range(2):
			x = 0
			for direction in ["w","sw","s","se","e","ne","n","nw"]:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("run%s_%d"%(direction,owner),animation)
				x += width * m * 2
			y += owneroffset
		
		x,y,m,n = 0,0,16,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("expand_%d"%(owner),animation)
			y += owneroffset
