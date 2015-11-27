import pygame

from listbox import ListBox
from data import images
from button import RA2Button, PalatteButton
from imagesprite import ImageSprite
from spritecontainer import SpriteContainer
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
		minimapw = self.minimap.get_rect().width
		minimaph = self.minimap.get_rect().height
		if x >= minimapx and x <= minimapx + minimapw and\
			 y >= minimapy and y <= minimapy + minimaph:
			self.map.x = -(x-minimapx)*self.map.groundwidth/minimapw
			self.map.y = -(y-minimapy)*self.map.groundheight/minimaph
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
		self.background = ImageSprite(images["ctrlpanel"])
		self.add(self.background)
		self.map = None
		self.mousedrag = False
		self.mousedown = False
		self.mouseMinimapDown = False
		self.characters = None
		
		self.buttons = pygame.sprite.Group()
		self.minimap = images["allyflag"]
	
	def save(self):
		pass
	
	def draw(self,screen):
		super(GameController,self).draw(screen)
		self.buttons.draw(screen)
		minimapw = self.minimap.get_rect().width
		minimaph = self.minimap.get_rect().height
		if self.mousedrag:
			x = min(self.mousedownx,self.mousex)
			y = min(self.mousedowny,self.mousey)
			w = abs(self.mousedownx-self.mousex)
			h = abs(self.mousedowny-self.mousey)
			rect = pygame.Rect(x,y,w,h)
			pygame.draw.rect(screen,WHITE,rect,1)
		screen.blit(self.minimap,(minimapx,minimapy))
		x = (-self.map.x) * minimapw / self.map.groundwidth + minimapx
		y = (-self.map.y) * minimaph / self.map.groundheight + minimapy
		w = battlewidth * self.minimap.get_rect().width / self.map.groundwidth
		h = battleheight * self.minimap.get_rect().height / self.map.groundheight
		view = pygame.Rect(x,y,w,h)
		pygame.draw.rect(screen,RED,view,1)
	
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
		self.updateMinimapView(x,y)
	
	def updateMinimapView(self,x,y):
		minimapw = self.minimap.get_rect().width
		minimaph = self.minimap.get_rect().height
		if x >= minimapx and x <= minimapx + minimapw and\
			 y >= minimapy and y <= minimapy + minimaph:
			self.map.x = -(x-minimapx)*self.map.groundwidth/minimapw
			self.map.y = -(y-minimapy)*self.map.groundheight/minimaph
			self.map.fitOffset()
			self.mouseMinimapDown = True
		
	def onMouseUp(self,x,y,button):
		super(GameController,self).onMouseUp(x,y,button)
		if button == 1:
			if self.mousedrag:
				x = min(self.mousedownx,self.mousex)
				y = min(self.mousedowny,self.mousey)
				w = abs(self.mousedownx-self.mousex)
				h = abs(self.mousedowny-self.mousey)
				rect = pygame.Rect(x,y,w,h)
				for unit in self.characters.unitSet:
					if rect.contains(unit.get_rect()):
						if unit.regionselectable:
							unit.selected = True
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
