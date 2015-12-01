import pygame
from sets import Set
from math import log,exp

from listbox import ListBox
from data import images
from button import RA2Button, PalatteButton, GameCtrlButton, GamePanelButton
from imagesprite import ImageSprite
from spritecontainer import SpriteContainer
from animation import SimpleAnimation
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

class MapEditor(SpriteContainer):
    def __init__(self,back):
        super(MapEditor,self).__init__()
        self.background = ImageSprite(images["ctrlpanel"])
        self.add(self.background)
        self.map = None
        self.mapfile = ""
        self.paint = 1
        self.mouseMinimapDown = False
        
        self.buttons = pygame.sprite.Group()
        self.grassButton = PalatteButton(0,0)
        self.grassButton.setMouseListener(self.setGrassPaint)
        self.buttons.add(self.grassButton)
        self.addSprite(self.grassButton,colorbuttonx,colorbuttony)
        self.waterButton = PalatteButton(0,1)
        self.waterButton.setMouseListener(self.setWaterPaint)
        self.buttons.add(self.waterButton)
        self.addSprite(self.waterButton,colorbuttonx+gridwidth,colorbuttony)
        self.saveButton = RA2Button("Save")
        self.saveButton.setMouseListener(self.save)
        self.buttons.add(self.saveButton)
        self.addSprite(self.saveButton,menubuttonx,self.waterButton.bottom())
        self.backButton = RA2Button("Back")
        self.backButton.setMouseListener(back)
        self.buttons.add(self.backButton)
        self.addSprite(self.backButton,menubuttonx,self.saveButton.bottom())

        self.minimap = images["allyflag"]
    
    def save(self):
        self.map.write(self.mapfile)
        
    def setGrassPaint(self):
        self.paint = 1
    def setWaterPaint(self):
        self.paint = 0
    
    def draw(self,screen):
        super(MapEditor,self).draw(screen)
        self.buttons.draw(screen)
        screen.blit(self.minimap,(minimapx,minimapy))
        x = (-self.map.x) * self.minimap.get_rect().width / self.map.groundwidth + minimapx
        y = (-self.map.y) * self.minimap.get_rect().height / self.map.groundheight + minimapy
        w = battlewidth * self.minimap.get_rect().width / self.map.groundwidth
        h = battleheight * self.minimap.get_rect().height / self.map.groundheight
        view = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen,RED,view,1)
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(MapEditor,self).onMouseMove(x,y,button1,button2,button3)
        if self.map != None:
            self.map.updateScrollV(x,y,button3==True)
            if button1 != None and button1:
                self.map.paint(x,y,self.paint)
        if self.mouseMinimapDown:
            self.updateMinimapView(x,y)
        
    def onMouseDown(self,x,y,button):
        super(MapEditor,self).onMouseDown(x,y,button)
        self.updateMinimapView(x,y)
    
    def updateMinimapView(self,x,y):
        minimapw = self.map.minimapw
        minimaph = self.map.minimaph
        if x >= minimapx and x <= minimapx + minimapw and\
            y >= minimapy and y <= minimapy + minimaph:
            x,y = self.map.transformFromMini(x,y)
            self.map.x,self.map.y = -x,-y
            self.map.fitOffset()
            self.mouseMinimapDown = True
        
    def onMouseUp(self,x,y,button):
        super(MapEditor,self).onMouseUp(x,y,button)
        self.mouseMinimapDown = False
        self.mousedown = False
    
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
            
class GameController(SpriteContainer):
    def __init__(self):
        super(GameController,self).__init__()
        self.lspacer = ImageSprite(images["lspacer"])
        self.lspacer.setpos(0,gamectrlbuttony)
        self.add(self.lspacer)
        self.credits = ImageSprite(images["credits"])
        self.credits.setpos(creditx,credity)
        self.add(self.credits)
        self.player = None

        self.powere = ImageSprite(images["powerp"],5,1,0)
        self.powerh = ImageSprite(images["powerp"],5,1,1)
        self.powerl = ImageSprite(images["powerp"],5,1,2)
        self.powern = ImageSprite(images["powerp"],5,1,3)
        self.moneyfont = pygame.font.Font(None,15)

        self.map = None
        self.mousedrag = False
        self.mousedown = False
        self.mouseMinimapDown = False
        self.characters = None

        self.animations = pygame.sprite.Group()
        self.lendcap = SimpleAnimation(\
                images["lendcap"],0,0,28,32,3,1,20,gamectrlbuttony)
        self.lendcap.setIndex(0)
        self.animations.add(self.lendcap)

        self.buttons = pygame.sprite.Group()
        self.groupOneButton = GameCtrlButton(0)
        self.groupOneButton.setMouseListener(self.setGroupOne)
        self.groupOneButton.x
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
        self.diplobtn = GamePanelButton("diplobtn")
        self.addSprite(self.diplobtn,diplobtnx,diplobtny)
        self.buttons.add(self.diplobtn)
        self.optbtn = GamePanelButton("optbtn")
        self.addSprite(self.optbtn,self.diplobtn.right(),diplobtny)
        self.buttons.add(self.optbtn)

        self.radar = SimpleAnimation(\
                images["radar"],0,0,168,110,33,1,radarx,self.optbtn.bottom()+10)
        self.radar.setIndex(0)
        self.animations.add(self.radar)
        
        self.minimap = images["allyflag"]
        self.groupOne = Set()
        self.groupTwo = Set()
        self.groupThree = Set()
        self.selected = Set()

    def takeOverGame(self,game,player):
        self.characters = game
        self.player = player
    
    def save(self):
        pass
    
    def get_battle_rect(self):
        return pygame.Rect(0,0,battlewidth,battleheight)
    
    def draw(self,screen):
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

        #self.drawMinimap(screen)
        self.buttons.draw(screen)
        self.animations.draw(screen)

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

    def drawMinimap(self,screen):
        if self.mousedrag:
            x = min(self.mousedownx,self.mousex)
            y = min(self.mousedowny,self.mousey)
            w = abs(self.mousedownx-self.mousex)
            h = abs(self.mousedowny-self.mousey)
            rect = pygame.Rect(x,y,w,h)
            pygame.draw.rect(screen,WHITE,rect,1)
        screen.blit(self.minimap,(minimapx,minimapy))
        x,y = self.map.transformMini(-self.map.x,-self.map.y)
        view = pygame.Rect(x,y,self.map.minimapvieww,self.map.minimapviewh)
        pygame.draw.rect(screen,RED,view,1)

        for unit in self.characters.unitSet:
            x,y = self.map.transformMini(unit.offsetx,unit.offsety)
            pygame.draw.rect(screen,colorofplayer[unit.player],pygame.Rect(x,y,1,1),2)
    
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
    
    def updateMinimapView(self,x,y):
        minimapw = self.map.minimapw
        minimaph = self.map.minimaph
        if x >= minimapx and x <= minimapx + minimapw and\
             y >= minimapy and y <= minimapy + minimaph:
            x,y = self.map.transformFromMini(x,y)
            self.map.x,self.map.y = -x,-y
            self.map.fitOffset()
            self.mouseMinimapDown = True
    
    def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
        super(GameController,self).onMouseMove(x,y,button1,button2,button3)
        if self.map != None:
            self.map.updateScrollV(x,y,button3==True)
        if button1 != None and button1 and self.mousedown:
            self.mousex = min(x,battlewidth)
            self.mousey = min(y,battleheight)
            self.mousedrag = True
        if self.mouseMinimapDown:
            self.updateMinimapView(x,y)
        
    def onMouseDown(self,x,y,button):
        super(GameController,self).onMouseDown(x,y,button)
        if button == 1:
            if x >= 0 and x <= battlewidth and\
               y >= 0 and y <= battleheight:
                self.mousedownx = x
                self.mousedowny = y
                self.mousedown = True
        elif button == 3:
            self.mousedrag = False
            if self.get_battle_rect().contains(pygame.Rect(x,y,1,1)):
                for unit in self.selected:
                    unit.target = (unit.offsetx+(x-unit.x),unit.offsety+(y-unit.y))
        self.updateMinimapView(x,y)
        
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
                    for unit in self.selected:
                        if unit.get_rect().contains(pygame.Rect(x,y,1,1)):
                            unit.onDoubleClick()
                    self.selected = Set()
                    for unit in self.player.units:
                        if unit.get_rect().contains(pygame.Rect(x,y,1,1)):
                            self.selected = Set([unit])
                            break
            self.mousedrag = False
            self.mousedown = False
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
