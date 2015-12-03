import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *

buildingRect = pygame.Rect(0,0,1,1)
aircmdAnimation = None
gcnstAnimation = None
powerAnimation = None
gpileAnimation = None

def initBuildingAnimations():
	global longBuildingHealthBlood, longBuildingHurtBlood,\
           longBuildingDangerBlood, shortBuildingHealthBlood,\
           shortBuildingHurtBlood, shortBuildingDangerBlood
	global aircmdAnimation, gcnstAnimation, powerAnimation, gpileAnimation
	bloodbarimg = images["buildingbloodbar"]
	longBuildingHealthBlood  = bloodbarimg.subsurface(0,0,300,10)
	longBuildingHurtBlood    = bloodbarimg.subsurface(0,10,300,10)
	longBuildingDangerBlood  = bloodbarimg.subsurface(0,20,300,10)
	shortBuildingHealthBlood = bloodbarimg.subsurface(0,0,150,10)
	shortBuildingHurtBlood   = bloodbarimg.subsurface(0,10,150,10)
	shortBuildingDangerBlood = bloodbarimg.subsurface(0,20,150,10)
	aircmdAnimation = AirCmdAnimation()
	gcnstAnimation = GcnstAnimation()
	powerAnimation = PowerAnimation()
	gpileAnimation = GpileAnimation()

class Building(Unit):
	def __init__(self,player,animationset,animation=None):
		super(Building,self).__init__(player,animationset,animation)
		self.rect = buildingRect
		self.modifyx = 0
		self.modifyy = 0
		self.regionselectable = False
	
	def get_rect(self):
		self.rect.width = self.size * 8
		self.rect.height = self.size * 4
		self.rect.center = (self.x,self.y)
		return self.rect
	
	def drawLongBloodBar(self,screen):
		offsetx,offsety = 200,200
		rotate = 30
		if self.HP >= self.fullHP/2:
			ngrid = self.HP * 30 / self.fullHP
			blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
		elif self.HP >= self.fullHP/4:
			ngrid = self.HP * 30 / self.fullHP
			blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
		else:
			ngrid = self.HP * 30 / self.fullHP
			blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
	def drawShortBloodBar(self,screen):
		offsetx,offsety = 100,150
		rotate = 30
		if self.HP >= self.fullHP/2:
			ngrid = self.HP * 15 / self.fullHP
			blood = shortBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
		elif self.HP >= self.fullHP/4:
			ngrid = self.HP * 15 / self.fullHP
			blood = shortBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
		else:
			ngrid = self.HP * 15 / self.fullHP
			blood = shortBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
			screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))

class AirCmd(Building):
	def __init__(self,player,animation=None):
		animationset = aircmdAnimation
		super(AirCmd,self).__init__(player,animationset,animation)
		self.size = sizeofunit["AirCmd"]
		self.fullHP = 1000
		self.HP = self.fullHP
		self.name = "AirCmd"
	def drawBloodBar(self,screen):
		self.drawShortBloodBar(screen)
classmap["AirCmd"] = AirCmd

class Power(Building):
	def __init__(self,player,animation=None):
		animationset = powerAnimation
		super(Power,self).__init__(player,animationset,animation)
		self.size = sizeofunit["Power"]
		self.fullHP = 1000
		self.HP = self.fullHP
		self.name = "Power"
	def drawBloodBar(self,screen):
		self.drawShortBloodBar(screen)
classmap["Power"] = Power
		
class Gcnst(Building):
	def __init__(self,player,animation=None):
		animationset = gcnstAnimation
		super(Gcnst,self).__init__(player,animationset,animation)
		self.size = sizeofunit["Gcnst"]
		self.fullHP = 3000
		self.HP = self.fullHP
		self.name = "Gcnst"
	def drawBloodBar(self,screen):
		self.drawLongBloodBar(screen)
classmap["Gcnst"] = Gcnst
		
class Gpile(Building):
	def __init__(self,player,animation=None):
		animationset = gpileAnimation
		super(Gpile,self).__init__(player,animationset,animation)
		self.size = sizeofunit["Gpile"]
		self.fullHP = 1000
		self.HP = self.fullHP
		self.name = "Gpile"
	def drawBloodBar(self,screen):
		self.drawLongBloodBar(screen)
classmap["Gpile"] = Gpile

class PowerAnimation(AnimationSet):
	def __init__(self):
		super(PowerAnimation,self).__init__()
		image = images["power"]
		offsetx,offsety = 99,132
		self.originalAnimation = "build"
		width,height = 213,165
		playeroffset = 330
		
		x,y,m,n = 0,165,25,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%player,animation)
			y += playeroffset
		
		x,y,m,n = 0,0,8,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%player,animation)
			self.getAnimation("build_%d"%player).next = animation
			y += playeroffset
		
		x,y,m,n = 1704,0,8,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%player,animation)
			y += playeroffset

class GpileAnimation(AnimationSet):
	def __init__(self):
		super(GpileAnimation,self).__init__()
		image = images["gpile"]
		offsetx,offsety = 209,161
		self.originalAnimation = "build"
		width,height = 375,222
		playeroffset = 666
		
		x,y,m,n = 0,444,25,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%player,animation)
			y += playeroffset
		
		x,y,m,n = 0,0,8,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%player,animation)
			self.getAnimation("build_%d"%player).next = animation
			y += playeroffset
		
		x,y,m,n = 0,222,8,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%player,animation)
			y += playeroffset

class AirCmdAnimation(AnimationSet):
	def __init__(self):
		super(AirCmdAnimation,self).__init__()
		image = images["aircmd"]
		offsetx,offsety = 140,170
		self.originalAnimation = "build"
		width,height = 282,243
		playeroffset = 486
		
		x,y,m,n = 0,243,25,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%player,animation)
			y += playeroffset
		
		x,y,m,n = 0,0,6,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%player,animation)
			self.getAnimation("build_%d"%player).next = animation
			y += playeroffset
		
		x,y,m,n = 1692,0,6,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%player,animation)
			y += playeroffset
			
class GcnstAnimation(AnimationSet):
	def __init__(self):
		super(GcnstAnimation,self).__init__()
		image = images["gcnst"]
		offsetx,offsety = 213,263
		self.originalAnimation = "build"
		width,height = 426,339
		playeroffset = 1356
		
		x,y,i0,j0,left,right,count = 0,678,0,0,0,20,29
		for player in range(numofplayer):
			animation = Animation()
			animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
			animation.loop = False
			self.addAnimation("build_%d"%player,animation)
			y += playeroffset
		
		x,y,m,n = 0,0,20,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("normal_%d"%player,animation)
			self.getAnimation("build_%d"%player).next = animation
			y += playeroffset
		
		x,y,m,n = 0,339,20,1
		for player in range(numofplayer):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			self.addAnimation("destroy_%d"%player,animation)
			y += playeroffset
