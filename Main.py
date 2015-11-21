import sys

from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample2, Button, ButtonState

from load import RA2Loading
from button import RA2Button, PalatteButton
from map import Map, initMap, groundData
from listbox import ListBox
from consts import menubuttonx, menubuttony, listboxx, listboxy,\
	gridwidth, gridheight, colorbuttonx, colorbuttony, mousescrollwidth,\
	battlewidth, battleheight

def main():
	loadList = [
		{"name":"loadimg","path":"./img/glsl.png"},
		{"name":"menubttn","path":"./img/mnbttn.png"},
		{"name":"menu","path":"./img/menu.png"},
		{"name":"ctrlpanel","path":"./img/ctrlpanel.png"},
		{"name":"editorpanel","path":"./img/editorpanel.png"},
		{"name":"ground","path":"./img/ground.png"},
		{"name":"lightground","path":"./img/lightground.png"},
		{"name":"red","path":"./img/red.png"},
		{"name":"green","path":"./img/green.png"},
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
	
	initMap(dataList)
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
	
	exitButton = RA2Button("Exit",dataList)
	exitButton.x = menubuttonx
	exitButton.y = menubuttony+mapEditorButton.height*2
	startMenu.addChild(exitButton)
	
	def clickStartButton(e):
		startNewGame()
	def clickMapEditorButton(e):
		startMapEditor()
	def clickExitButton(e):
		exit(0)
		
	startButton.addEventListener(MouseEvent.MOUSE_UP, clickStartButton)
	mapEditorButton.addEventListener(MouseEvent.MOUSE_UP, clickMapEditorButton)
	exitButton.addEventListener(MouseEvent.MOUSE_UP, clickExitButton)
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
	global colorPanel, paint
	paint = 1
	colorPanel = Sprite()
	colorPanel.addChild(Bitmap(BitmapData(dataList["ctrlpanel"])))
	grassButton = PalatteButton(0,0,dataList)
	grassButton.x = colorbuttonx
	grassButton.y = colorbuttony
	colorPanel.addChild(grassButton)
	waterButton = PalatteButton(0,1,dataList)
	waterButton.x = colorbuttonx + gridwidth
	waterButton.y = colorbuttony
	colorPanel.addChild(waterButton)
	saveButton = RA2Button("Save",dataList)
	saveButton.x = menubuttonx
	saveButton.y = colorbuttony + 100
	colorPanel.addChild(saveButton)
	backButton = RA2Button("Back",dataList)
	backButton.x = menubuttonx
	backButton.y = colorbuttony + saveButton.height + 100
	colorPanel.addChild(backButton)
	def onClickGrassButton(e):
		global paint
		paint = 1
	def onClickWaterButton(e):
		global paint
		paint = 0
	def onClickSaveButton(e):
		global map, mapfile
		map.write(mapfile)
	def onClickBackButton(e):
		global map, mapfile
		mapfile = ""
		goBackToEditorPanel()
	grassButton.addEventListener(MouseEvent.MOUSE_UP,onClickGrassButton)
	waterButton.addEventListener(MouseEvent.MOUSE_UP,onClickWaterButton)
	saveButton.addEventListener(MouseEvent.MOUSE_UP,onClickSaveButton)
	backButton.addEventListener(MouseEvent.MOUSE_UP,onClickBackButton)
	
def keydown(e):
	global map
	if e.keyCode == KeyCode.KEY_LEFT:
		map.scrollv[0] = 1
	elif e.keyCode == KeyCode.KEY_RIGHT:
		map.scrollv[1] = 1
	elif e.keyCode == KeyCode.KEY_UP:
		map.scrollv[2] = 1
	elif e.keyCode == KeyCode.KEY_DOWN:
		map.scrollv[3] = 1
		
def keyup(e):
	global map
	if e.keyCode == KeyCode.KEY_LEFT:
		map.scrollv[0] = 0
	elif e.keyCode == KeyCode.KEY_RIGHT:
		map.scrollv[1] = 0
	elif e.keyCode == KeyCode.KEY_UP:
		map.scrollv[2] = 0
	elif e.keyCode == KeyCode.KEY_DOWN:
		map.scrollv[3] = 0
	
def goBackToStartMenu():
	editorPanel.remove()
	ctrlLayer.addChild(startMenu)

def goBackToEditorPanel():
	global map
	map.clear()
	colorPanel.remove()
	ctrlLayer.addChild(editorPanel)
	colorPanel.removeEventListener(Event.ENTER_FRAME, editorloop)
	ctrlLayer.removeEventListener(MouseEvent.MOUSE_MOVE, onEditMouseMove)
	ctrlLayer.removeEventListener(MouseEvent.MOUSE_DOWN, onEditMouseDown)
	ctrlLayer.removeEventListener(MouseEvent.MOUSE_UP, onEditMouseUp)

def startMapEditor():
	global startMenu, editorPanel, map, mapLayer
	startMenu.remove()
	ctrlLayer.addChild(editorPanel)

def editMap(filename):
	global colorPanel, editorPanel, ctrlLayer, map, mousepressed, mapfile
	mapfile = filename
	map = Map(200,200,mapLayer)
	map.read(filename)
	map.load()
	editorPanel.remove()
	ctrlLayer.addChild(colorPanel)
	colorPanel.addEventListener(Event.ENTER_FRAME, editorloop)
	ctrlLayer.addEventListener(MouseEvent.MOUSE_MOVE, onEditMouseMove)
	ctrlLayer.addEventListener(MouseEvent.MOUSE_DOWN, onEditMouseDown)
	ctrlLayer.addEventListener(MouseEvent.MOUSE_UP, onEditMouseUp)
	mousepressed = False
	
def startNewGame():
	global startMenu, ctrlPanel, map, mapLayer
	startMenu.remove()
	ctrlLayer.addChild(ctrlPanel)
	
	map = Map(200,200,mapLayer)
	map.read("./map/map0.txt")
	map.load()
	ctrlPanel.addEventListener(Event.ENTER_FRAME, mainloop)
	
def updateScrollV():
	global mousex, mousey, map
	if mousex > 0 and mousex < mousescrollwidth:
		map.scrollv[4] = 1
	else:
		map.scrollv[4] = 0
	if mousex > stage.width - mousescrollwidth and mousex < stage.width:
		map.scrollv[5] = 1
	else:
		map.scrollv[5] = 0
	if mousey > 0 and mousey < mousescrollwidth:
		map.scrollv[6] = 1
	else:
		map.scrollv[6] = 0
	if mousey > stage.height - mousescrollwidth and mousey < stage.height:
		map.scrollv[7] = 1
	else:
		map.scrollv[7] = 0

def onEditMouseMove(e):
	global mousex, mousey, map, mousepressed
	mousex, mousey = e.offsetX, e.offsetY
	updateScrollV()
	if mousepressed: map.paint(mousex,mousey,paint)
	
def onEditMouseDown(e):
	global mousex, mousey, paint, mousepressed
	mousepressed = True
	
def onEditMouseUp(e):
	global mousepressed
	mousepressed = False
	
def editorloop(e):
	map.scroll()
	
def mainloop(e):
	pass
	map.scroll()
	
init(16, "Red Alert", 800, 600, main)
