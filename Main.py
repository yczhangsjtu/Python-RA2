import sys
import pygame

from load import Loader, loadImages
from consts import *
from data import images
from listbox import ListBox
from panels import SelectMapPanel, MapEditor, GameController, GameBackController,\
        MapBackController, StartMenu
from map import Map, initMap
from game import Game

def load():
    global screen
    loader = Loader()
    loader.loadimg("loadimg")
    loader.load(images["loadimg"],screen,loadImages)

def gameInit():
    global ctrlLayer, characterLayer, mapLayer, startMenu, selectMapPanel, editMapPanel,\
        mapEditor, gameController, gameBackController, mapBackController, saveMapPanel
    
    startMenu = StartMenu(startNewGame, selectMap, startMapEditor, quit)
    selectMapPanel = SelectMapPanel(selectMapBack,backToStartMenu)
    editMapPanel = SelectMapPanel(editMap,backToStartMenu)
    mapEditor = MapEditor(gotoMapBackController)
    gameController = GameController(gotoGameBackController)
    gameBackController = GameBackController(gotoSaveGame,goBackToGame,exitGame)
    mapBackController = MapBackController(gotoSaveMap,goBackToMap,exitMap)
    saveMapPanel = SelectMapPanel(saveMapBack,backToMapBackController)
    
    ctrlLayer = startMenu
    characterLayer = None
    mapLayer = None
    
def startNewGame():
    global ctrlLayer, startMenu, mapLayer, characterLayer
    ctrlLayer = gameController
    mapLayer = Map(mapwidth,mapheight)
    characterLayer = Game(mapLayer)

    characterLayer.initNewGame(defaultplayers)
    ctrlLayer.takeOverGame(characterLayer,characterLayer.players[0])
    ctrlLayer.map = mapLayer
    mapLayer.read("./map/%s"%(startMenu.mapfilename))

    loader = Loader()
    loader.load(images["loadmap"],screen,mapLayer.load,\
        [images["bar"].subsurface(0,0,barlength,barheight),(barx,bary)])
    ctrlLayer.minimap = mapLayer.minimap
    characterLayer.running = True

def selectMap():
    global ctrlLayer
    ctrlLayer = selectMapPanel

def exitMap():
    global ctrlLayer,mapLayer
    ctrlLayer = startMenu
    mapLayer = None

def exitGame():
    global ctrlLayer,mapLayer,characterLayer
    ctrlLayer = startMenu
    mapLayer = None
    characterLayer = None
    
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

def gotoSaveMap():
    global ctrlLayer
    ctrlLayer = saveMapPanel

def gotoSaveGame():
    pass

def goBackToMap():
    global ctrlLayer
    ctrlLayer = mapEditor

def goBackToGame():
    global ctrlLayer
    ctrlLayer = gameController

def saveMapBack():
    global ctrlLayer
    mapLayer.write("./map/%s"%ctrlLayer.listBox.selectedtext())
    ctrlLayer = mapBackController

def gotoMapBackController():
    global ctrlLayer
    ctrlLayer = mapBackController

def gotoGameBackController():
    global ctrlLayer
    ctrlLayer = gameBackController

def backToMapBackController():
    global ctrlLayer
    ctrlLayer = mapBackController

def backToStartMenu():
    global ctrlLayer
    ctrlLayer = startMenu
    
def editMap():
    global mapEditor, ctrlLayer, mapLayer
    mapfile = "./map/%s"%(editMapPanel.listBox.selectedtext())
    ctrlLayer = mapEditor
    mapEditor.mapfile = mapfile
    mapLayer = Map(mapwidth,mapheight)
    mapEditor.map = mapLayer
    mapLayer.read(mapfile)
    loader = Loader()
    loader.load(images["loadmap"],screen,mapLayer.load,\
        [images["bar"].subsurface(0,0,barlength,barheight),(barx,bary)])
    ctrlLayer.minimap = mapLayer.minimap
    
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
    pygame.display.set_caption(APP_CAPTION)
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    
    load()
    gameInit()
    
    while True:
        if hasattr(mapLayer,"draw"):
            mapLayer.draw(screen)
        if hasattr(characterLayer,"draw"):
            characterLayer.draw(screen)
        if hasattr(ctrlLayer,"draw"):
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
        
