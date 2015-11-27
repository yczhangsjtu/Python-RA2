import pygame
from spritecontainer import ExtendSprite

class ImageSprite(ExtendSprite):
	def __init__(self,image):
		super(ImageSprite,self).__init__()
		
		self.setimage(image)