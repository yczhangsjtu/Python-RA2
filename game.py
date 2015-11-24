from pylash.display import Sprite
from pylash.events import MouseEvent

from map import Map
from unit import Unit

class Game():
	def __init__(self,map,charLayer):
		self.map = map
		self.unitSet = None
		self.characterLayer = charLayer
	
	def initNewGame(self,dataList):
		self.unitSet = UnitSet()
		self.characterLayer.addChild(self.unitSet)
		self.unitSet.addUnit(Unit("mcv",0,dataList),5,5)
		self.unitSet.addUnit(Unit("adog",1,dataList),8,5)
		self.unitSet.show(0)
		self.unitSet.show(1)
	
	def onMouseDown(self,e):
		pass
	
	def onMouseUp(self,e):
		pass
	
	def onMouseMove(self,e):
		pass
	
class UnitSet(Sprite):
	def __init__(self):
		super(UnitSet,self).__init__()
		self.units = []
	
	def addUnit(self,unit):
		self.units.append(unit)
		
	def addUnit(self,unit,col,row):
		unit.x, unit.y = Map.getAbsPos(col,row)
		self.units.append(unit)
		
	def removeUnit(self,unit):
		self.hide(unit)
		self.units.remove(unit)
		
	def show(self,index):
		if index >= 0 and index < len(self.units):
			self.addChild(self.units[index])
	
	def hide(self,unit):
		if unit.parent != None:
			building.remove()
				
	def hide(self,index):
		if index >= 0 and index < len(self.units):
			self.hide(self.units[index])