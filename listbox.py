import pygame

from consts import optionheight, boxwidth, boxheight, boxpad, WHITE
from data import images
from button import TextButton
from imagesprite import ImageSprite
from spritecontainer import SpriteContainer

class ListBox(SpriteContainer):
	def __init__(self):
		super(ListBox,self).__init__()
		self.textlist = []
		self.buttonlist = []
		self.buttons = pygame.sprite.Group()
		self.select = -1
		self.background = ImageSprite(images["listboxbg"])
		self.add(self.background)
		self.addSprite(self.background)
	"""
	def setx(self,x):
		self.x = x
		self.background.image.rect.topleft = (self.x,self.y)
		self.updateButtonPosition()
	def sety(self,y):
		self.y = y
		self.background.rect.topleft = (self.x,self.y)
		self.updateButtonPosition()
	def setpos(self,x,y):
		self.x,self.y = x,y
		self.background.rect.topleft = (self.x,self.y)
		self.updateButtonPosition()
	def updateButtonPosition(self):
		for i in range(len(self.buttonlist)):
			self.buttonlist[i].setpos(self.x+boxpad,self.y+i*optionheight+boxpad)
	"""
	
	def addItem(self,text):
		font = pygame.font.Font(None,24)
		img = images["listboxbar"]
		btnwidth = img.get_rect().width
		btnheight = img.get_rect().height/2
		normal = img.subsurface(pygame.Rect(0,0,btnwidth,btnheight))
		selected = img.subsurface(pygame.Rect(0,btnheight,btnwidth,btnheight))
		button = TextButton(text,font,normal,normal,selected)
		self.textlist.append(text)
		self.buttonlist.append(button)
		self.addSprite(button,boxpad,len(self.buttons)*optionheight+boxpad)
		self.buttons.add(button)
		
		if self.select == -1:
			self.selectItem(0)
	
	def selectItem(self,index):
		if index < 0 or index >= len(self.textlist):return
		self.select = index
		for button in self.buttonlist:
			button.recover()
		self.buttonlist[index].under()
	
	def onMouseDown(self,x,y):
		k = int(y/optionheight)
		self.selectItem(k)
	
	def selectedtext(self):
		if self.select == -1:
			return ""
		return self.textlist[self.select]
	
	def draw(self,screen):
		super(ListBox,self).draw(screen)
		self.buttons.draw(screen)
