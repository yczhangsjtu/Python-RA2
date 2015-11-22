from map import Map
from pylash.display import Sprite

class Game():
	def __init__(self,map):
		self.map = map
		self.unitSet = UnitSet(BuildingSet(),InfantrySet(),VehicleSet())
	
class UnitSet():
	def __init__(self,bset,iset,vset):
		self.buildingSet = bset
		self.infantrySet = iset
		self.vehicleSet = vset
		self.sprite = Sprite()
		self.sprite.addChild(bset.sprite)
		self.sprite.addChild(iset.sprite)
		self.sprite.addChild(vset.sprite)

class BuildingSet():
	def __init__(self):
		self.sprite = Sprite()
		self.buildings = []

class InfantrySet():
	def __init__(self):
		self.sprite = Sprite()
		self.infantries = []
		
class VehicleSet():
	def __init__(self):
		self.sprite = Sprite()
		self.vehicles = []
	