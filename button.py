from pylash.ui import Button
from pylash.display import Sprite, BitmapData, Bitmap
from pylash.text import TextField
from consts import gridwidth, gridheight

class RA2Button(Button):
	def __init__(self, text, dataList):
		btnImage = dataList["menubttn"]
		btnwidth = int(btnImage.width()/3)
		
		normal = Sprite()
		normal.addChild(Bitmap(BitmapData(btnImage,0,0,btnwidth)))
		txt = TextField()
		txt.text = text
		txt.textColor = "white"
		txt.size = 20
		txt.x = (normal.width - txt.width) / 2
		txt.y = (normal.height - txt.height) / 2
		normal.addChild(txt)
        
		txt = TextField()
		txt.text = text
		txt.textColor = "white"
		txt.size = 20
		txt.x = (normal.width - txt.width) / 2
		txt.y = (normal.height - txt.height) / 2
		over = Sprite()
		over.addChild(Bitmap(BitmapData(btnImage,btnwidth,0,btnwidth)))
		over.addChild(txt)
        
		txt = TextField()
		txt.text = text
		txt.textColor = "white"
		txt.size = 20
		txt.x = (normal.width - txt.width) / 2
		txt.y = (normal.height - txt.height) / 2
		pressed = Sprite()
		pressed.addChild(Bitmap(BitmapData(btnImage,btnwidth*2,0,btnwidth)))
		pressed.addChild(txt)
		
		super(RA2Button,self).__init__(normal,over,pressed,None)

class PalatteButton(Button):
	def __init__(self, i, j, dataList):
		btnImage = dataList["ground"]
		lightBtnImage = dataList["lightground"]
		self.index = j * 4 + i + 1
		offsetx = i * gridwidth
		offsety = j * gridheight
		normal = Sprite()
		normal.addChild(Bitmap(BitmapData(btnImage,offsetx,offsety,gridwidth,gridheight)))
		over = Sprite()
		over.addChild(Bitmap(BitmapData(lightBtnImage,offsetx,offsety,gridwidth,gridheight)))
		super(PalatteButton,self).__init__(normal,over,None,None)
		
