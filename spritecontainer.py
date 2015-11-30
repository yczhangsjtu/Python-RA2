import pygame

class ExtendSprite(pygame.sprite.Sprite):
	def __init__(self):
		super(ExtendSprite,self).__init__()
		self.x,self.y = 0,0
	
	def setimage(self,image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)
		
	def bottom(self):
		return self.rect.bottom
	def right(self):
		return self.rect.right
	def left(self):
		return self.rect.left
	def top(self):
		return self.rect.top
	
	def width(self):
		return self.rect.width
		
	def height(self):
		return self.rect.height
	
	def contains(self,x,y):
		return self.rect.contains(pygame.Rect(x,y,1,1))
	
	def setx(self,x):
		self.x = x
		self.rect.topleft = (self.x, self.y)
	
	def sety(self,y):
		self.y = y
		self.rect.topleft = (self.x, self.y)
	
	def setpos(self,x,y):
		self.x, self.y = x, y
		self.rect.topleft = (self.x, self.y)
	
	def onMouseDown(self,x,y,button):
		pass
	def onMouseUp(self,x,y,button):
		pass
	def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
		pass
	def onKeyDown(self,keyCode,mod):
		pass
	def onKeyUp(self,keyCode,mod):
		pass

class SpriteContainer(pygame.sprite.Group):
	def __init__(self):
		super(SpriteContainer,self).__init__()
		self.spriteset = []
		self.x,self.y = 0,0
	
	def addSprite(self,sprite,x=0,y=0):
		self.spriteset.append(sprite)
		sprite.offsetx = x
		sprite.offsety = y
		sprite.setpos(self.x+sprite.offsetx,self.y+sprite.offsety)
		
	def setx(self,x):
		self.x = x
		self.updateSprites()
	def sety(self,y):
		self.y = y
		self.updateSprites()
	def setpos(self,x,y):
		self.x,self.y = x,y
		self.updateSprites()
	def movex(self,dx):
		self.setx(self.x+dx)
	def movey(self,dy):
		self.sety(self.y+dy)
	def move(self,dx,dy):
		self.setpos(self.x+dx,self.y+dy)
	def updateSprites(self):
		for sprite in self.spriteset:
			sprite.setpos(self.x+sprite.offsetx,self.y+sprite.offsety)
	def draw(self,screen):
		super(SpriteContainer,self).draw(screen)
	def onMouseDown(self,x,y,button):
		for sprite in self.spriteset:
			sprite.onMouseDown(x,y,button)
	def onMouseUp(self,x,y,button):
		for sprite in self.spriteset:
			sprite.onMouseUp(x,y,button)
	def onMouseMove(self,x,y,button1=None,button2=None,button3=None):
		for sprite in self.spriteset:
			sprite.onMouseMove(x,y)
	def onKeyDown(self,keyCode,mod):
		for sprite in self.spriteset:
			sprite.onKeyDown(keyCode,mod)
	def onKeyUp(self,keyCode,mod):
		for sprite in self.spriteset:
			sprite.onKeyUp(keyCode,mod)
