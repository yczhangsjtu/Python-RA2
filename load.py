import threading, time
import pygame
import shpfile

from data import images
from map import initMap
from consts import *
from building import initBuildingAnimations
from infantry import initInfantryAnimations
from vehicle import initVehicleAnimations

def loadImages(progress):
	loader = Loader()
	N = len(loadList)
	n = 0
	for imgname in loadList:
		loader.loadimg(imgname)
		n += 1
		progress[0] = float(n)/N
	initMap()
	initBuildingAnimations()
	initInfantryAnimations()
	initVehicleAnimations()
	progress[0] = 1

class Loader():
	def __init__(self):
		pass
	
	def load(self,img,screen,function,progressbar=None):
		progress = [0]
		
		def start():
			function(progress)
		
		loadThread = threading.Thread(target = start)
		loadThread.start()
		while progress[0] < 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						exit(0)
			screen.blit(img,(0,0))
			if progressbar != None:
				rect = progressbar[0].get_rect().copy()
				rect.width = int(rect.width * progress[0])
				screen.blit(progressbar[0].subsurface(rect),progressbar[1])
			pygame.display.flip()
			pygame.time.Clock().tick(60)
		
	def loadimg(self,name):
		path = loadList[name]
		images[name] = pygame.image.load(path)

