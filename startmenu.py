import pygame

from data import images
from imagesprite import ImageSprite
from button import Button, RA2Button
from spritecontainer import SpriteContainer
from consts import *


class StartMenu(SpriteContainer):
	def __init__(self, startNewGame, selectMap, startMapEditor, quit):
		super(StartMenu,self).__init__()
		self.background = ImageSprite(images["menu"])
		self.add(self.background)
		self.buttons = pygame.sprite.Group()
		self.startButton = RA2Button("Start")
		self.startButton.setMouseListener(startNewGame)
		self.buttons.add(self.startButton)
		self.addSprite(self.startButton,menubuttonx,menubuttony)
		self.selectButton = RA2Button("Select Map")
		self.selectButton.setMouseListener(selectMap)
		self.buttons.add(self.selectButton)
		self.addSprite(self.selectButton,menubuttonx,self.startButton.bottom())
		self.editButton = RA2Button("Map Editor")
		self.editButton.setMouseListener(startMapEditor)
		self.buttons.add(self.editButton)
		self.addSprite(self.editButton,menubuttonx,self.selectButton.bottom())
		self.exitButton = RA2Button("Exit")
		self.exitButton.setMouseListener(quit)
		self.buttons.add(self.exitButton)
		self.addSprite(self.exitButton,menubuttonx,self.editButton.bottom())
		self.mapfilename = defaultmapfile
		self.mapfile = pygame.sprite.Group()
		self.textsprite = pygame.sprite.Sprite()
		self.mapfile.add(self.textsprite)
		self.setMapFile(self.mapfilename)
	
	def setMapFile(self,text):
		self.mapfilename = text
		font = pygame.font.Font(None,32)
		self.textsprite.image = font.render(text,False,WHITE)
		self.textsprite.rect = self.textsprite.image.get_rect()
		self.textsprite.rect.center = (mapnamex,mapnamey)
	
	def draw(self,surface):
		super(StartMenu,self).draw(surface)
		self.mapfile.draw(surface)
		self.buttons.draw(surface)