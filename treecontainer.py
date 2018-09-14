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
		self.topcontainer = container
		while not container.isLeaf():
			container = container.lt
		self.container = container
		if self.container.data == None:
			self.findNextData()
		if not self.container == None:
			if self.container.data == None:
				raise Exception('Data is none after findNextData!')
	
	def findNextData(self):
		if self.container == None: return
		while True:
			if self.container == self.topcontainer:
				self.container = None
				return
			father = self.container.father
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
	
	def __next__(self):
		if self.container == None:
			raise StopIteration
		data = self.container.data
		if data == None:
			raise Exception('Data is None!')
		self.findNextData()
		if not self.container == None:
			if self.container.data == None:
				raise Exception('Data is none after findNextData!')
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
	
	def __str__(self):
		return self.toString(0)
	
	def toString(self,indent):
		res = "%s|----[%s,%s,%s,%s]"%(" "*indent,self.x,self.y,self.x+self.width,self.y+self.height)
		if self.data != None:
			res += "--------(%d,%d),%d"%(self.data.offsetx,self.data.offsety,self.data.size)
		if not self.leaf:
			for child in self.children:
				res += "\n%s"%(child.toString(indent+1))
		else:
			res += "------Leaf"
			
		return res
	
	def getTopContainer(self):
		if self.father == None:
			return self
		return self.father.getTopContainer()
	
	def isLeaf(self):
		return self.leaf
	
	def contains(self,x,y):
		return x >= self.x and x < self.x+self.width and\
			   y >= self.y and y < self.y+self.height
	
	def split(self):
		if self.width < 2 or self.height < 2:
			raise Exception('Two small to split!')
			exit(1)
		if not self.leaf: return
		if self.data != None:
			if not self.contains(self.data.offsetx,self.data.offsety):
				print(self)
				print(self.data)
				print(self.data.offsetx,self.data.offsety,self.data.size)
				raise Exception('Does not contain self.data.')
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
			# print("Going through all %d children."%len(self.children))
			for child in self.children:
				# print("For child: ",child)
				if child.contains(self.data.offsetx,self.data.offsety):
					child.data = self.data
					self.data.container = child
					self.data = None
					# print(child)
					# print("contains self.data.")
					return
				# else:
					# print(child)
					# print("does not contain self.data.")
					# print(self.data.offsetx,self.data.offsety)
			print(self)
			print(self.data.offsetx,self.data.offsety)
			raise Exception('No child contains self.data.')
		
	def add(self,data):
		if data == None:
			raise Exception('Added data is none!')
		if not self.contains(data.offsetx,data.offsety):
			print(data.offsetx,data.offsety)
			print(self.x,self.y,self.width,self.height)
			raise Exception('Data offset does not contained in the box.')
			exit(1)
		if self.leaf:
			if self.data == None:
				# print("Adding",data,data.offsetx,data.offsety,data.size,"to")
				# print(self)
				self.data = data
				data.container = self
				return True
			if self.data == data:
				print(self)
				print(data)
				print(data.offsetx,data.offsety,data.size)
				print(self.data)
				print(self.data.offsetx,self.data.offsety,self.data.size)
				raise Exception('Adding already existed member.')
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
		if not c.leaf:
			raise Exception('Container is not leaf.')
		# print(c.data,"removed from")
		# print(c)
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
					hasdata = child
				else:
					return
		if hasdata != None:
			# print("Collecting data",hasdata.data,"from")
			# print(hasdata)
			self.data = hasdata.data
			self.data.container = self
			hasdata.data = None
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
	
	def availableSize(self,size,x,y):
		if self.leaf:
			if self.data == None:
				return True
			return not collideDataPos(self.data,x,y,size)
		result = True
		for child in self.children:
			if child.collide(size+maxsize,x,y):
				result = result and child.availableSize(size,x,y)
			if not result: break
		return result

	def available(self,data,x,y):
		if self.leaf:
			if self.data == data or self.data == None:
				return True
			return not collideDataPos(self.data,x,y,data.size)
		result = True
		for child in self.children:
			if child.collide(data.size+maxsize,x,y):
				result = result and child.available(data,x,y)
			if not result: break
		return result
	
	def move(self,data,x,y):
		if y < self.y: y = self.y
		if y >= self.y + self.height: y = self.y + self.height
		if x < self.x: x = self.x
		if x >= self.x + self.width: x = self.x + self.width
		if data.size > maxsize:
			raise Exception('Too big')
		if self.available(data,x,y):
			self.remove(data)
			data.offsetx = x
			data.offsety = y
			if not self.add(data):
				raise Exception('Failed to add after removing.')
				exit(1)
			else:
				return True
		# else:
		# 	print(x,y,data.size,"is not available.")
		return False
