import pygame
import importlib

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images


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
	def __init__(self,owner,animationset):
		super(Vehicle,self).__init__(owner,animationset)
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
				self.moveTo(x,y)
			else:
				x,y = self.target.offsetx,self.target.offsety
				if dist(self.offsetx,self.offsety,x,y) > self.range:
					self.moveTo(x,y)
		else:
			if self.animation == "expand_%d"%(self.owner) and self.end:
				self.replace = ("building",self.expandInto)
	
	def expand(self):
		self.startAnimation("expand_%d"%(self.owner))
		
class MCV(Vehicle):
	def __init__(self,owner):
		animationset = mcvAnimation
		super(MCV,self).__init__(owner,animationset)
		self.speed = 5
		self.size = 6
		self.range = 0
		self.fullHP = 3000
		self.HP = self.fullHP
		self.expandInto = "AirCmd"
	
	def get_rect(self):
		self.rect.center = (self.x,self.y-20)
		return self.rect
		
	def onDoubleClick(self):
		self.expand()

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
				animation.loop = True
				# animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
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
