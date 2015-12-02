import pygame
from sets import Set
from math import log,exp

from listbox import ListBox
from data import images,classmap
from button import RA2Button, CreateButton, GameCtrlButton,\
        GamePanelButton, GamePanelPressedButton, TabButton, ButtonSet
from imagesprite import ImageSprite
from spritecontainer import SpriteContainer
from animation import SimpleAnimation
from map import getGridPos,addPos,getAbsPos
from consts import *

class SelectMapPanel(SpriteContainer):
    def __init__(self, select, back):
        super(SelectMapPanel,self).__init__()
        self.background = ImageSprite(images["selectmap"])
        self.add(self.background)
        
        self.buttons = pygame.sprite.Group()
        self.selectButton = RA2Button("Select")
        self.selectButton.setpos(menubuttonx,menubuttony)
        self.selectButton.setMouseListener(select)
        self.buttons.add(self.selectButton)
        
        self.backButton = RA2Button("Back")
        self.backButton.setpos(menubuttonx,self.selectButton.bottom())
        self.backButton.setMouseListener(back)
        self.buttons.add(self.backButton)
        
        self.listBox = ListBox()
        self.listBox.addItem("map0.txt")
        self.listBox.addItem("map1.txt")
        self.listBox.addItem("map2.txt")
        self.listBox.addItem("map3.txt")
        self.listBox.setpos(listboxx,listboxy)
    
    def onMouseDown(self,x,y,button):
        self.listBox.onMouseDown(x,y-self.listBox.y-boxpad)
        self.selectButton.onMouseDown(x,y,button)
        self.backButton.onMouseDown(x,y,button)
        
    def onMouseUp(self,x,y,button):
        self.selectButton.onMouseUp(x,y,button)
        self.backButton.onMouseUp(x,y,button)
        
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        self.selectButton.onMouseMove(x,y)
        self.backButton.onMouseMove(x,y)
    
    def draw(self,screen):
        super(SelectMapPanel,self).draw(screen)
        self.listBox.draw(screen)
        self.buttons.draw(screen)

class BattleFieldController(SpriteContainer):
    def __init__(self,gotoBackController):
        super(BattleFieldController,self).__init__()
        self.lspacer = ImageSprite(images["lspacer"])
        self.lspacer.setpos(0,gamectrlbuttony)
        self.add(self.lspacer)
        self.credits = ImageSprite(images["credits"])
        self.credits.setpos(creditx,credity)
        self.add(self.credits)
        self.paneltop = ImageSprite(images["top"])
        self.paneltop.setpos(topx,self.credits.bottom())
        self.add(self.paneltop)
        self.bttnbkgd = ImageSprite(images["bttnbkgd"])
        self.bttnbkgd.setpos(bttnbkgdx,bttnbkgdy)
        self.add(self.bttnbkgd)
        self.map = None
        self.mousedrag = False
        self.mouseMinimapDown = False

        self.animations = pygame.sprite.Group()
        self.lendcap = SimpleAnimation(\
                images["lendcap"],0,0,28,32,3,1,lendcapx,lendcapy)
        self.lendcap.setIndex(0)
        self.animations.add(self.lendcap)
        self.rendcap = SimpleAnimation(\
                images["rendcap"],0,0,28,32,1,1,rendcapx,rendcapy)
        self.rendcap.setIndex(0)
        self.animations.add(self.rendcap)

        self.buttons = pygame.sprite.Group()
        self.diplobtn = GamePanelButton("diplobtn")
        self.addSprite(self.diplobtn,diplobtnx,diplobtny)
        self.buttons.add(self.diplobtn)

        self.optbtn = GamePanelButton("optbtn")
        self.optbtn.setMouseListener(gotoBackController)
        self.addSprite(self.optbtn,self.diplobtn.right(),diplobtny)
        self.buttons.add(self.optbtn)

        self.radar = SimpleAnimation(\
                images["radar"],0,0,168,110,33,1,radarx,self.paneltop.bottom())
        self.radar.setIndex(0)
        self.animations.add(self.radar)

        self.tabtop = ImageSprite(images["tabtop"])
        self.tabtop.setpos(tabx,self.radar.bottom())
        self.add(self.tabtop)
        self.side0 = ImageSprite(images["sideb"])
        self.side0.setpos(createbtnboxx,self.tabtop.bottom())
        self.add(self.side0)
        self.side1 = ImageSprite(images["sideb"])
        self.side1.setpos(createbtnboxx,self.side0.bottom())
        self.add(self.side1)
        self.side2 = ImageSprite(images["sideb"])
        self.side2.setpos(createbtnboxx,self.side1.bottom())
        self.add(self.side2)
        self.side3 = ImageSprite(images["sideb"])
        self.side3.setpos(createbtnboxx,self.side2.bottom())
        self.add(self.side3)
        self.side4 = ImageSprite(images["sideb"])
        self.side4.setpos(createbtnboxx,self.side3.bottom())
        self.add(self.side4)
        self.side5 = ImageSprite(images["sideb"])
        self.side5.setpos(createbtnboxx,self.side4.bottom())
        self.add(self.side5)
        self.side6 = ImageSprite(images["sideb"])
        self.side6.setpos(createbtnboxx,self.side5.bottom())
        self.add(self.side6)
        self.tabbtm = ImageSprite(images["tabbtm"])
        self.tabbtm.setpos(tabx,self.side6.bottom())
        self.add(self.tabbtm)

        self.repairbtn = GamePanelPressedButton("repairbtn")
        self.addSprite(self.repairbtn,repairbtnx,self.radar.bottom()+7)
        self.buttons.add(self.repairbtn)
        self.sellbtn = GamePanelPressedButton("sellbtn")
        self.addSprite(self.sellbtn,self.repairbtn.right(),self.repairbtn.top())
        self.buttons.add(self.sellbtn)

        self.tab = Set()
        self.tabbtn0 = TabButton(0,self.tab,ButtonSet())
        self.tabbtn0.children.group = pygame.sprite.Group()
        self.tabbtn0.children.scroll = 0
        self.addSprite(self.tabbtn0,tabbtnx,self.repairbtn.bottom())
        self.buttons.add(self.tabbtn0)
        self.tab.add(self.tabbtn0)
        self.tabbtn1 = TabButton(1,self.tab,ButtonSet())
        self.tabbtn1.children.scroll = 0
        self.tabbtn1.children.group = pygame.sprite.Group()
        self.addSprite(self.tabbtn1,self.tabbtn0.right(),self.repairbtn.bottom())
        self.buttons.add(self.tabbtn1)
        self.tab.add(self.tabbtn1)
        self.tabbtn2 = TabButton(2,self.tab,ButtonSet())
        self.tabbtn2.children.scroll = 0
        self.tabbtn2.children.group = pygame.sprite.Group()
        self.addSprite(self.tabbtn2,self.tabbtn1.right(),self.repairbtn.bottom())
        self.buttons.add(self.tabbtn2)
        self.tab.add(self.tabbtn2)
        self.tabbtn3 = TabButton(3,self.tab,ButtonSet())
        self.tabbtn3.children.scroll = 0
        self.tabbtn3.children.group = pygame.sprite.Group()
        self.addSprite(self.tabbtn3,self.tabbtn2.right(),self.repairbtn.bottom())
        self.buttons.add(self.tabbtn3)
        self.tab.add(self.tabbtn3)
        self.tabbtn0.under()

    def save(self):
        pass
    
    def get_battle_rect(self):
        return pygame.Rect(0,0,battlewidth,battleheight)

    def goodToPutBuilding(self,name,col,row):
        return self.characters.isEmpty(col,row) and\
            ((self.map.islandGrid(col,row) and canland[name])
          or (self.map.iswaterGrid(col,row) and canwater[name]))
    
    def draw(self,screen):
        super(BattleFieldController,self).draw(screen)

        self.buttons.draw(screen)
        self.animations.draw(screen)
        self.drawMinimap(screen)
        self.drawCreateButtons(screen)

    def drawCreateButtons(self,screen):
        if self.tabbtn0.children.visible:
            self.drawCreateButtonSet(self.tabbtn0.children,screen)
        if self.tabbtn1.children.visible:
            self.drawCreateButtonSet(self.tabbtn1.children,screen)
        if self.tabbtn2.children.visible:
            self.drawCreateButtonSet(self.tabbtn2.children,screen)
        if self.tabbtn3.children.visible:
            self.drawCreateButtonSet(self.tabbtn3.children,screen)

    def drawCreateButtonSet(self,buttonSet,screen):
        if not buttonSet.visible: return
        for button in buttonSet:
            ix = button.index % 2
            iy = button.index / 2 + buttonSet.scroll
            button.setpos(ix*createbtnw+createbtnx,iy*createbtny+self.side0.top())
        buttonSet.group.draw(screen)

    def drawMinimap(self,screen):
        screen.blit(self.minimap,(minimapx,minimapy))
        x,y = self.map.transformMini(-self.map.x,-self.map.y)
        view = pygame.Rect(x,y,self.map.minimapvieww,self.map.minimapviewh)
        pygame.draw.rect(screen,RED,view,1)
    
    def updateMinimapView(self,x,y):
        if x >= minimapx and x <= minimapx + minimapw and\
             y >= minimapy and y <= minimapy + minimaph:
            x,y = self.map.transformFromMini(\
                    x-self.map.minimapvieww/2,y-self.map.minimapviewh/2)
            self.map.x,self.map.y = -x,-y
            self.map.fitOffset()
            self.mouseMinimapDown = True

    def clickButtonSet(self,buttonSet,x,y,button):
        for b in buttonSet:
            if button == 1:
                ix = b.index % 2
                iy = b.index / 2 + buttonSet.scroll
                b.setpos(ix*createbtnw+createbtnx,iy*createbtny+self.side0.top())
                if not b.disabled and b.contains(x,y):
                    b.mouseListener(b.name)
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(BattleFieldController,self).onMouseMove(x,y,button1,button2,button3)
        if self.map != None:
            self.map.updateScrollV(x,y,button3==True)
        if self.mouseMinimapDown:
            self.updateMinimapView(x,y)
        
    def onMouseDown(self,x,y,button):
        super(BattleFieldController,self).onMouseDown(x,y,button)
        if self.tabbtn0.children.visible:
            self.clickButtonSet(self.tabbtn0.children,x,y,button)
        if self.tabbtn1.children.visible:
            self.clickButtonSet(self.tabbtn1.children,x,y,button)
        if self.tabbtn2.children.visible:
            self.clickButtonSet(self.tabbtn2.children,x,y,button)
        if self.tabbtn3.children.visible:
            self.clickButtonSet(self.tabbtn3.children,x,y,button)
        self.updateMinimapView(x,y)
        
    def onMouseUp(self,x,y,button):
        super(BattleFieldController,self).onMouseUp(x,y,button)
        self.mouseMinimapDown = False
    
    def onKeyDown(self,keyCode,mod):
        if keyCode == pygame.K_LEFT:
            self.map.scrollv[0] = 1
        elif keyCode == pygame.K_RIGHT:
            self.map.scrollv[1] = 1
        elif keyCode == pygame.K_UP:
            self.map.scrollv[2] = 1
        elif keyCode == pygame.K_DOWN:
            self.map.scrollv[3] = 1
        
    def onKeyUp(self,keyCode,mod):
        if keyCode == pygame.K_LEFT:
            self.map.scrollv[0] = 0
        elif keyCode == pygame.K_RIGHT:
            self.map.scrollv[1] = 0
        elif keyCode == pygame.K_UP:
            self.map.scrollv[2] = 0
        elif keyCode == pygame.K_DOWN:
            self.map.scrollv[3] = 0

class GameController(BattleFieldController):
    def __init__(self,gotoBackController):
        super(GameController,self).__init__(gotoBackController)
        
        self.minimap = None
        self.groupOne = Set()
        self.groupTwo = Set()
        self.groupThree = Set()
        self.selected = Set()

        self.groupOneButton = GameCtrlButton(0)
        self.groupOneButton.setMouseListener(self.setGroupOne)
        self.buttons.add(self.groupOneButton)
        self.addSprite(self.groupOneButton,self.lendcap.right(),gamectrlbuttony)

        self.groupTwoButton = GameCtrlButton(1)
        self.groupTwoButton.setMouseListener(self.setGroupTwo)
        self.buttons.add(self.groupTwoButton)
        self.addSprite(self.groupTwoButton,self.groupOneButton.right(),gamectrlbuttony)

        self.groupThreeButton = GameCtrlButton(2)
        self.groupThreeButton.setMouseListener(self.setGroupThree)
        self.buttons.add(self.groupThreeButton)
        self.addSprite(self.groupThreeButton,self.groupTwoButton.right(),gamectrlbuttony)

        self.selectSameTypeButton = GameCtrlButton(3)
        self.selectSameTypeButton.setMouseListener(self.selectSameType)
        self.buttons.add(self.selectSameTypeButton)
        self.addSprite(self.selectSameTypeButton,self.groupThreeButton.right(),gamectrlbuttony)

        self.deployButton = GameCtrlButton(4)
        self.deployButton.setMouseListener(self.deploy)
        self.buttons.add(self.deployButton)
        self.addSprite(self.deployButton,self.selectSameTypeButton.right(),gamectrlbuttony)

        self.guardButton = GameCtrlButton(6)
        self.guardButton.setMouseListener(self.guard)
        self.buttons.add(self.guardButton)
        self.addSprite(self.guardButton,self.deployButton.right(),gamectrlbuttony)

        self.setpathButton = GameCtrlButton(9)
        self.setpathButton.setMouseListener(self.setpath)
        self.buttons.add(self.setpathButton)
        self.addSprite(self.setpathButton,self.guardButton.right(),gamectrlbuttony)

        self.player = None
        self.characters = None

        self.powere = ImageSprite(images["powerp"],5,1,0)
        self.powerh = ImageSprite(images["powerp"],5,1,1)
        self.powerl = ImageSprite(images["powerp"],5,1,2)
        self.powern = ImageSprite(images["powerp"],5,1,3)
        self.moneyfont = pygame.font.Font(None,15)

        self.createButtons = {}
        for unitname in requisite:
            self.createButtons[unitname] = CreateButton(unitname)
            self.createButtons[unitname].setMouseListener(self.addToCreateList)

        self.selectBuildingPosition = ""
        self.pointerset = None

    def addToCreateList(self,name):
        if typeofunit[name] == "building":
            builded = self.player.getBuildingInFactory()
            if builded != None:
                if builded[0] == 0 and builded[2] == name:
                    self.selectBuildingPosition = name
                else:
                    self.cannotApply()
            else:
                self.player.addToCreateList(name)
        else:
            self.player.addToCreateList(name)

    def takeOverGame(self,game,player):
        self.characters = game
        self.player = player

    def draw(self,screen):
        if self.pointerset != None:
            for col,row in self.pointerset:
                if self.goodToPutBuilding(self.selectBuildingPosition,col,row):
                    self.map.drawGreenPointer(screen,col,row)
                else:
                    self.map.drawRedPointer(screen,col,row)
        for unit in self.selected:
            if unit.inarea(self.characters):
                unit.drawBloodBar(screen)
                if unit in self.groupOne:
                    unit.drawGroup(screen,1)
                if unit in self.groupTwo:
                    unit.drawGroup(screen,2)
                if unit in self.groupThree:
                    unit.drawGroup(screen,3)

        super(GameController,self).draw(screen)

        moneyimg = self.moneyfont.render(str(self.player.money),False,WHITE)
        moneyrect = moneyimg.get_rect()
        moneyrect.center = self.credits.rect.center
        screen.blit(moneyimg,moneyrect)

        if self.mousedrag:
            x = min(self.mousedownx,self.mousex)
            y = min(self.mousedowny,self.mousey)
            w = abs(self.mousedownx-self.mousex)
            h = abs(self.mousedowny-self.mousey)
            rect = pygame.Rect(x,y,w,h)
            pygame.draw.rect(screen,WHITE,rect,1)

        self.drawPower(screen)

    def drawMinimap(self,screen):
        super(GameController,self).drawMinimap(screen)

        for unit in self.characters.unitSet:
            x,y = self.map.transformMini(unit.offsetx,unit.offsety)
            pygame.draw.rect(screen,colorofplayer[unit.player],pygame.Rect(x,y,1,1),2)

    def drawPower(self,screen):
        ppowern = int((1-exp(-max(self.player.powergen,self.player.powerload)*log(2)/200)) * powern)
        if self.player.powergen > self.player.powerload:
            powergenn = ppowern
            powerloadn = self.player.powerload*ppowern/self.player.powergen
        else:
            powerloadn = ppowern
            if self.player.powerload == 0:
                powergenn = 0
            else:
                powergenn = self.player.powergen*ppowern/self.player.powerload
        for i in range(powern):
            screen.blit(self.powere.image,(powerx,powery-i*2))
        if self.player.powerhigh:
            for i in range(powergenn):
                screen.blit(self.powerh.image,(powerx,powery-i*2))
        elif self.player.powerlow:
            for i in range(powergenn):
                screen.blit(self.powerl.image,(powerx,powery-i*2))
        for i in range(powerloadn):
            screen.blit(self.powern.image,(powerx,powery-i*2))

    def setGroupOne(self):
        if len(self.groupOne) == 0:
            self.groupOne = self.selected.copy()
            for unit in self.selected:
                if unit in self.groupTwo:
                    self.groupTwo.remove(unit)
                if unit in self.groupThree:
                    self.groupThree.remove(unit)
        else:
            self.selected = self.groupOne.copy()
    
    def setGroupTwo(self):
        if len(self.groupTwo) == 0:
            self.groupTwo = self.selected.copy()
            for unit in self.selected:
                if unit in self.groupOne:
                    self.groupOne.remove(unit)
                if unit in self.groupThree:
                    self.groupThree.remove(unit)
        else:
            self.selected = self.groupTwo.copy()
    
    def setGroupThree(self):
        if len(self.groupThree) == 0:
            self.groupThree = self.selected.copy()
            for unit in self.player.units:
                if unit in self.groupOne:
                    self.groupOne.remove(unit)
                if unit in self.groupTwo:
                    self.groupTwo.remove(unit)
        else:
            self.selected = self.groupThree.copy()
    
    def selectSameType(self):
        selectedTypes = Set()
        for unit in self.selected:
            selectedTypes.add(unit.name)
        original = len(self.selected)
        for unit in self.player.units:
            if unit.name in selectedTypes and unit.inarea(self.characters):
                self.selected.add(unit)
        if len(self.selected) == original:
            for unit in self.player.units:
                if unit.name in selectedTypes:
                    self.selected.add(unit)
    
    def deploy(self):
        pass
    
    def guard(self):
        pass
    
    def setpath(self):
        pass

    def cannotApply(self):
        pass

    def update(self):
        self.player.update()
        self.updateBuildingButtons()
        self.updateDefenceButtons()
        self.updateInfantryButtons()
        self.updateVehicleButtons()
        self.cleanupRemovedUnits()

    def cleanupRemovedUnits(self):
        self.groupOne.intersection_update(self.player.units)
        self.groupTwo.intersection_update(self.player.units)
        self.groupThree.intersection_update(self.player.units)
        self.selected.intersection_update(self.player.units)

    def updateBuildingButtons(self):
        builded = self.player.getBuildingInFactory()
        visible = self.tabbtn0.children.visible
        self.tabbtn0.children = ButtonSet()
        self.tabbtn0.children.visible = visible
        self.tabbtn0.children.scroll = 0
        self.tabbtn0.children.group = pygame.sprite.Group()
        for i,building in enumerate(self.player.buildingList):
            self.tabbtn0.children.add(self.createButtons[building])
            self.createButtons[building].index = i
            self.tabbtn0.children.group.add(self.createButtons[building])
            if builded != None and builded[2] != building:
                self.createButtons[building].disable()

    def updateDefenceButtons(self):
        builded = self.player.getDefenceInFactory()
        visible = self.tabbtn1.children.visible
        self.tabbtn1.children = ButtonSet()
        self.tabbtn1.children.visible = visible
        self.tabbtn1.children.scroll = 0
        self.tabbtn1.children.group = pygame.sprite.Group()
        for i,defence in enumerate(self.player.defenceList):
            self.tabbtn1.children.add(self.createButtons[defence])
            self.createButtons[defence].index = i
            self.tabbtn1.children.group.add(self.createButtons[defence])
            if builded != None and builded[2] != defence:
                self.createButtons[defence].disable()

    def updateInfantryButtons(self):
        visible = self.tabbtn2.children.visible
        self.tabbtn2.children = ButtonSet()
        self.tabbtn2.children.visible = visible
        self.tabbtn2.children.scroll = 0
        self.tabbtn2.children.group = pygame.sprite.Group()
        for i,infantry in enumerate(self.player.infantryList):
            self.tabbtn2.children.add(self.createButtons[infantry])
            self.createButtons[infantry].index = i
            self.tabbtn2.children.group.add(self.createButtons[infantry])

    def updateVehicleButtons(self):
        visible = self.tabbtn3.children.visible
        self.tabbtn3.children = ButtonSet()
        self.tabbtn3.children.visible = visible
        self.tabbtn3.children.scroll = 0
        self.tabbtn3.children.group = pygame.sprite.Group()
        for i,vehicle in enumerate(self.player.infantryList):
            self.tabbtn3.children.add(self.createButtons[vehicle])
            self.createButtons[vehicle].index = i
            self.tabbtn3.children.group.add(self.createButtons[vehicle])
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(GameController,self).onMouseMove(x,y,button1,button2,button3)
        if self.selectBuildingPosition != "":
            if self.get_battle_rect().contains(pygame.Rect(x,y,1,1)) and\
                    not button1 and not button2:
                pointerx,pointery = self.map.getGridPos(x,y)
                self.pointerset = [(addPos(pointerx,pointery,col,row))\
                        for col,row in pointerset[self.selectBuildingPosition]]
            return
        if button1 != None and button1 and self.mousedown:
            self.mousex = min(x,battlewidth)
            self.mousey = min(y,battleheight)
            self.mousedrag = True

    def onMouseDown(self,x,y,button):
        super(GameController,self).onMouseDown(x,y,button)
        if button == 1:
            if self.pointerset != None:
                for col,row in self.pointerset:
                    if not self.goodToPutBuilding(self.selectBuildingPosition,col,row):
                        return
                name = self.selectBuildingPosition
                building = classmap[name](self.player.index)
                col,row = self.pointerset[0]
                offsetx,offsety = getAbsPos(col,row,True)
                offsetx += modify[name][0]
                offsety += modify[name][1]
                self.characters.addUnit(building,offsetx,offsety)
                self.pointerset = None
                self.selectBuildingPosition = ""
                self.player.popBuildingList()
                return
            if x >= 0 and x <= battlewidth and\
               y >= 0 and y <= battleheight:
                self.mousedownx = x
                self.mousedowny = y
                self.mousedown = True
        elif button == 3:
            self.selectBuildingPosition = ""
            self.pointerset = None
            self.mousedrag = False
            if self.get_battle_rect().contains(pygame.Rect(x,y,1,1)):
                for unit in self.selected:
                    unit.target = (unit.offsetx+(x-unit.x),unit.offsety+(y-unit.y))

    def onMouseUp(self,x,y,button):
        super(GameController,self).onMouseUp(x,y,button)
        if button == 1:
            if self.mousedrag:
                x = min(self.mousedownx,self.mousex)
                y = min(self.mousedowny,self.mousey)
                w = abs(self.mousedownx-self.mousex)
                h = abs(self.mousedowny-self.mousey)
                rect = pygame.Rect(x,y,w,h)
                self.selected = Set()
                for unit in self.player.units:
                    if rect.contains(unit.get_rect()):
                        if unit.regionselectable:
                            self.selected.add(unit)
            else:
                if self.get_battle_rect().contains(pygame.Rect(x,y,1,1)):
                    nounit = True
                    for unit in self.selected:
                        if unit.get_rect().contains(pygame.Rect(x,y,1,1)):
                            nounit = False
                            unit.onDoubleClick()
                            break
                    self.selected = Set()
                    if nounit:
                        for unit in self.player.units:
                            if unit.get_rect().contains(pygame.Rect(x,y,1,1)):
                                self.selected = Set([unit])
                                break
            self.mousedrag = False
            self.mousedown = False

class MapEditor(BattleFieldController):
    def __init__(self,gotoBackController):
        super(MapEditor,self).__init__(gotoBackController)
        self.map = None
        self.mapfile = ""
        self.paint = 1
        
        self.grassButton = CreateButton("Grass")
        self.grassButton.setMouseListener(self.setPaint)
        self.buttons.add(self.grassButton)
        self.addSprite(self.grassButton,createbtnx,self.side0.top())
        self.waterButton = CreateButton("Water")
        self.waterButton.setMouseListener(self.setPaint)
        self.buttons.add(self.waterButton)
        self.addSprite(self.waterButton,self.grassButton.right(),self.side0.top())
    
    def save(self):
        self.map.write(self.mapfile)
        
    def setPaint(self,name):
        if name == "Grass":
            self.paint = 1
        elif name == "Water":
            self.paint = 0
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(MapEditor,self).onMouseMove(x,y,button1,button2,button3)
        if self.map != None:
            if button1 != None and button1:
                self.map.paint(x,y,self.paint)
            
class GameBackController(SpriteContainer):
    def __init__(self,gotoSave,goBack,exitGame):
        super(GameBackController,self).__init__()
        self.background = ImageSprite(images["selectmap"])
        self.add(self.background)

        self.buttons = pygame.sprite.Group()
        self.saveButton = RA2Button("Save")
        self.saveButton.setMouseListener(gotoSave)
        self.addSprite(self.saveButton,menubuttonx,menubuttony)
        self.buttons.add(self.saveButton)
        self.backButton = RA2Button("Back")
        self.backButton.setMouseListener(goBack)
        self.addSprite(self.backButton,menubuttonx,self.saveButton.bottom())
        self.buttons.add(self.backButton)
        self.exitButton = RA2Button("Exit")
        self.exitButton.setMouseListener(exitGame)
        self.addSprite(self.exitButton,menubuttonx,self.backButton.bottom())
        self.buttons.add(self.exitButton)

    def draw(self,screen):
        super(GameBackController,self).draw(screen)
        self.buttons.draw(screen)

    def onMouseDown(self,x,y,button):
        super(GameBackController,self).onMouseDown(x,y,button)
        
    def onMouseUp(self,x,y,button):
        super(GameBackController,self).onMouseUp(x,y,button)
        
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(GameBackController,self).onMouseMove(x,y,button1,button2,button3)

class MapBackController(GameBackController):
    def __init__(self,gotoSave,goBack,exitMap):
        super(MapBackController,self).__init__(gotoSave,goBack,exitMap)
        self.game = None

    def onMouseDown(self,x,y,button):
        super(MapBackController,self).onMouseDown(x,y,button)
        
    def onMouseUp(self,x,y,button):
        super(MapBackController,self).onMouseUp(x,y,button)
        
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(MapBackController,self).onMouseMove(x,y,button1,button2,button3)
