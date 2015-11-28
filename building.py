import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *

buildingRect = pygame.Rect(0,0,1,1)
aircmdAnimation = None
gcnstAnimation = None

def initBuildingAnimations():
	global longBuildingHealthBlood, longBuildingHurtBlood,\
           longBuildingDangerBlood, shortBuildingHealthBlood,\
           shortBuildingHurtBlood, shortBuildingDangerBlood
	global aircmdAnimation, gcnstAnimation
	bloodbarimg = images["buildingbloodbar"]
	longBuildingHealthBlood  = bloodbarimg.subsurface(0,0,300,10)
	longBuildingHurtBlood    = bloodbarimg.subsurface(0,10,300,10)
	longBuildingDangerBlood  = bloodbarimg.subsurface(0,20,300,10)
	shortBuildingHealthBlood = bloodbarimg.subsurface(0,0,150,10)
	shortBuildingHurtBlood   = bloodbarimg.subsurface(0,10,150,10)
	shortBuildingDangerBlood = bloodbarimg.subsurface(0,20,150,10)
	aircmdAnimation = AirCmdAnimation()
	gcnstAnimation = GcnstAnimation()

class Building(Unit):
	def __init__(self,owner,animationset):
		super(Building,self).__init__(owner,animationset)
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
	def __init__(self,owner):
		animationset = aircmdAnimation
		super(AirCmd,self).__init__(owner,animationset)
		self.size = sizeofunit["AirCmd"]
		self.fullHP = 1000
		self.HP = self.fullHP
	def drawBloodBar(self,screen):
		self.drawShortBloodBar(screen)
classmap["AirCmd"] = AirCmd
		
class Gcnst(Building):
	def __init__(self,owner):
		animationset = gcnstAnimation
		super(Gcnst,self).__init__(owner,animationset)
		self.size = sizeofunit["Gcnst"]
		self.fullHP = 3000
		self.HP = self.fullHP
	def drawBloodBar(self,screen):
		self.drawLongBloodBar(screen)
classmap["Gcnst"] = Gcnst

class AirCmdAnimation(AnimationSet):
	def __init__(self):
		super(AirCmdAnimation,self).__init__()
		image = images["aircmd"]
		offsetx,offsety = 140,170
		self.originalAnimation = "build"
		self.modifyx = -50
		self.modifyy = 0
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
		offsetx,offsety = 213,263
		self.originalAnimation = "build"
		width,height = 426,339
		owneroffset = 2034
		self.modifyx = 20
		self.modifyy = -20
		
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
