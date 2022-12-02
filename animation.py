import pygame
import traceback

from imagesprite import ImageSprite
from consts import *

directions = ["n", "nw", "w", "sw", "s", "se", "e", "ne"]


class Animation(pygame.sprite.GroupSingle):
  def __init__(self):
    super(Animation, self).__init__()
    self.spriteset = []
    self.index = -1
    self.loop = True
    self.next = None
    self.end = False

  def get_rect(self):
    if self.sprite is not None:
      return self.sprite.rect
    return None

  def addImageSprite(self, image, offsetx, offsety):
    self.addSprite(ImageSprite(image), offsetx, offsety)

  def addImageSpriteSheet(self, image, x, y, width, height, m, n,
                          offsetx, offsety, skip=0):
    count = 0
    for j in range(n):
      for i in range(m):
        if count % (skip+1) == 0:
          subimage = image.subsurface(x+i*width, y+j*height, width, height)
          self.addImageSprite(subimage, offsetx, offsety)
        count += 1

  def addBrokenSpriteSheet(self, image, x, y, i0, j0,
                           width, height, left, right, count,
                           offsetx, offsety):
    i, j = i0, j0
    for k in range(count):
      try:
        subimage = image.subsurface(x+i*width, y+j*height, width, height)
        self.addImageSprite(subimage, offsetx, offsety)
      except Exception as e:
        print(traceback.format_exc())
        print(x, y, width, height, i, j)
      i += 1
      if i >= right:
        i = left
        j += 1

  def addSprite(self, sprite, offsetx, offsety):
    sprite.offsetx = offsetx
    sprite.offsety = offsety
    self.spriteset.append(sprite)

  def setIndex(self, index):
    if len(self.spriteset) == 0:
      self.index = -1
      self.end = False
      return self.index
    if self.loop:
      self.index = index % len(self.spriteset)
    elif index < 0:
      self.index = 0
    elif index >= len(self.spriteset):
      self.index = len(self.spriteset)-1
    else:
      self.index = index
    self.end = (self.index == len(self.spriteset)-1)
    self.add(self.spriteset[self.index])
    return self.index

  def step(self):
    self.index += 1
    self.setIndex(self.index)

  def setx(self, x):
    if self.sprite is not None:
      self.sprite.rect.left = x-self.sprite.offsetx

  def sety(self, y):
    if self.sprite is not None:
      self.sprite.rect.top = y-self.sprite.offsety

  def setpos(self, x, y):
    if self.sprite is not None:
      self.sprite.rect.topleft = (x-self.sprite.offsetx, y-self.sprite.offsety)


class AnimationSet(pygame.sprite.GroupSingle):
  def __init__(self):
    super(AnimationSet, self).__init__()
    self.animationSet = {}
    self.end = False

  def get_rect(self):
    if self.sprite is not None:
      return self.sprite.rect
    return None

  def addAnimation(self, name, animation):
    self.animationSet[name] = animation
    animation.name = name

  def getAnimation(self, name):
    return self.animationSet[name]

  def setState(self, name, index):
    animation = self.animationSet[name]
    animation.setIndex(index)
    self.add(animation.sprite)
    self.end = animation.end

  def setx(self, x):
    if self.sprite is not None:
      self.sprite.rect.left = x-self.sprite.offsetx

  def sety(self, y):
    if self.sprite is not None:
      self.sprite.rect.top = y-self.sprite.offsety

  def setpos(self, x, y):
    if self.sprite is not None:
      self.sprite.rect.topleft = (x-self.sprite.offsetx, y-self.sprite.offsety)

  def step(self, name, index):
    animation = self.animationSet[name]
    animation.setIndex(index)
    self.end = animation.end
    if not animation.end or animation.loop:
      animation.step()
      self.end = animation.end
      return name, animation.index
    elif animation.next is None:
      return name, animation.index
    else:
      return animation.next.name, 0

  def addAnimationFromSpriteSheet(self, image, x, y, width, height, m, n,
                                  offsetx, offsety, playeroffset, name,
                                  loop=True, nextanim=None, prevanim=None):
    for player in range(numofplayer):
      animation = Animation()
      animation.addImageSpriteSheet(
          image, x, y, width, height, m, n, offsetx, offsety)
      self.addAnimation("%s_%d" % (name, player), animation)
      if not loop:
        animation.loop = False
      if nextanim is not None:
        animation.next = self.getAnimation("%s_%d" % (nextanim, player))
      if prevanim is not None:
        self.getAnimation("%s_%d" % (prevanim, player)).next = animation
      y += playeroffset

  def addAnimationFromSpriteSheetDir(self, image, x, y, width, height, m, n,
                                     offsetx, offsety, playeroffset, name,
                                     loop=True, nextanim=None, prevanim=None):
    for player in range(numofplayer):
      X = x
      for direction in directions:
        animation = Animation()
        animation.addImageSpriteSheet(
            image, X, y, width, height, m, n, offsetx, offsety)
        self.addAnimation("%s%s_%d" % (name, direction, player), animation)
        if not loop:
          animation.loop = False
        if nextanim is not None:
          animation.next = self.getAnimation(
              "%s%s_%d" % (nextanim, direction, player))
        if prevanim is not None:
          self.getAnimation("%s%s_%d" %
                            (prevanim, direction, player)).next = animation
        X += width * m
      y += playeroffset


class SimpleAnimation(Animation):
  def __init__(self, image, x, y, width, height, m, n, offsetx, offsety):
    super(SimpleAnimation, self).__init__()
    self.addImageSpriteSheet(image, x, y, width, height, m, n, 0, 0)
    for sprite in self.spriteset:
      sprite.setpos(offsetx, offsety)
    self.setIndex(0)
    self.started = False

  def onMouseDown(self, x, y, button):
    pass

  def onMouseMove(self, x, y, button1=None, button2=None, button3=None):
    pass

  def onMouseUp(self, x, y, button):
    pass

  def bottom(self):
    return self.sprite.rect.bottom

  def right(self):
    return self.sprite.rect.right

  def left(self):
    return self.sprite.rect.left

  def top(self):
    return self.sprite.rect.top
