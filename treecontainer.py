def collide(x1,y1,s1,x2,y2,s2):
	return abs(x1-x2)+abs(y1-y2)*2 < 8*(s1+s2)

class TreeContainer(object):
	def __init__(self,x,y,width,height):
		self.lefttop = None
		self.righttop = None
		self.leftbottom = None
		self.rightbottom = None
		self.children = [None]*4
		self.data = None
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	def isLeaf(self):
		return True
		
