from pylash.display import Sprite
from pylash.text import TextField
from pylash.events import Event, MouseEvent
from consts import optionheight, boxwidth, boxheight

class ListBox(Sprite):
	def __init__(self):
		super(ListBox,self).__init__()
		self.textlist = []
		self.select = -1
		self.background = Sprite()
		self.selectBar = Sprite()
		self.addChild(self.background)
		self.selectBar.x = 0
		self.selectBar.graphics.beginFill("red")
		self.selectBar.graphics.drawRect(0,0,boxwidth,optionheight)
		self.selectBar.graphics.endFill()
		self.background.graphics.lineStyle(2,"white")
		#self.background.graphics.beginFill("black")
		self.background.graphics.drawRect(0,0,boxwidth,boxheight)
		#self.background.graphics.endFill()
		self.addEventListener(MouseEvent.MOUSE_DOWN, self.mouseClicked)
	
	def add(self,text):
		textfield = TextField()
		textfield.text = text
		textfield.textColor = "white"
		textfield.size = optionheight
		textfield.x = 0
		textfield.y = len(self.textlist) * optionheight
		self.addChild(textfield)
		self.textlist.append(text)
		if self.select == -1:
			self.select = 0
			self.background.addChild(self.selectBar)
			self.selectBar.y = self.select * optionheight
	
	def mouseClicked(self,e):
		k = int((e.offsetY - self.y)/ optionheight)
		if k >= 0 and k < len(self.textlist):
			self.select = k
			self.selectBar.y = self.select * optionheight
	
	def selectedtext(self):
		if self.select == -1:
			return ""
		return self.textlist[self.select]
