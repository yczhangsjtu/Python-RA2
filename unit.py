from pylash.display import Sprite, Bitmap, BitmapData, Animation, AnimationSet, AnimationPlayMode
from pylash.events import AnimationEvent, MouseEvent

from data import unitData
from consts import animationspeed

class Unit(Sprite):
	def __init__(self,name,owner,datalist):
		super(Unit,self).__init__()
		self.datalist = datalist
		self.init(name,owner)
		self.addEventListener(MouseEvent.MOUSE_DOWN,self.onClick)
		self.addEventListener(MouseEvent.DOUBLE_CLICK,self.onDoubleClick)
	
	def init(self,name,owner):
		self.removeAllChildren()
		data = unitData[name]
		image = self.datalist[name]
		self.type = data["type"]
		self.owner = owner
		offset = data["owneroffset"] * owner
		list = data["animationlist"]
		self.animationSet = AnimationSet()
		self.animationSet.x = -data["origin"][0]
		self.animationSet.y = -data["origin"][1]
		self.addChild(self.animationSet)
		self.currentAnimation = data["origanim"]
		self.speed = data["speed"]
		self.doubleclick = data["doubleclick"]
		self.selected = False
		self.next = {}
		self.stopmethod = {}
		self.framemethod = {}
		for animationName in list:
			animationdata = list[animationName]
			offsetx,offsety,w,h,n = animationdata["num"]
			offsety += offset
			framelist = Animation.divideUniformSizeFrames(w, h, n, 1)
			skip = animationdata["skip"]
			framelist = [framelist[0][::skip+1]]
			bmpdata = BitmapData(image, offsetx, offsety, w, h)
			animation = Animation(bmpdata, framelist)
			animation.playMode = AnimationPlayMode.HORIZONTAL
			animation.speed = animationspeed
			animation.loop = animationdata["loop"]
			animation.name = animationName
			self.stopmethod[animationName] = animationdata["stopmethod"]
			self.framemethod[animationName] = animationdata["framemethod"]
			self.next[animationName] = animationdata["next"]
			animation.addEventListener(AnimationEvent.STOP,self.animationStop)
			animation.addEventListener(AnimationEvent.CHANGE_FRAME,self.animate)
			self.animationSet.addAnimation(animationName,animation)
		self.changeAnimation(self.currentAnimation)
	
	def changeAnimation(self,animation):
		self.currentAnimation = animation
		self.animationSet.changeAnimation(animation)
	
	def animate(self,e):
		framemethod = self.framemethod[self.currentAnimation]
		if framemethod != None:
			framemethod = framemethod.split(' ')
			getattr(Unit,framemethod[0])(self,*framemethod[1:])
	
	def animationStop(self,e):
		stopmethod = self.stopmethod[self.currentAnimation]
		if stopmethod != None:
			stopmethod = stopmethod.split(' ')
			getattr(Unit,stopmethod[0])(self,*stopmethod[1:])
			return
		next = self.next[self.currentAnimation]
		if next != None:
			self.changeAnimation(next)
	
	def transform(self,name):
		self.init(name,self.owner)
	
	def onClick(self,e):
		if not self.selected:
			self.selected = True
		else:
			if self.doubleclick != None:
				self.changeAnimation(self.doubleclick)

	def onDoubleClick(self,e):
		self.selected = False
		if self.doubleclick != None:
			self.changeAnimation(self.doubleclick)
	
	def moven(self):
		self.y -= self.speed
	def movenw(self):
		self.x -= self.speed
		self.y -= self.speed
	def movew(self):
		self.x -= self.speed
	def movesw(self):
		self.x -= self.speed
		self.y -= self.speed
	def moves(self):
		self.y += self.speed
	def movese(self):
		self.x += self.speed
		self.y -= self.speed
	def movee(self):
		self.x += self.speed
	def movene(self):
		self.x += self.speed
		self.y -= self.speed
		