import pygame

from map import Map, getAbsPos, getGridCenter
from treecontainer import collide, TreeContainer
from data import classmap
from unit import Unit
from vehicle import *
from infantry import *
from building import *
from consts import *


class Game():
  def __init__(self, map):
    self.map = map
    self.unitSet = None
    self.x = map.x
    self.y = map.y
    self.running = False
    self.players = []

  def initNewGame(self, playerData):
    self.unitSet = TreeContainer(
        10, 10, self.map.groundwidth-20, self.map.groundheight-20)
    self.running = False
    self.players = [Player(i) for i in range(2)]
    for player in self.players:
      player.money = 30000

    for player in playerData:
      data = playerData[player]
      flag = data["flag"]
      col, row = data["position"]
      mcv = MCV(flag)
      self.addUnitGrid(mcv, col, row)
      for unitdata in data["initials"]:
        name = unitdata["name"]
        x, y = unitdata["pos"]
        animation = unitdata["animation"]
        x, y = x+mcv.offsetx, y+mcv.offsety
        self.addUnit(classmap[name](flag, animation), x, y)
    self.updatePosition()

  def addUnit(self, unit, x, y):
    if self.unitSet.addPos(unit, x, y):
      self.players[unit.player]._addUnit(unit)
      return True
    return False

  def addUnitGrid(self, unit, col, row):
    if self.unitSet.addGrid(unit, col, row):
      self.players[unit.player]._addUnit(unit)
      return True
    return False

  def removeUnit(self, unit):
    self.unitSet.remove(unit)
    self.players[unit.player]._removeUnit(unit)

  def available(self, unit, x, y):
    return self.unitSet.available(unit, x, y)

  def step(self):
    unitlist = []
    for unit in self.unitSet:
      unitlist.append(unit)
    for unit in unitlist:
      unit.step(self.map, self)
      if hasattr(unit, "replace") and unit.replace is not None:
        name = unit.replace
        newunit = classmap[name](unit.player)
        newunit.HP = unit.HP
        newunit.fullHP = unit.fullHP
        if isinstance(newunit, Building):
          offsetx, offsety = getGridCenter(unit.offsetx, unit.offsety)
        offsetx += modify[name][0]
        offsety += modify[name][1]
        self.removeUnit(unit)
        if not self.addUnit(newunit, offsetx, offsety):
          self.addUnit(unit)

  def updatePosition(self):
    self.x = self.map.x
    self.y = self.map.y
    for unit in self.unitSet:
      unit.x = self.x + unit.offsetx
      unit.y = self.y + unit.offsety

  def update(self):
    self.updatePosition()
    if self.running:
      for player in self.players:
        player._update()
        if player.createIsReady["infantry"] and player.mainGpile is not None:
          player.createMobUnit(player.mainGpile, "infantry", self)
        if player.createIsReady["vehicle"] and player.mainGweap is not None:
          player.createMobUnit(player.mainGweap, "vehicle", self)
      self.step()

  def get_battle_rect():
    return pygame.Rect(0, 0, battlewidth, battleheight)

  def isEmpty(self, col, row):
    if not self.map.validFullPos(col, row):
      return False
    x, y = getAbsPos(col, row, True)
    return self.unitSet.availableSize(6, x, y)

  def inarea(self, unit):
    rect = unit.get_rect().copy()
    center = rect.center
    rect.width *= 3
    rect.height *= 3
    rect.center = center
    return rect.colliderect(pygame.Rect(0, 0, battlewidth, battleheight))

  def draw(self, screen):
    self.updatePosition()
    units = []
    for unit in self.unitSet:
      units.append(unit)
    units.sort(key=lambda unit: unit.offsety)
    for unit in units:
      if self.inarea(unit):
        unit.draw(screen)

  def onMouseDown(self, x, y, button):
    for unit in self.unitSet:
      unit.onMouseDown(x, y, button)

  def onMouseUp(self, x, y, button):
    pass

  def onMouseMove(self, x, y, button1=None, button2=None, button3=None):
    pass


class Player():
  def __init__(self, index):
    self.index = index
    self.units = set()
    self.money = 0
    self.powergen = 0
    self.powerload = 0
    self.powerhigh = False
    self.powerlow = False
    self.nopower = True

    self.numOfUnit = {}
    self.numOfUnitInCreate = {}

    self.createButtonList = {"building": [], "defence": [],
                             "infantry": [], "vehicle": []}

    self.createList = {"building": [], "defence": [],
                       "infantry": [], "vehicle": []}
    self.createMoneyCost = {"building": 0, "defence": 0,
                            "infantry": 0, "vehicle": 0}
    self.createIsReady = {"building": False, "defence": False,
                          "infantry": False, "vehicle": False}
    self.createStop = {"building": False, "defence": False,
                       "infantry": False, "vehicle": False}

    self.mainGpile = None
    self.mainGweap = None

  def createFixUnit(self, col, row, t, characters):
    builded = self.getUnitInFactory(t)
    if builded is not None and self.createIsReady[t]:
      name = builded[2]
      offsetx, offsety = getAbsPos(col, row, True)
      offsetx += modify[name][0]
      offsety += modify[name][1]
      unit = classmap[name](self.index)
      if characters.addUnit(unit, offsetx, offsety):
        self.__popCreateList(t)

  def createMobUnit(self, factory, t, characters):
    builded = self.getUnitInFactory(t)
    if builded is not None and self.createIsReady[t]:
      name = builded[2]
      offsetx = factory.offsetx + createPosition[factory.name][0]
      offsety = factory.offsety + createPosition[factory.name][1]
      animation = createAnimation[name]
      unit = classmap[name](self.index, animation)
      if characters.addUnit(unit, offsetx, offsety):
        self.__popCreateList(t)

  def _addUnit(self, unit):
    unit.player = self.index
    self.units.add(unit)
    if unit.name in self.numOfUnit:
      self.numOfUnit[unit.name] += 1
    else:
      self.numOfUnit[unit.name] = 1

  def _removeUnit(self, unit):
    self.units.remove(unit)
    self.numOfUnit[unit.name] -= 1

  def _update(self):
    for t in ["building", "defence", "infantry", "vehicle"]:
      self.__updateCreateButtonList(t)
      self.__stepCreateList(t)
    self.__resetMainFactories()
    self.__updatePower()

  def __updatePower(self):
    self.powergen = 0
    self.powerload = 0
    for unit in self.units:
      if hasattr(unit, "power"):
        if unit.power > 0:
          self.powergen += unit.power
        elif unit.power < 0:
          self.powerload -= unit.power
    self.powerhigh = self.powergen >= self.powerload - powerthresh
    self.powerlow = not self.powerhigh and self.powergen >= self.powerload
    self.nopower = not self.powerhigh and not self.powerlow

  def __resetMainFactories(self):
    if self.mainGpile is None or self.mainGpile not in self.units:
      self.mainGpile = None
      for unit in self.units:
        if unit.name == "Gpile":
          self.mainGpile = unit
          break
    if self.mainGweap is None or self.mainGweap not in self.units:
      self.mainGweap = None
      for unit in self.units:
        if unit.name == "Gweap":
          self.mainGweap = unit
          break

  def cancelCreateList(self, t):
    if len(self.createList[t]) > 0:
      if self.createStop[t] or self.createIsReady[t]:
        self.createList[t].pop(0)
        self.money += self.createMoneyCost[t]
        self.createMoneyCost[t] = 0
        self.createStop[t] = False
        self.createIsReady[t] = False
      else:
        self.createStop[t] = True

  def getUnitInFactory(self, t):
    if len(self.createList[t]) > 0:
      return self.createList[t][0]
    return None

  def addToCreateList(self, name):
    self.createList[typeofunit[name]].append(
        [costofunit[name], costofunit[name], name])
    if name in self.numOfUnitInCreate:
      self.numOfUnitInCreate[name] += 1
    else:
      self.numOfUnitInCreate[name] = 1

  def getNumOfUnit(self, name):
    if name in self.numOfUnit:
      return self.numOfUnit[name]
    return 0

  def getNumOfUnitInCreate(self, name):
    if name in self.numOfUnitInCreate:
      return self.numOfUnitInCreate[name]
    return 0

  def __stepCreateList(self, t):
    if len(self.createList[t]) > 0:
      if self.createStop[t]:
        return
      if self.createList[t][0][0] > 0:
        if self.money > 0:
          if self.createList[t][0][0] >= createspeed:
            self.createList[t][0][0] -= createspeed
            self.createMoneyCost[t] += createspeed
            self.money -= createspeed
          else:
            self.createMoneyCost[t] += self.createList[t][0][0]
            self.money -= self.createList[t][0][0]
            self.createList[t][0][0] = 0
        self.createIsReady[t] = False
      else:
        self.createIsReady[t] = True

  def __updateCreateButtonList(self, t):
    self.createButtonList[t] = []
    for unit in allunits[t]:
      enough = True
      for req in requisite[unit]:
        if req not in self.numOfUnit or self.numOfUnit[req] <= 0:
          enough = False
      if enough:
        self.createButtonList[t].append(unit)

  def __popCreateList(self, t):
    if len(self.createList[t]) > 0:
      self.createList[t].pop(0)
      self.createMoneyCost[t] = 0
      self.createIsReady[t] = False
