import sys

from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample2, Button, ButtonState

from load import RA2Loading
from button import RA2Button, PalatteButton
from map import Map
from listbox import ListBox
from consts import menubuttonx, menubuttony, listboxx, listboxy,\
	gridwidth, gridheight, colorbuttonx, colorbuttony

def main():
	loadList = [
		{"name":"loadimg","path":"./img/glsl.png"},
		{"name":"menubttn","path":"./img/mnbttn.png"},
		{"name":"menu","path":"./img/menu.png"},
		{"name":"ctrlpanel","path":"./img/ctrlpanel.png"},
		{"name":"editorpanel","path":"./img/editorpanel.png"},
		{"name":"ground","path":"./img/ground.png"},
		{"name":"lightground","path":"./img/lightground.png"},
	]
	loadingPage = RA2Loading()
	addChild(loadingPage)
	
	def loadComplete(result):
		global dataList
		loadingPage.remove()
		dataList = result
		gameInit()
	
	LoadManage.load(loadList, loadingPage.setProgress, loadComplete)

def gameInit():
	global ctrlLayer, characterLayer, mapLayer
	mapLayer = Sprite()
	addChild(mapLayer)
	characterLayer = Sprite()
	addChild(characterLayer)
	ctrlLayer = Sprite()
	addChild(ctrlLayer)
	fps = FPS()
	addChild(fps)
	
	initMapEditor()
	initCtrlLayer()

def initCtrlLayer():
	global ctrlLayer, startButton, mapEditorButton, startMenu
	
	startMenu = Sprite()
	ctrlLayer.addChild(startMenu)
	startMenu.addChild(Bitmap(BitmapData(dataList["menu"])))
	
	startButton = RA2Button("Start",dataList)
	startButton.x = menubuttonx
	startButton.y = menubuttony
	startMenu.addChild(startButton)
	
	mapEditorButton = RA2Button("Map Editor",dataList)
	mapEditorButton.x = menubuttonx
	mapEditorButton.y = menubuttony+mapEditorButton.height
	startMenu.addChild(mapEditorButton)
	
	def clickStartButton(e):
		startNewGame()
	def clickMapEditorButton(e):
		startMapEditor()
		
	startButton.addEventListener(MouseEvent.MOUSE_UP, clickStartButton)
	mapEditorButton.addEventListener(MouseEvent.MOUSE_UP, clickMapEditorButton)
	stage.addEventListener(KeyboardEvent.KEY_DOWN, keydown)
	stage.addEventListener(KeyboardEvent.KEY_UP, keyup)
	
	initCtrlPanel()
	initEditorPanel()
	
def initCtrlPanel():
	global ctrlPanel
	ctrlPanel = Sprite()
	ctrlPanel.addChild(Bitmap(BitmapData(dataList["ctrlpanel"])))
	
def initEditorPanel():
	global editorPanel, listBox, editButton, backButton, ctrlLayer
	editorPanel = Sprite()
	editorPanel.addChild(Bitmap(BitmapData(dataList["editorpanel"])))
	listBox = ListBox()
	listBox.add("map0.txt")
	listBox.add("map1.txt")
	listBox.add("map2.txt")
	listBox.add("map3.txt")
	listBox.x = listboxx
	listBox.y = listboxy
	editorPanel.addChild(listBox)
	
	editButton = RA2Button("Edit",dataList)
	editButton.x = menubuttonx
	editButton.y = menubuttony
	editorPanel.addChild(editButton)
	def onClickEditButton(e):
		editMap("./map/%s"%(listBox.selectedtext()))
	editButton.addEventListener(MouseEvent.MOUSE_UP,onClickEditButton)
	
	backButton = RA2Button("Back",dataList)
	backButton.x = menubuttonx
	backButton.y = menubuttony+backButton.height
	editorPanel.addChild(backButton)
	def onClickBackButton(e):
		goBackToStartMenu()
	backButton.addEventListener(MouseEvent.MOUSE_UP,onClickBackButton)

def initMapEditor():
	global colorPanel
	colorPanel = Sprite()
	colorPanel.addChild(Bitmap(BitmapData(dataList["ctrlpanel"])))
	grassButton = PalatteButton(0,0,dataList)
	grassButton.x = colorbuttonx
	grassButton.y = colorbuttony
	colorPanel.addChild(grassButton)
	waterButton = PalatteButton(3,5,dataList)
	waterButton.x = colorbuttonx + gridwidth
	waterButton.y = colorbuttony
	colorPanel.addChild(waterButton)

def keydown(e):
	global map
	if e.keyCode == KeyCode.KEY_RIGHT:
		map.scrollv = [-1,0]
	elif e.keyCode == KeyCode.KEY_LEFT:
		map.scrollv = [1,0]
	elif e.keyCode == KeyCode.KEY_UP:
		map.scrollv = [0,1]
	elif e.keyCode == KeyCode.KEY_DOWN:
		map.scrollv = [0,-1]
		
def keyup(e):
	global map
	map.scrollv = (0,0)
	
def goBackToStartMenu():
	editorPanel.remove()
	ctrlLayer.addChild(startMenu)
	
def startMapEditor():
	global startMenu, editorPanel, map, mapLayer
	startMenu.remove()
	ctrlLayer.addChild(editorPanel)

def editMap(mapfile):
	global colorPanel, editorPanel, ctrlLayer, map
	map = Map(200,200,mapLayer)
	map.read(mapfile)
	map.load(dataList)
	editorPanel.remove()
	ctrlLayer.addChild(colorPanel)
	colorPanel.addEventListener(Event.ENTER_FRAME, mainloop)
	
def startNewGame():
	global startMenu, ctrlPanel, map, mapLayer
	startMenu.remove()
	ctrlLayer.addChild(ctrlPanel)
	
	map = Map(200,200,mapLayer)
	map.read("./map/map0.txt")
	map.load(dataList)
	ctrlPanel.addEventListener(Event.ENTER_FRAME, mainloop)

def mainloop(e):
	map.scroll()
	
init(16, "Red Alert", 800, 600, main)
