from pylash.display import Sprite, Bitmap, BitmapData
from consts import gridwidth, gridheight, battlewidth, battleheight, scrollspeed

class Map():
	def __init__(self, row, col, mapLayer):
		self.map = [[1]*row for i in range(col)]
		self.pieces = [[Sprite() for i in range(row)] for j in range(col)]
		self.width = col
		self.height = row
		self.mapLayer = mapLayer
		self.mapview = Sprite()
		self.mapLayer.addChild(self.mapview)
		self.mapview.x, self.mapview.y = (0,0)
		self.scrollv = [0,0]
	
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
	
	def load(self, dataList):
		for i in range(self.width):
			for j in range(self.height):
				k = self.map[i][j]
				offsetx = gridwidth*((k-1)%4)
				offsety = gridheight*(int((k-1)/4))
				self.pieces[i][j].addChild(Bitmap(\
					BitmapData(dataList["ground"],offsetx,offsety,gridwidth,gridheight)))
				self.pieces[i][j].x = gridwidth/2 * (i-1)
				self.pieces[i][j].y = gridheight*j - gridheight/2*((i+1)%2)
		self.update()
	
	def inarea(self,x,y):
		realx = x + self.mapview.x
		realy = y + self.mapview.y
		return realx > -gridwidth and realx < battlewidth\
			and realy > -gridheight and realy < battleheight
	
	def scroll(self):
		self.mapview.x += self.scrollv[0] * scrollspeed
		self.mapview.y += self.scrollv[1] * scrollspeed
		if self.mapview.x > 0: self.mapview.x = 0
		if self.mapview.y > 0: self.mapview.y = 0
		if self.mapview.x < -battlewidth: self.mapview.x = -battlewidth
		if self.mapview.y < -battleheight: self.mapview.y = -battleheight
		self.update()
	
	def update(self):
		for i in range(self.width):
			for j in range(self.height):
				piece = self.pieces[i][j]
				if piece.parent != None:
					piece.remove()
				if self.inarea(piece.x,piece.y):
					self.mapview.addChild(piece)
