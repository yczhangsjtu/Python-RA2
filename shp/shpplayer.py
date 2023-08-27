import shp
import pygame
import os

data = shp.load("Refactor/render_layer/img/shp/small/engineer.shp",
                "Refactor/render_layer/img/pal/red.pal")
w, h = data[0].w, data[0].h
n = len(data)

print("%d, %dx%d" % (n, w, h))

pygame.init()

font = pygame.font.Font(None, 24)

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Shp reader")


def drawOnPixelArray(array, d, w, h):
    for i in range(h):
        for j in range(w):
            offset = (i * w + j) * 4
            array[j, i] = (d[offset], d[offset+1], d[offset+2], d[offset+3])


frames = [None]*n
for i in range(n):
    frames[i] = pygame.Surface([w, h]).convert_alpha()
    drawOnPixelArray(pygame.PixelArray(frames[i]), data[i].data, w, h)

k = 0
clock = pygame.time.Clock()
while True:
    screen.fill((255, 255, 255))
    screen.blit(frames[k], (0, 0))
    screen.blit(font.render(str(k)+"/"+str(n), True, (0, 0, 0)), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    clock.tick(12)
    k += 1
    if k >= n:
        k = 0
