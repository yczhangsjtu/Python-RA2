import pygame

from data import images
from imagesprite import ImageSprite
from spritecontainer import ExtendSprite
from consts import *

class Button(ExtendSprite):
	def __init__(self,normal,over,pressed):
		super(Button,self).__init__()
		self.normal = normal
		self.over = over
		self.pressed = pressed
		self.setimage(self.normal)
		self.mouseListener = None
	
	def setMouseListener(self,callback):
		self.mouseListener = callback
		
	def recover(self):
		self.setimage(self.normal)
	
	def shade(self):
		self.setimage(self.over)
	
	def under(self):
		self.setimage(self.pressed)
	
	def onMouseMove(self,x,y):
		if not self.contains(x,y):
			self.recover()
		else:
			self.shade()
			
	def onMouseDown(self,x,y,button):
		if not self.contains(x,y): return
		self.under()
		
	def onMouseUp(self,x,y,button):
		if not self.image == self.pressed: return
		self.recover()
		if self.contains(x,y):
			if self.mouseListener != None:
				self.mouseListener()
				
class TextButton(Button):
	def __init__(self,text,font,normal,over,pressed):
		textimg = font.render(text,False,WHITE)
		textrect = textimg.get_rect()
		
		normalimg = normal.copy()
		textrect.center = normalimg.get_rect().center
		normalimg.blit(textimg,textrect)
		
		overimg = over.copy()
		textrect.center = overimg.get_rect().center
		overimg.blit(textimg,textrect)
		
		pressedimg = pressed.copy()
		textrect.center = pressedimg.get_rect().center
		pressedimg.blit(textimg,textrect)
		
		super(TextButton,self).__init__(normalimg,overimg,pressedimg)

class RA2Button(TextButton):
	def __init__(self,text):
		font = pygame.font.Font(None,26)
		img = images["menubttn"]
		btnwidth = img.get_rect().width/3
		btnheight = img.get_rect().height
		normalimg = images["menubttn"].subsurface(0,0,btnwidth,btnheight)
		overimg = images["menubttn"].subsurface(btnwidth,0,btnwidth,btnheight)
		pressedimg = images["menubttn"].subsurface(btnwidth*2,0,btnwidth,btnheight)
		super(RA2Button,self).__init__(text,font,normalimg,overimg,pressedimg)

class PalatteButton(Button):
	def __init__(self,col,row):
		normal = images["ground"].subsurface(col*gridwidth,row*gridheight,gridwidth,gridheight)
		over = images["lightground"].subsurface(col*gridwidth,row*gridheight,gridwidth,gridheight)
		pressed = over
		super(PalatteButton,self).__init__(normal,over,pressed)

class GameCtrlButton(Button):
	def __init__(self,index):
		img = images["button%d%d"%(index/10,index%10)]
		normal = img.subsurface(0,0,img.get_width()/2,img.get_height())
		over = img.subsurface(img.get_width()/2,0,img.get_width()/2,img.get_height())
		pressed = over
		super(GameCtrlButton,self).__init__(normal,over,pressed)

class GamePanelButton(Button):
	def __init__(self,name):
		img = images[name]
		normal = img.subsurface(0,0,img.get_width()/2,img.get_height())
		over = normal
		pressed = img.subsurface(img.get_width()/2,0,img.get_width()/2,img.get_height())
		super(GamePanelButton,self).__init__(normal,over,pressed)
