import pygame
from random import choice

from map import getGridCenter
from animation import Animation, AnimationSet
from consts import *
from data import images

directions = ["nw","w","sw","s","se","e","ne","n"]

def dist(x1,y1,x2,y2):
	return abs(x1-x2)+abs(y1-y2)
	
class Unit(object):
	def __init__(self,owner,animationset):
		self.owner = owner
		self.animationset = animationset
		self.animation = "%s_%d"%(animationset.originalAnimation,owner)
		self.index = 0
		self.selected = False
		self.target = None
		self.rect = pygame.Rect(0,0,1,1)
		self.land = True
		self.water = False
		self.air = False
		self.HP = 0
		self.selectable = True
		self.regionselectable = True
		self.x = 0
		self.y = 0
	
	def drawArea(self,screen):
		pointlist = [(self.x+self.size*8,self.y)]
		pointlist.append((self.x,self.y-self.size*4))
		pointlist.append((self.x-self.size*8,self.y))
		pointlist.append((self.x,self.y+self.size*4))
		pygame.draw.polygon(screen,WHITE,pointlist)
	
	def draw(self,screen):
		self.drawArea(screen)
		self.animationset.setState(self.animation,self.index)
		self.animationset.setpos(self.x,self.y)
		self.animationset.draw(screen)
		if self.selected:
			self.drawBloodBar(screen)
	
	def drawBloodBar(self,screen):
		pass
	
	def get_rect(self):
		self.rect.centerx = self.x
		self.rect.bottom = self.y
		return self.rect
	
	def step(self,map,characters):
		self.animation,self.index = self.animationset.step(self.animation,self.index)
		self.end = self.animationset.end
		offsetx,offsety = self.offsetx,self.offsety
		if self.animation == "rune_%d"%(self.owner):
			offsetx += self.speed
		if self.animation == "runw_%d"%(self.owner):
			offsetx -= self.speed
		if self.animation == "runn_%d"%(self.owner):
			offsety -= self.speed
		if self.animation == "runs_%d"%(self.owner):
			offsety += self.speed
		if self.animation == "runne_%d"%(self.owner):
			offsetx += self.speed*2/3
			offsety -= self.speed/3
		if self.animation == "runnw_%d"%(self.owner):
			offsetx -= self.speed*2/3
			offsety -= self.speed/3
		if self.animation == "runse_%d"%(self.owner):
			offsetx += self.speed*2/3
			offsety += self.speed/3
		if self.animation == "runsw_%d"%(self.owner):
			offsetx -= self.speed*2/3
			offsety += self.speed/3

		if self.offsetx != offsetx or self.offsety != offsety:
			success = False
			if map.island(offsetx,offsety) and self.land or\
			   map.iswater(offsetx,offsety) and self.water:
				success = characters.unitSet.move(self,offsetx,offsety)
			if not success:
				self.setStopAnimation()
	
	def startAnimation(self,animation):
		if not self.end: #self.animation == animation:
				return
		self.animation,self.index = animation,0
			
	def moveTo(self,x,y,characters):
		if dist(self.offsetx,self.offsety,x,y) < 2*self.speed:
			characters.unitSet.move(self,x,y)
			self.stop()
		else:
			corner = None
			directx = None
			directy = None
			if x > self.offsetx + self.speed:
				directx = self.moveRight
			elif x < self.offsetx - self.speed:
				directx = self.moveLeft
			if y > self.offsety + self.speed:
				directy = self.moveDown
				if directx == self.moveLeft:
					corner = self.moveDownLeft
				elif directx == self.moveRight:
					corner = self.moveDownRight
			elif y < self.offsety - self.speed:
				directy = self.moveUp
				if directx == self.moveLeft:
					corner = self.moveUpLeft
				elif directx == self.moveRight:
					corner = self.moveUpRight
			if corner == None and directx == None and directy == None:
				characters.unitSet.move(self,x,y)
				self.stop()
			elif directx == None:
				directy()
			elif directy == None:
				directx()
			else:
				ratioxy = abs(self.offsetx-x)/abs(self.offsety-y)
				ratioyx = abs(self.offsety-y)/abs(self.offsetx-x)
				if ratioxy > 2:
					directx()
				elif ratioyx > 2:
					directy()
				else:
					corner()
				
	def moveRight(self):
		self.startAnimation("rune_%d"%(self.owner))
	def moveLeft(self):
		self.startAnimation("runw_%d"%(self.owner))
	def moveDown(self):
		self.startAnimation("runs_%d"%(self.owner))
	def moveUp(self):
		self.startAnimation("runn_%d"%(self.owner))
	def moveDownRight(self):
		self.startAnimation("runse_%d"%(self.owner))
	def moveDownLeft(self):
		self.startAnimation("runsw_%d"%(self.owner))
	def moveUpRight(self):
		self.startAnimation("runne_%d"%(self.owner))
	def moveUpLeft(self):
		self.startAnimation("runnw_%d"%(self.owner))
	
	def setStopAnimation(self):
		for direction in directions:
			if self.animation == "run%s_%d"%(direction,self.owner) or\
				self.animation == "crawl%s_%d"%(direction,self.owner):
				self.startAnimation("stand%s_%d"%(direction,self.owner))
	def stop(self):
		self.setStopAnimation()
		if self.target != None and isinstance(self.target,tuple):
			self.target = None
		return
	
	def onMouseDown(self,x,y,button):
		rect = self.get_rect()
		if button == 1:
			if rect.contains(pygame.Rect(x,y,1,1)):
				if self.selected:
					self.onDoubleClick()
				if self.selectable:
					self.selected = True
			else:
				self.selected = False
		elif button == 3:
			if self.selected:
				self.target = (self.offsetx+(x-self.x),self.offsety+(y-self.y))
		
	def onMouseUp(self,x,y,button):
		pass
		
	def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
		pass
	
	def onDoubleClick(self):
		pass
	
	def width(self):
		return self.get_rect().width
	def height(self):
		return self.get_rect().height
