import pygame
import importlib

from map import Map, getAbsPos, getGridCenter
from treecontainer import collide
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
	
	def initNewGame(self,playerData):
		self.unitSet = UnitSet()
		self.units = self.unitSet.units
		
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
			self.update()
	
	def addUnit(self,unit,x,y):
		self.unitSet.addUnit(unit,x,y)
		
	def addUnitGrid(self,unit,col,row):
		self.unitSet.addUnitGrid(unit,col,row)
	
	def removeUnit(self,unit):
		self.unitSet.removeUnit(unit)
	
	def available(self,unit,x,y):
		return self.unitSet.available(unit,x,y)

	def step(self):
		addunitlist = []
		removeunitlist = []
		for unit in self.units:
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
				addunitlist.append(newunit)
				removeunitlist.append(unit)
		for unit in removeunitlist:
			self.removeUnit(unit)
		
		for unit in addunitlist:
			self.addUnit(unit,unit.offsetx,unit.offsety)
	
	def updatePosition(self):
		self.x = self.map.x
		self.y = self.map.y
		for unit in self.units:
			unit.x = self.x + unit.offsetx
			unit.y = self.y + unit.offsety
			
	def update(self):
		self.updatePosition()
		self.step()
	
	def inarea(self,unit):
		x,y = unit.offsetx+self.x,unit.offsety+self.y
		w,h = unit.width(),unit.height()
		return x > -w and y > -h and x < battlewidth and y < battleheight
	
	def draw(self,screen):
		self.updatePosition()
		for unit in self.units:
			if self.inarea(unit):
				unit.draw(screen)
	
	def onMouseDown(self,x,y,button):
		for unit in self.units:
			unit.onMouseDown(x,y,button)
	
	def onMouseUp(self,x,y,button):
		pass
	
	def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
		pass
	
class UnitSet():
	def __init__(self):
		self.units = []
	
	def addUnit(self,unit):
		self.units.append(unit)
		
	def addUnit(self,unit,x,y):
		unit.offsetx, unit.offsety = x,y
		self.units.append(unit)
		
	def addUnitGrid(self,unit,col,row):
		unit.offsetx, unit.offsety = getAbsPos(col,row)
		self.units.append(unit)
		
	def removeUnit(self,unit):
		self.units.remove(unit)
	
	def available(self,unit,x,y):
		for u in self.units:
			if u == unit: continue
			if collide(u.offsetx,u.offsety,u.size,x,y,unit.size):
				return False
		return True
