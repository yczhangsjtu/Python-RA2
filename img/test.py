import shpfile
import pygame
import sys

data = shpfile.load(sys.argv[1],"./pal/red.pal")
w,h = data[0]
n = len(data)-1

print "%d, %dx%d"%(n,w,h)

pygame.init()
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Shp reader")

def drawOnPixelArray(array,d,w,h):
	for i in range(h):
		for j in range(w):
			offset = (i * w + j) * 4
			array[j,i] = (d[offset],d[offset+1],d[offset+2],d[offset+3])

frames = [None]*n
for i in range(n):
	frames[i] = pygame.Surface([w,h]).convert_alpha()
	drawOnPixelArray(pygame.PixelArray(frames[i]),data[i+1],w,h)

k = 0
clock = pygame.time.Clock()
while True:
	screen.fill((255,255,255))
	screen.blit(frames[k],(0,0))
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
	clock.tick(2)
	k+=1
	if k >= n: k = 0
