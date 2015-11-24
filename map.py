from pylash.display import Sprite, Bitmap, BitmapData
from consts import gridwidth, gridheight, battlewidth, battleheight, scrollspeed

groundData = []
greenBitmap = None
redBitmap = None

def initMap(dataList):
	global groundData, greenBitmap, redBitmap
	for k in range(0,10):
		offsetx = gridwidth*(k%5)
		offsety = gridheight*(int(k/5))
		groundData.append(BitmapData(dataList["ground"],offsetx,offsety,gridwidth,gridheight))
	greenBitmap = BitmapData(dataList["green"])
	redBitmap = BitmapData(dataList["red"])

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
		self.scrollv = [0,0,0,0,0,0,0,0]
		self.groundwidth = self.width * gridwidth/2
		self.groundheight = self.height * gridheight
	
	def clear(self):
		self.map = None
		self.pieces = None
		self.mapLayer.removeAllChildren()
		
	def initPointer(self):
		self.greenPointer = Sprite()
		self.greenPointer.addChild(Bitmap(greenBitmap))
		self.redPointer = Sprite()
		self.redPointer.addChild(Bitmap(redBitmap))
		
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
	
	def load(self):
		for i in range(self.width):
			for j in range(self.height):
				self.setBitmap(i,j)
				self.pieces[i][j].x = gridwidth/2 * (i-1)
				self.pieces[i][j].y = gridheight*j - gridheight/2*((i+1)%2)
		self.update()
	
	def paint(self,x,y,paint):
		if x >= 0 and x <= battlewidth and y >= 0 and y <= battleheight:
			col,row = self.getGridPos(x,y)
			self.map[col][row] = paint
			self.setBitmap(col,row)
			self.setNeighborBitmap(col,row)
	
	def setBitmap(self,col,row):
		if not self.validPos(col,row): return
		self.pieces[col][row].removeAllChildren()
		k = self.map[col][row]
		if k == 1:
			self.pieces[col][row].addChild(Bitmap(groundData[0]))
			if self.northeastv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[3]))
			if self.northwestv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[1]))
			if self.southeastv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[4]))
			if self.southwestv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[2]))
			if self.eastv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[9]))
			if self.westv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[6]))
			if self.northv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[8]))
			if self.southv(col,row) == 0:
				self.pieces[col][row].addChild(Bitmap(groundData[7]))
		elif k == 0:
			self.pieces[col][row].addChild(Bitmap(groundData[5]))
	
	def setNeighborBitmap(self,col,row):
		for col,row in self.neighbors(col,row):
			self.setBitmap(col,row)
	
	def inarea(self,x,y):
		realx = x + self.mapview.x
		realy = y + self.mapview.y
		return realx > -gridwidth and realx < battlewidth\
			and realy > -gridheight and realy < battleheight
	
	def scroll(self):
		if self.scrollv[0]==1 or self.scrollv[4] == 1:
			self.mapview.x += scrollspeed
		if self.scrollv[1]==1 or self.scrollv[5] == 1:
			self.mapview.x -= scrollspeed
		if self.scrollv[2]==1 or self.scrollv[6] == 1:
			self.mapview.y += scrollspeed
		if self.scrollv[3]==1 or self.scrollv[7] == 1:
			self.mapview.y -= scrollspeed
		if self.mapview.x > 0: self.mapview.x = 0
		if self.mapview.y > 0: self.mapview.y = 0
		if self.mapview.x < battlewidth-self.groundwidth: self.mapview.x = battlewidth-self.groundwidth
		if self.mapview.y < battleheight-self.groundheight: self.mapview.y = battleheight-self.groundheight
		self.update()
	
	def update(self):
		for i in range(self.width):
			for j in range(self.height):
				piece = self.pieces[i][j]
				if piece.parent != None:
					piece.remove()
				if self.inarea(piece.x,piece.y):
					self.mapview.addChild(piece)
	
	def getAbsPos(col,row):
		x = gridwidth/2 * (col-1)
		y = gridheight*row - gridheight/2*((col+1)%2)
		return x+gridwidth/2,y+gridheight/2
	
	def getGridPos(self,x,y):
		X,Y = x-self.mapview.x,y-self.mapview.y
		X,Y = X/gridwidth*2,Y/gridheight*2
		X,Y = int((X+Y+1)/2), int((-X+Y+1)/2+1000)-1000
		row,col = int((X+Y)/2),X-Y
		return col,row
	
	def getGrid(self,x,y):
		col,row = self.getGridPos(x,y)
		if self.validPos(col,row):
			return self.pieces[col][row]
		return None
	
	def validPos(self,col,row):
		return row >= 0 and row < self.height and col >= 0 and col < self.width
	
	def updateRedPointer(self,pos):
		col,row = pos
		if self.redPointer.parent != None:
			self.redPointer.remove()
		if not self.validPos(col,row):
			return
		self.pieces[col][row].addChild(self.redPointer)
		
	def updateGreenPointer(self,pos):
		col,row = pos
		if self.greenPointer.parent != None:
			self.greenPointer.remove()
		if not self.validPos(col,row):
			return
		self.pieces[col][row].addChild(self.greenPointer)
	
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