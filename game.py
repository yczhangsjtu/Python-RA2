import pygame
from sets import Set

from map import Map, getAbsPos, getGridCenter
from treecontainer import collide, TreeContainer
from data import classmap
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
        self.players = []
    
    def initNewGame(self,playerData):
        self.unitSet = TreeContainer(10,10,self.map.groundwidth-20,self.map.groundheight-20)
        self.running = False
        self.players = [Player(i) for i in range(2)]
        for player in self.players:
            player.money = 10000
        
        for player in playerData:
            data = playerData[player]
            flag = data["flag"]
            col,row = data["position"]
            mcv = MCV(flag)
            self.addUnitGrid(mcv,col,row)
            for unitdata in data["initials"]:
                name = unitdata["name"]
                x,y = unitdata["pos"]
                animation = unitdata["animation"]
                x,y = x+mcv.offsetx,y+mcv.offsety
                self.addUnit(classmap[name](flag,animation),x,y)
        self.updatePosition()
    
    def addUnit(self,unit,x,y):
        self.unitSet.addPos(unit,x,y)
        self.players[unit.player].addUnit(unit)
        
    def addUnitGrid(self,unit,col,row):
        self.unitSet.addGrid(unit,col,row)
        self.players[unit.player].addUnit(unit)
    
    def removeUnit(self,unit):
        self.unitSet.remove(unit)
        self.players[unit.player].removeUnit(unit)
    
    def available(self,unit,x,y):
        return self.unitSet.available(unit,x,y)

    def step(self):
        unitlist = []
        for unit in self.unitSet:
            unitlist.append(unit)
        for unit in unitlist:
            unit.step(self.map,self)
            if hasattr(unit,"replace") and unit.replace != None:
                name = unit.replace
                newunit = classmap[name](unit.player)
                newunit.HP = unit.HP
                newunit.fullHP = unit.fullHP
                if isinstance(newunit,Building):
                    offsetx,offsety = getGridCenter(unit.offsetx,unit.offsety)
                offsetx += modify[name][0]
                offsety += modify[name][1]
                self.removeUnit(unit)
                self.addUnit(newunit,offsetx,offsety)
    
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
    
    def get_battle_rect():
        return pygame.Rect(0,0,battlewidth,battleheight)

    def isEmpty(self,col,row):
        if not self.map.validFullPos(col,row): return False
        x,y = getAbsPos(col,row,True)
        return self.unitSet.availableSize(6,x,y)
    
    def inarea(self,unit):
        rect = unit.get_rect().copy()
        center = rect.center
        rect.width *= 3
        rect.height *= 3
        rect.center = center
        return rect.colliderect(pygame.Rect(0,0,battlewidth,battleheight))
    
    def draw(self,screen):
        self.updatePosition()
        units = []
        for unit in self.unitSet:
            units.append(unit)
        units.sort(key=lambda unit: unit.offsety)
        for unit in units:
            if self.inarea(unit):
                unit.draw(screen)
    
    def onMouseDown(self,x,y,button):
        for unit in self.unitSet:
            unit.onMouseDown(x,y,button)
    
    def onMouseUp(self,x,y,button):
        pass
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        pass

class Player():
    def __init__(self,index):
        self.index = index
        self.units = Set()
        self.money = 0
        self.powergen = 0
        self.powerload = 0
        self.powerhigh = False
        self.powerlow = False
        self.nopower= True

        self.numOfUnit = {}
        self.numOfUnitInCreate = {}

        self.buildingList = []
        self.defenceList = []
        self.infantryList = []
        self.vehicleList = []

        self.buildingCreateList = []
        self.buildingMoneyCost = 0
        self.buildingIsReady = False
        self.defenceCreateList = []
        self.defenceMoneyCost = 0
        self.defenceIsReady = False
        self.infantryCreateList = []
        self.infantryMoneyCost = 0
        self.infantryIsReady = False
        self.vehicleCreateList = []
        self.vehicleMoneyCost = 0
        self.vehicleIsReady = False

    def addUnit(self,unit):
        unit.player = self.index
        self.units.add(unit)
        if unit.name in self.numOfUnit:
            self.numOfUnit[unit.name] += 1
        else:
            self.numOfUnit[unit.name] = 1

    def removeUnit(self,unit):
        self.units.remove(unit)
        self.numOfUnit[unit.name] -= 1

    def update(self):
        self.updateBuildingList()
        self.updateBuildingCreateList()
        self.updateDefenceList()
        self.updateDefenceCreateList()
        self.updateInfantryList()
        self.updateInfantryCreateList()
        self.updateVehicleList()
        self.updateVehicleCreateList()

    def updateBuildingCreateList(self):
        if len(self.buildingCreateList) > 0:
            if self.buildingCreateList[0][0] > 0:
                if self.money > 0:
                    if self.buildingCreateList[0][0] >= createspeed:
                        self.buildingCreateList[0][0] -= createspeed
                        self.buildingMoneyCost += createspeed
                        self.money -= createspeed
                    else:
                        self.buildingMoneyCost += self.buildingCreateList[0][0]
                        self.money -= self.buildingCreateList[0][0]
                        self.buildingCreateList[0][0] = 0
            else:
                self.buildingIsReady = True
    def updateDefenceCreateList(self):
        if len(self.defenceCreateList) > 0:
            if self.defenceCreateList[0][0] > 0:
                if self.money > 0:
                    if self.defenceCreateList[0][0] >= createspeed:
                        self.defenceCreateList[0][0] -= createspeed
                        self.defenceMoneyCost += createspeed
                        self.money -= createspeed
                    else:
                        self.defenceMoneyCost += self.defenceCreateList[0][0]
                        self.money -= self.defenceCreateList[0][0]
                        self.defenceCreateList[0][0] = 0
            else:
                self.defenceIsReady = True
    def updateInfantryCreateList(self):
        if len(self.infantryCreateList) > 0:
            if self.infantryCreateList[0][0] > 0:
                if self.money > 0:
                    if self.infantryCreateList[0][0] >= createspeed:
                        self.infantryCreateList[0][0] -= createspeed
                        self.infantryMoneyCost += createspeed
                        self.money -= createspeed
                    else:
                        self.infantryMoneyCost += self.infantryCreateList[0][0]
                        self.money -= self.infantryCreateList[0][0]
                        self.infantryCreateList[0][0] = 0
            else:
                pass
    def updateVehicleCreateList(self):
        if len(self.vehicleCreateList) > 0:
            if self.vehicleCreateList[0][0] > 0:
                if self.money > 0:
                    if self.vehicleCreateList[0][0] >= createspeed:
                        self.vehicleCreateList[0][0] -= createspeed
                        self.vehicleMoneyCost += createspeed
                        self.money -= createspeed
                    else:
                        self.vehicleMoneyCost += self.vehicleCreateList[0][0]
                        self.money -= self.vehicleCreateList[0][0]
                        self.vehicleCreateList[0][0] = 0
            else:
                pass

    def updateBuildingList(self):
        self.buildingList = []
        for building in requisite:
            if typeofunit[building] != "building": continue
            enough = True
            for req in requisite[building]:
                if not req in self.numOfUnit or self.numOfUnit[req] <= 0:
                    enough = False
            if enough:
                self.buildingList.append(building)
    def updateDefenceList(self):
        self.defenceList = []
        for defence in requisite:
            if typeofunit[defence] != "defence": continue
            enough = True
            for req in requisite[defence]:
                if not req in self.numOfUnit or self.numOfUnit[req] <= 0:
                    enough = False
            if enough:
                self.defenceList.append(defence)
    def updateInfantryList(self):
        self.infantryList = []
        for infantry in requisite:
            if typeofunit[infantry] != "infantry": continue
            enough = True
            for req in requisite[infantry]:
                if not req in self.numOfUnit or self.numOfUnit[req] <= 0:
                    enough = False
            if enough:
                self.infantryList.append(infantry)
    def updateVehicleList(self):
        self.vehicleList = []
        for vehicle in requisite:
            if typeofunit[vehicle] != "vehicle": continue
            enough = True
            for req in requisite[vehicle]:
                if not req in self.numOfUnit or self.numOfUnit[req] <= 0:
                    enough = False
            if enough:
                self.vehicleList.append(vehicle)

    def getBuildingInFactory(self):
        if len(self.buildingCreateList) > 0:
            return self.buildingCreateList[0]
        return None
    def getDefenceInFactory(self):
        if len(self.defenceCreateList) > 0:
            return self.defenceCreateList[0]
        return None
    def getInfantryInFactory(self):
        if len(self.infantryCreateList) > 0:
            return self.infantryCreateList[0]
        return None
    def getVehicleInFactory(self):
        if len(self.vehicleCreateList) > 0:
            return self.vehicleCreateList[0]
        return None

    def addToCreateList(self,name):
        if typeofunit[name] == "building":
            self.buildingCreateList.append([costofunit[name],costofunit[name],name])
        elif typeofunit[name] == "defence":
            self.defenceCreateList.append([costofunit[name],costofunit[name],name])
        elif typeofunit[name] == "infantry":
            self.infantryCreateList.append([costofunit[name],costofunit[name],name])
        elif typeofunit[name] == "vehicle":
            self.vehicleCreateList.append([costofunit[name],costofunit[name],name])
        if name in self.numOfUnitInCreate:
            self.numOfUnitInCreate[name] += 1
        else:
            self.numOfUnitInCreate[name] = 1

    def getNumOfUnit(self,name):
        if name in self.numOfUnit:
            return self.numOfUnit[name]
        return 0

    def getNumOfUnitInCreate(self,name):
        if name in self.numOfUnitInCreate:
            return self.numOfUnitInCreate[name]
        return 0
