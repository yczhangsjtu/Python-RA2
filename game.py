import pygame
import importlib

from map import Map, getAbsPos, getGridCenter
from treecontainer import collide, TreeContainer
from unit import Unit
from vehicle import *
from infantry import *
from building import *
from consts import *

class Game():
	def __init__(self,map):
		self.map = map
		self.unitSet = None
		self.x = map.x
		self.y = map.y
		self.running = False
	
	def initNewGame(self,playerData):
		self.unitSet = TreeContainer(0,0,self.map.groundwidth,self.map.groundheight)
		self.running = False
		
		for player in playerData:
			data = playerData[player]
			flag = data["flag"]
			col,row = data["position"]
			mcv = MCV(flag)
			self.addUnitGrid(mcv,col,row)
			for unitdata in data["initials"]:
				name = unitdata["name"]
				type = unitdata["type"]
				x,y = unitdata["pos"]
				x,y = x+mcv.offsetx,y+mcv.offsety
				self.addUnit(getattr(importlib.import_module(type),name)(flag),x,y)
		self.updatePosition()
	
	def addUnit(self,unit,x,y):
		self.unitSet.addPos(unit,x,y)
		
	def addUnitGrid(self,unit,col,row):
		self.unitSet.addGrid(unit,col,row)
	
	def removeUnit(self,unit):
		self.unitSet.remove(unit)
	
	def available(self,unit,x,y):
		return self.unitSet.available(unit,x,y)

	def step(self):
		unitlist = []
		for unit in self.unitSet:
			unitlist.append(unit)
		for unit in unitlist:
			unit.step(self.map,self)
			if hasattr(unit,"replace") and unit.replace != None:
				type = unit.replace[0]
				name = unit.replace[1]
				newunit = getattr(importlib.import_module(type),name)(unit.owner)
				newunit.HP = unit.HP
				newunit.fullHP = unit.fullHP
				if type == "building":
					unit.offsetx,unit.offsety = getGridCenter(unit.offsetx,unit.offsety)
				newunit.offsetx = unit.offsetx + newunit.animationset.modifyx
				newunit.offsety = unit.offsety + newunit.animationset.modifyy
				self.removeUnit(unit)
				self.addUnit(newunit,newunit.offsetx,newunit.offsety)
	
	def updatePosition(self):
		self.x = self.map.x
		self.y = self.map.y
		for unit in self.unitSet:
			unit.x = self.x + unit.offsetx
			unit.y = self.y + unit.offsety
			
	def update(self):
		self.updatePosition()
		if self.running:
			self.step()
	
	def inarea(self,unit):
		rect = unit.get_rect().copy()
		center = rect.center
		rect.width *= 3
		rect.height *= 3
		rect.center = center
		return rect.colliderect(pygame.Rect(0,0,battlewidth,battleheight))
	
	def draw(self,screen):
		self.updatePosition()
		for unit in self.unitSet:
			if self.inarea(unit):
				unit.draw(screen)
	
	def onMouseDown(self,x,y,button):
		for unit in self.unitSet:
			unit.onMouseDown(x,y,button)
	
	def onMouseUp(self,x,y,button):
		pass
	
	def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
		pass
