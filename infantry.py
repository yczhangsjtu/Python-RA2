import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images


e3Animation = None
adogAnimation = None
directions = ["n","wn","w","sw","s","se","e","ne"]

	
def initInfantryAnimations():
	global bloodbarimg, infantryHealthBlood, infantryHurtBlood, infantryDangerBlood
	global e3Animation, adogAnimation
	bloodbarimg = images["bloodbar"]
	infantryHealthBlood = bloodbarimg.subsurface(0,0,25,5)
	infantryHurtBlood = bloodbarimg.subsurface(0,4,25,5)
	infantryDangerBlood = bloodbarimg.subsurface(0,8,25,5)
	e3Animation = E3Animation()
	adogAnimation = AdogAnimation()

class Infantry(Unit):
	def __init__(self,owner,animationset):
		super(Infantry,self).__init__(owner,animationset)
	
	def drawBloodBar(self,screen):
		if self.HP >= self.fullHP/2:
			ngrid = self.HP * 8 / self.fullHP
			screen.blit(infantryHealthBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
		elif self.HP >= self.fullHP/4:
			ngrid = self.HP * 8 / self.fullHP
			screen.blit(infantryHurtBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
		else:
			ngrid = self.HP * 8 / self.fullHP
			screen.blit(infantryDangerBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
	
	def step(self):
		super(Infantry,self).step()
		if self.target != None:
			if isinstance(self.target,tuple):
				x,y = self.target
				self.moveTo(x,y)
			else:
				x,y = self.target.offsetx,self.target.offsety
				if dist(self.offsetx,self.offsety,x,y) > self.range:
					self.moveTo(x,y)
		
		
class Adog(Infantry):
	def __init__(self,owner):
		animationset = adogAnimation
		super(Adog,self).__init__(owner,animationset)
		self.speed = 10
		self.size = 1
		self.range = 0
		self.fullHP = 100
		self.HP = self.fullHP

class E3(Infantry):
	def __init__(self,owner):
		animationset = e3Animation
		super(E3,self).__init__(owner,animationset)
		self.speed = 4
		self.size = 1
		self.range = 100
		self.fullHP = 100
		self.HP = self.fullHP

class E3Animation(AnimationSet):
	def __init__(self):
		super(E3Animation,self).__init__()
		image = images["E3"]
		offsetx,offsety = 57,37
		self.originalAnimation = "runsw"
		width,height = 118,72
		owneroffset = 504
		
		y,m,n = 0,1,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				self.addAnimation("stand%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		y,m,n = 216,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("run%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
			
		y,m,n = 288,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("crawl%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		y,m,n = 360,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("attack%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
			
		y,m,n = 432,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("crawlattack%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		x,y,m,n = 1110,72,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			animation.next = self.getAnimation("standsw_%d"%(owner))
			self.addAnimation("cheer_%d"%(owner),animation)
			y += owneroffset
			
		x,y,m,n = 0,72,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			animation.next = self.getAnimation("standsw_%d"%(owner))
			self.addAnimation("squeez_%d"%(owner),animation)
			y += owneroffset
		
		x,y,m,n = 2220,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("die1_%d"%(owner),animation)
			y += owneroffset
			
		x,y,m,n = 3330,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("die2_%d"%(owner),animation)
			y += owneroffset
			
class AdogAnimation(AnimationSet):
	def __init__(self):
		super(AdogAnimation,self).__init__()
		image = images["adog"]
		offsetx,offsety = 36,27
		self.originalAnimation = "runsw"
		width,height = 74,72
		owneroffset = 288
		
		y,m,n = 0,1,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				self.addAnimation("stand%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		y,m,n = 72,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("run%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		y,m,n = 216,6,1
		for owner in range(2):
			x = 0
			for direction in directions:
				animation = Animation()
				animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
				animation.loop = False
				animation.next = self.getAnimation("stand%s_%d"%(direction,owner))
				self.addAnimation("attack%s_%d"%(direction,owner),animation)
				x += width * m
			y += owneroffset
		
		x,y,m,n = 0,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			animation.next = self.getAnimation("standsw_%d"%(owner))
			self.addAnimation("tail_%d"%(owner),animation)
			y += owneroffset
			
		x,y,m,n = 1110,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			animation.next = self.getAnimation("standsw_%d"%(owner))
			self.addAnimation("squeez_%d"%(owner),animation)
			y += owneroffset
		
		x,y,m,n = 2220,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("die1_%d"%(owner),animation)
			y += owneroffset
			
		x,y,m,n = 3330,144,15,1
		for owner in range(2):
			animation = Animation()
			animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
			animation.loop = False
			self.addAnimation("die2_%d"%(owner),animation)
			y += owneroffset
			