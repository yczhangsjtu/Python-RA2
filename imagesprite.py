import pygame
from spritecontainer import ExtendSprite


class ImageSprite(ExtendSprite):
  def __init__(self, image, splitx=1, splity=1, indexx=0, indexy=0):
    super(ImageSprite, self).__init__()

    rect = image.get_rect()
    w, h = rect.width/splitx, rect.height/splity
    subrect = pygame.Rect(w*indexx, h*indexy, w, h)
    self.setimage(image.subsurface(subrect))
