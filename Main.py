import sys
import pygame

"""
from button import RA2Button, PalatteButton
from map import Map, initMap, groundData
from game import Game
"""
from load import Loader
from consts import *
from data import images
from startmenu import StartMenu
from listbox import ListBox
from panels import SelectMapPanel, MapEditor, GameController
from map import Map, initMap
from game import Game
from building import initBuildingAnimations
from infantry import initInfantryAnimations
from vehicle import initVehicleAnimations

def load():
	global screen
	loader = Loader()
	
	def loadImages(progress):
		N = len(loadList)+1
		n = 0
		for imgname in loadList:
			loader.loadimg(imgname)
			n += 1
			progress[0] = float(n)/N
		initMap()
		initBuildingAnimations()
		initInfantryAnimations()
		initVehicleAnimations()
		progress[0] = 1
	
	loader.loadimg("loadimg")
	loader.load(images["loadimg"],screen,loadImages)

def gameInit():
	global ctrlLayer, characterLayer, mapLayer, startMenu, selectMapPanel, editMapPanel, mapfile,\
		mapEditor, gameController
	
	mapfile = "map0.txt"

	startMenu = StartMenu(startNewGame, selectMap, startMapEditor, quit)
	selectMapPanel = SelectMapPanel(selectMapBack,backToStartMenu)
	editMapPanel = SelectMapPanel(editMap,backToStartMenu)
	mapEditor = MapEditor(backToStartMenu)
	gameController = GameController()
	
	ctrlLayer = startMenu
	characterLayer = pygame.sprite.Group()
	mapLayer = pygame.sprite.Group()
	
def startNewGame():
	global ctrlLayer, startMenu, mapLayer, characterLayer
	mapfile = "./map/%s"%(startMenu.mapfilename)
	ctrlLayer = gameController
	mapLayer = Map(mapwidth,mapheight)
	characterLayer = Game(mapLayer)
	characterLayer.initNewGame(defaultplayers)
	ctrlLayer.characters = characterLayer
	ctrlLayer.map = mapLayer
	mapLayer.read(mapfile)
	loader = Loader()
	loader.load(images["loadmap"],screen,mapLayer.load,\
		[images["bar"].subsurface(0,0,barlength,barheight),(barx,bary)])

def selectMap():
	global ctrlLayer
	ctrlLayer = selectMapPanel
	
def selectMapBack():
	global ctrlLayer
	ctrlLayer = startMenu
	mapfile = selectMapPanel.listBox.selectedtext()
	startMenu.setMapFile(mapfile)

def startMapEditor():
	global ctrlLayer
	ctrlLayer = editMapPanel
	
def quit():
	pygame.quit()
	exit(0)

def backToStartMenu():
	global ctrlLayer, mapLayer
	ctrlLayer = startMenu
	mapLayer = pygame.sprite.Group()
	
def editMap():
	global mapEditor, ctrlLayer, mapLayer, mapfile
	mapfile = "./map/%s"%(editMapPanel.listBox.selectedtext())
	ctrlLayer = mapEditor
	mapEditor.mapfile = mapfile
	mapLayer = Map(mapwidth,mapheight)
	mapEditor.map = mapLayer
	mapLayer.read(mapfile)
	loader = Loader()
	loader.load(images["loadmap"],screen,mapLayer.load,\
		[images["bar"].subsurface(0,0,barlength,barheight),(barx,bary)])
	
def onMouseDown(x,y,button):
	if hasattr(ctrlLayer,"onMouseDown"):
		ctrlLayer.onMouseDown(x,y,button)
	if hasattr(characterLayer,"onMouseDown"):
		characterLayer.onMouseDown(x,y,button)
	if hasattr(mapLayer,"onMouseDown"):
		mapLayer.onMouseDown(x,y,button)
		
def onMouseUp(x,y,button):
	if hasattr(ctrlLayer,"onMouseUp"):
		ctrlLayer.onMouseUp(x,y,button)
	if hasattr(characterLayer,"onMouseUp"):
		characterLayer.onMouseUp(x,y,button)
	if hasattr(mapLayer,"onMouseUp"):
		mapLayer.onMouseUp(x,y,button)
		
def onMouseMove(x,y,button1=None,button2=None,button3=None):
	if hasattr(ctrlLayer,"onMouseMove"):
		ctrlLayer.onMouseMove(x,y,button1,button2,button3)
	if hasattr(characterLayer,"onMouseMove"):
		characterLayer.onMouseMove(x,y,button1,button2,button3)
	if hasattr(mapLayer,"onMouseMove"):
		mapLayer.onMouseMove(x,y,button1,button2,button3)

def onKeyDown(keyCode,mod):
	if keyCode == pygame.K_ESCAPE:
		pygame.quit()
		exit(0)
	if hasattr(ctrlLayer,"onKeyDown"):
		ctrlLayer.onKeyDown(keyCode,mod)
		
def onKeyUp(keyCode,mod):
	if hasattr(ctrlLayer,"onKeyUp"):
		ctrlLayer.onKeyUp(keyCode,mod)
	
def update(t):
	if hasattr(ctrlLayer,"update"):
		ctrlLayer.update()
	if hasattr(characterLayer,"update"):
		characterLayer.update()
	if hasattr(mapLayer,"update"):
		mapLayer.update()

if __name__ == "__main__":
	global screen, clock, startMenu
	pygame.init()
	size = (winwidth,winheight)
	screen = pygame.display.set_mode(size)
	screen.convert_alpha()
	pygame.display.set_caption(APP_CAPTION)
	pygame.display.toggle_fullscreen()
	clock = pygame.time.Clock()
	
	load()
	gameInit()
	
	while True:
		mapLayer.draw(screen)
		characterLayer.draw(screen)
		ctrlLayer.draw(screen)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				onMouseDown(event.pos[0],event.pos[1],event.button)
			if event.type == pygame.MOUSEBUTTONUP:
				onMouseUp(event.pos[0],event.pos[1],event.button)
			if event.type == pygame.MOUSEMOTION:
				onMouseMove(*(event.pos+event.buttons))
			if event.type == pygame.KEYDOWN:
				onKeyDown(event.key,event.mod)
			if event.type == pygame.KEYUP:
				onKeyUp(event.key,event.mod)
		clock.tick(16)
		update(pygame.time.get_ticks())
		
