from consts import *
from map import getAbsPos

def collidePos(x1,y1,s1,x2,y2,s2):
	return abs(x1-x2)+abs(y1-y2)*occupyx/occupyy < occupyx*(s1+s2)

def collideDataPos(data,x2,y2,s2):
	return collidePos(data.offsetx,data.offsety,data.size,x2,y2,s2)

def collide(data1,data2):
	return collideDataPos(data1,data2.offsetx,data2.offsety,data2.size)

class TreeContainerIter(object):
	def __init__(self,container):
		while not container.isLeaf():
			container = container.lt
		self.container = container
		if self.container.data == None:
			self.findNextData()
	
	def findNextData(self):
		if self.container == None: return
		while True:
			father = self.container.father
			if father == None:
				self.container = None
				return
			current = -1
			for i in range(4):
				if father.children[i] == self.container:
					current = i
					break
			if current == 3:
				self.container = father
			else:
				self.container = father.children[current+1]
				while not self.container.isLeaf():
					self.container = self.container.lt
				if self.container.data != None:
					return
	
	def next(self):
		if self.container == None:
			raise StopIteration
		data = self.container.data
		self.findNextData()
		return data

class TreeContainer(object):
	def __init__(self,x,y,width,height,father=None):
		self.lt = None
		self.rt = None
		self.lb = None
		self.rb = None
		self.children = [None]*4
		self.data = None
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.leaf = True
		self.father = father
	
	def __iter__(self):
		return TreeContainerIter(self)
	
	def isLeaf(self):
		return self.leaf
	
	def contains(self,x,y):
		return x >= self.x and x < self.x+self.width and\
			   y >= self.y and y < self.y+self.height
	
	def split(self):
		if not self.leaf: return
		lw = self.width/2
		rw = self.width - lw
		uh = self.height/2
		dh = self.height - uh
		self.lt = TreeContainer(self.x,   self.y,   lw,uh,self)
		self.rt = TreeContainer(self.x+lw,self.y,   rw,uh,self)
		self.lb = TreeContainer(self.x,   self.y+uh,lw,dh,self)
		self.rb = TreeContainer(self.x+lw,self.y+uh,rw,dh,self)
		self.children = [self.lt,self.rt,self.lb,self.rb]
		self.leaf = False
		if self.data != None:
			for child in self.children:
				if child.contains(self.data.offsetx,self.data.offsety):
					child.data = self.data
					self.data.container = child
					self.data = None
					break
		
	def add(self,data):
		if not self.contains(data.offsetx,data.offsety):
			print data.offsetx,data.offsety
			print self.x,self.y,self.width,self.height
			raise Exception('Data offset does not contained in the box.')
			exit(1)
		if self.leaf:
			if self.data == None:
				self.data = data
				data.container = self
				return True
			if collide(self.data,data):
				return False
			self.split()
		for child in self.children:
			if child.contains(data.offsetx,data.offsety):
				if child.add(data): return True
		return False
	
	def addPos(self,data,x,y):
		data.offsetx,data.offsety = x,y
		return self.add(data)
	
	def addGrid(self,data,col,row):
		data.offsetx,data.offsety = getAbsPos(col,row)
		return self.add(data)
	
	def remove(self,data):
		c = data.container
		if c.data == None:
			raise Exception('Removing none object.')
			exit(1)
		if not c.leaf:
			raise Exception('Container is not leaf.')
		c.data = None
		if c.father != None:
			c.father.cleanup()
	
	def cleanup(self):
		if self.leaf: return
		hasdata = None
		for child in self.children:
			if not child.leaf:
				return
			if child.data != None:
				if hasdata == None:
					return
				hasdata = child
		if hasdata != None:
			self.data = hasdata.data
		self.leaf = True
		self.lt = None
		self.rt = None
		self.lb = None
		self.rb = None
		self.children = [None]*4
		if self.father != None:
			self.father.cleanup()
	
	def collide(self,size,x,y):
		l = occupyx * size
		w = occupyy * size
		c1 = x > self.x-l and x < self.x+self.width+l and\
			 y > self.y-w and y < self.y+self.height+w
		X = 2*x - (2*self.x + self.width)
		Y = 2*y - (2*self.y + self.height)
		c2 = abs(w*X)+abs(l*Y) < abs(l*self.height+w*self.width+2*l*w)
		return c1 and c2
	
	def available(self,data,x,y):
		if self.leaf:
			if self.data == data or self.data == None:
				return True
			return not collideDataPos(self.data,x,y,data.size)
		result = True
		for child in self.children:
			if child.collide(data.size,x,y):
				result = result and child.available(data,x,y)
			if not result: break
		return result
	
	def move(self,data,x,y):
		if self.available(data,x,y):
			self.remove(data)
			data.offsetx = x
			data.offsety = y
			self.add(data)
			return True
		return False
