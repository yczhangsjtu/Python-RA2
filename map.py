import pygame

from spritecontainer import SpriteContainer
from imagesprite import ImageSprite
from data import images
from consts import *

greenBitmap = None
redBitmap = None

def getAbsPos(col,row,center=False):
	x = gridwidth/2 * (col-1)
	y = gridheight*row - gridheight/2*((col+1)%2)
	if center:
		x,y = x+gridwidth/2,y+gridheight/2
	return x,y

def getGridPos(x,y):
	X,Y = float(x*2)/gridwidth,float(y*2)/gridheight
	X,Y = int((X+Y+1)/2), int(-X+Y+1+1000)/2-500
	row,col = (X+Y)/2,X-Y
	return col,row

def getGridCenter(x,y):
	col,row = getGridPos(x,y)
	return getAbsPos(col,row,True)
		
def initMap():
	offsety = gridheight
	offsetx = 0
	images["water"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth
	images["west"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*2
	images["south"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*3
	images["north"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*4
	images["east"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsety = 0
	offsetx = 0
	images["grass"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth
	images["northwest"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*2
	images["southwest"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*3
	images["northeast"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)
	offsetx = gridwidth*4
	images["southeast"] = images["ground"].subsurface(offsetx,offsety,gridwidth,gridheight)

class Map(SpriteContainer):
	def __init__(self, row, col):
		super(Map,self).__init__()
		self.map = [[1]*row for i in range(col)]
		self.width = col
		self.height = row
		self.scrollv = [0,0,0,0,0,0,0,0]
		self.groundwidth = self.width * gridwidth/2
		self.groundheight = self.height * gridheight
		self.groundimg = pygame.Surface([self.groundwidth,self.groundheight])
		self.ground = ImageSprite(self.groundimg)
		self.groundbox = pygame.sprite.Group()
		self.groundbox.add(self.ground)
		self.addSprite(self.ground)
		self.minimap = pygame.Surface([self.width,self.height])
		self.minimapw = self.width
		self.minimaph = self.height
		self.minimapvieww = battlewidth * self.minimapw / self.groundwidth
		self.minimapviewh = battleheight * self.minimaph / self.groundheight
		
	def read(self,filename):
		with open(filename) as f:
			for j in range(self.height):
				line = f.readline().strip('\n')
				nums = line.split(" ")
				for i in range(self.width):
					self.map[i][j] = int(nums[i])
	
	def write(self,filename):
		with open(filename,"w") as f:
			for j in range(self.height):
				line = " ".join(map(str,[self.map[i][j] for i in range(self.width)]))
				f.write("%s\n"%line)
	
	def load(self,process):
		process[0],N = 0,self.width*self.height
		for i in range(self.width):
			for j in range(self.height):
				self.setBitmap(i,j)
				process[0] = float(i*self.height+j)/N
		process[0] = 1
	
	def paint(self,x,y,paint):
		if x >= 0 and x <= battlewidth and y >= 0 and y <= battleheight:
			col,row = self.getGridPos(x,y)
			self.map[col][row] = paint
			self.setBitmap(col,row)
			self.setNeighborBitmap(col,row)
	
	def setBitmap(self,col,row):
		if not self.validPos(col,row): return
		k = self.map[col][row]
		x,y = getAbsPos(col,row)
		if k == 1:
			self.groundimg.blit(images["grass"],(x,y))
			pygame.draw.rect(self.minimap,GREEN,pygame.Rect(col,row,1,1),1)
			if self.northeastv(col,row) == 0:
				self.groundimg.blit(images["northeast"],(x,y))
			if self.northwestv(col,row) == 0:
				self.groundimg.blit(images["northwest"],(x,y))
			if self.southeastv(col,row) == 0:
				self.groundimg.blit(images["southeast"],(x,y))
			if self.southwestv(col,row) == 0:
				self.groundimg.blit(images["southwest"],(x,y))
			if self.eastv(col,row) == 0:
				self.groundimg.blit(images["east"],(x,y))
			if self.westv(col,row) == 0:
				self.groundimg.blit(images["west"],(x,y))
			if self.northv(col,row) == 0:
				self.groundimg.blit(images["north"],(x,y))
			if self.southv(col,row) == 0:
				self.groundimg.blit(images["south"],(x,y))
		elif k == 0:
			self.groundimg.blit(images["water"],(x,y))
			pygame.draw.rect(self.minimap,BLUE,pygame.Rect(col,row,1,1),1)
	
	def setNeighborBitmap(self,col,row):
		for col,row in self.neighbors(col,row):
			self.setBitmap(col,row)
	
	def inarea(self,x,y):
		realx,realy = x+self.x,y+self.y
		return realx > -gridwidth and realx < battlewidth\
			and realy > -gridheight and realy < battleheight
	
	def scroll(self):
		self.movex(scrollspeed * max(self.scrollv[0],self.scrollv[4]))
		self.movex(-scrollspeed * max(self.scrollv[1],self.scrollv[5]))
		self.movey(scrollspeed * max(self.scrollv[2],self.scrollv[6]))
		self.movey(-scrollspeed * max(self.scrollv[3],self.scrollv[7]))
		self.fitOffset()
	
	def fitOffset(self):
		if self.x > 0: self.setx(0)
		if self.y > 0: self.sety(0)
		if self.x < battlewidth-self.groundwidth+50: self.setx(battlewidth-self.groundwidth+50)
		if self.y < battleheight-self.groundheight+50: self.sety(battleheight-self.groundheight+50)
	
	def updateScrollV(self,x,y,button):
		if x <= mousescrollwidth:
			self.scrollv[4] = 1
		else:
			self.scrollv[4] = 0
		if button: self.scrollv[4] *= 2
		if x >= winwidth - mousescrollwidth:
			self.scrollv[5] = 1
		else:
			self.scrollv[5] = 0
		if button: self.scrollv[5] *= 2
		if y <= mousescrollwidth:
			self.scrollv[6] = 1
		else:
			self.scrollv[6] = 0
		if button: self.scrollv[6] *= 2
		if y >= winheight - mousescrollwidth:
			self.scrollv[7] = 1
		else:
			self.scrollv[7] = 0
		if button: self.scrollv[7] *= 2
		
	def update(self):
		self.scroll()
	
	def getGridPos(self,x,y):
		return getGridPos(x-self.x,y-self.y)
	
	def validPos(self,col,row):
		return row >= 0 and row < self.height and col >= 0 and col < self.width
	
	def island(self,x,y):
		col,row = getGridPos(x,y)
		return self.islandGrid(col,row)
	
	def islandGrid(self,col,row):
		if not self.validPos(col,row): return False
		return self.map[col][row] == 1
	
	def iswater(self,x,y):
		col,row = getGridPos(x,y)
		return self.iswaterGrid(col,row)
	
	def iswaterGrid(self,col,row):
		if not self.validPos(col,row): return False
		return self.map[col][row] == 0
	
	def transformMini(self,x,y):
		x = x * self.minimapw / self.groundwidth + minimapx
		y = y * self.minimaph / self.groundheight + minimapy
		return x,y
	
	def transformFromMini(self,x,y):
		x = (x-minimapx)*self.groundwidth/self.minimapw
		y = (y-minimapy)*self.groundheight/self.minimaph
		return x,y
	
	def draw(self,screen):
		super(Map,self).draw(screen)
		self.groundbox.draw(screen)
		
	def nearNeighbors(self,col,row):
		return [self.northeast(col,row),self.northwest(col,row),\
			self.southeast(col,row),self.southwest(col,row)]
	def farNeighbors(self,col,row):
		return [self.east(col,row),self.west(col,row),self.south(col,row),self.north(col,row)]
	def neighbors(self,col,row):
		return self.nearNeighbors(col,row) + self.farNeighbors(col,row)
	def northeast(self,col,row):
		return col+1,row-(col+1)%2
	def southwest(self,col,row):
		return col-1,row+col%2
	def southeast(self,col,row):
		return col+1,row+col%2
	def northwest(self,col,row):
		return col-1,row-(col+1)%2
	def east(self,col,row):
		return col+2,row
	def west(self,col,row):
		return col-2,row
	def north(self,col,row):
		return col,row-1
	def south(self,col,row):
		return col,row+1
	def northeastv(self,col,row):
		ncol,nrow = self.northeast(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def southwestv(self,col,row):
		ncol,nrow = self.southwest(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def southeastv(self,col,row):
		ncol,nrow = self.southeast(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def northwestv(self,col,row):
		ncol,nrow = self.northwest(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def eastv(self,col,row):
		ncol,nrow = self.east(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def westv(self,col,row):
		ncol,nrow = self.west(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def northv(self,col,row):
		ncol,nrow = self.north(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
	def southv(self,col,row):
		ncol,nrow = self.south(col,row)
		if self.validPos(ncol,nrow):
			return self.map[ncol][nrow]
		return self.map[col][row]
