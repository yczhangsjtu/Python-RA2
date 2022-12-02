import pygame
from random import choice

from map import getGridCenter
from animation import Animation, AnimationSet
from consts import *
from data import images

directions = ["nw", "w", "sw", "s", "se", "e", "ne", "n"]


def initBloodBars():
  global bloodbarimg, infantryHealthBlood, infantryHurtBlood, \
      infantryDangerBlood
  bloodbarimg = images["bloodbar"]
  infantryHealthBlood = bloodbarimg.subsurface(0, 0, 25, 5)
  infantryHurtBlood = bloodbarimg.subsurface(0, 4, 25, 5)
  infantryDangerBlood = bloodbarimg.subsurface(0, 8, 25, 5)


def dist(x1, y1, x2, y2):
  return abs(x1-x2)+abs(y1-y2)


class Unit(object):
  def __init__(self, player, animationset, animation=None):
    self.player = player
    self.animationset = animationset
    self.name = ""
    self.animation = f"%s_{player}" % (animationset.originalAnimation
                                       if animation is None else animation)
    self.index = 0
    self.target = None
    self.rect = pygame.Rect(0, 0, 1, 1)
    self.air = False
    self.HP = 0
    self.selectable = True
    self.regionselectable = True
    self.nextAnimation = ""
    self.x = 0
    self.y = 0
    self.end = False

  def drawArea(self, screen):
    pointlist = [(self.x+self.size*8, self.y)]
    pointlist.append((self.x, self.y-self.size*4))
    pointlist.append((self.x-self.size*8, self.y))
    pointlist.append((self.x, self.y+self.size*4))
    pygame.draw.polygon(screen, WHITE, pointlist)

  def draw(self, screen):
    # self.drawArea(screen)
    self.animationset.setState(self.animation, self.index)
    self.animationset.setpos(self.x, self.y)
    self.animationset.draw(screen)

  def inarea(self, characterset):
    return characterset.inarea(self)

  def drawGroup(self, screen, group):
    rect = self.get_rect()
    x, y = rect.topright
    rect = pygame.Rect(x, y, groupw, grouph)
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, colorofplayer[self.player], rect, 2)
    textimg = pygame.font.Font(None, 15).render(
        str(group), False, colorofplayer[self.player])
    textrect = textimg.get_rect()
    textrect.center = rect.center
    screen.blit(textimg, textrect)

  def drawBloodBar(self, screen):
    pass

  def get_rect(self):
    self.rect.centerx = self.x
    self.rect.bottom = self.y
    return self.rect

  def move(self, map, characters):
    offsetx, offsety = self.offsetx, self.offsety
    if self.animation == "rune_%d" % (self.player):
      offsetx += self.speed
    if self.animation == "runw_%d" % (self.player):
      offsetx -= self.speed
    if self.animation == "runn_%d" % (self.player):
      offsety -= self.speed
    if self.animation == "runs_%d" % (self.player):
      offsety += self.speed
    if self.animation == "runne_%d" % (self.player):
      offsetx += self.speed*2/3
      offsety -= self.speed/3
    if self.animation == "runnw_%d" % (self.player):
      offsetx -= self.speed*2/3
      offsety -= self.speed/3
    if self.animation == "runse_%d" % (self.player):
      offsetx += self.speed*2/3
      offsety += self.speed/3
    if self.animation == "runsw_%d" % (self.player):
      offsetx -= self.speed*2/3
      offsety += self.speed/3
    if self.offsetx != offsetx or self.offsety != offsety:
      success = ((map.island(offsetx, offsety) and canland[self.name]) or
                 (map.iswater(offsetx, offsety) and canwater[self.name])) and\
          characters.unitSet.move(self, offsetx, offsety)
      if not success:
        self.tempStop()
        return False
    return True

  def step(self, map, characters):

    if self.end and self.nextAnimation != "":
      self.animation, self.index = self.nextAnimation, 0
      self.nextAnimation = ""
      self.animationset.setState(self.animation, self.index)
      self.end = self.animationset.end
    else:
      self.animation, self.index = self.animationset.step(
          self.animation, self.index)
      self.end = self.animationset.end
    self.move(map, characters)

  def startAnimation(self, animation):
    self.nextAnimation = animation

  def moveTo(self, x, y, characters):
    if dist(self.offsetx, self.offsety, x, y) < 2*self.speed:
      characters.unitSet.move(self, x, y)
      self.stop()
    else:
      corner = None
      directx = None
      directy = None
      if x > self.offsetx + self.speed:
        directx = self.moveRight
      elif x < self.offsetx - self.speed:
        directx = self.moveLeft
      if y > self.offsety + self.speed:
        directy = self.moveDown
        if directx == self.moveLeft:
          corner = self.moveDownLeft
        elif directx == self.moveRight:
          corner = self.moveDownRight
      elif y < self.offsety - self.speed:
        directy = self.moveUp
        if directx == self.moveLeft:
          corner = self.moveUpLeft
        elif directx == self.moveRight:
          corner = self.moveUpRight
      if corner is None and directx is None and directy is None:
        characters.unitSet.move(self, x, y)
        self.stop()
      elif directx is None:
        directy()
      elif directy is None:
        directx()
      else:
        ratioxy = abs(self.offsetx-x)/abs(self.offsety-y)
        ratioyx = abs(self.offsety-y)/abs(self.offsetx-x)
        if ratioxy > 2:
          directx()
        elif ratioyx > 2:
          directy()
        else:
          corner()

  def moveRight(self):
    self.startAnimation("rune_%d" % (self.player))

  def moveLeft(self):
    self.startAnimation("runw_%d" % (self.player))

  def moveDown(self):
    self.startAnimation("runs_%d" % (self.player))

  def moveUp(self):
    self.startAnimation("runn_%d" % (self.player))

  def moveDownRight(self):
    self.startAnimation("runse_%d" % (self.player))

  def moveDownLeft(self):
    self.startAnimation("runsw_%d" % (self.player))

  def moveUpRight(self):
    self.startAnimation("runne_%d" % (self.player))

  def moveUpLeft(self):
    self.startAnimation("runnw_%d" % (self.player))

  def getStopAnimation(self):
    for direction in directions:
      if self.animation == "run%s_%d" % (direction, self.player) or\
              self.animation == "crawl%s_%d" % (direction, self.player):
        return "stand%s_%d" % (direction, self.player)
    return "stand%s_%d" % ("e", self.player)

  def tempStop(self):
    self.animation, self.index = self.getStopAnimation(), 0
    self.animationset.setState(self.animation, self.index)
    self.end = self.animationset.end

  def stop(self):
    self.tempStop()
    if self.target is not None and isinstance(self.target, tuple):
      self.target = None
    return

  def onMouseDown(self, x, y, button):
    pass

  def onMouseUp(self, x, y, button):
    pass

  def onMouseMove(self, x, y, button1=None, button2=None, button3=None):
    pass

  def onDoubleClick(self):
    pass

  def width(self):
    return self.get_rect().width

  def height(self):
    return self.get_rect().height


class MobileUnit(Unit):
  def __init__(self, player, animationset, animation=None):
    super(MobileUnit, self).__init__(player, animationset, animation)

  def step(self, map, characters):
    super(MobileUnit, self).step(map, characters)
    if self.target is not None:
      if isinstance(self.target, tuple):
        x, y = self.target
        self.moveTo(x, y, characters)
      else:
        x, y = self.target.offsetx, self.target.offsety
        if dist(self.offsetx, self.offsety, x, y) > self.range:
          self.moveTo(x, y, characters)

  def drawMobBloodBar(self, screen, mng, offsetx, offsety):
    if self.HP >= self.fullHP/2:
      ngrid = self.HP * mng / self.fullHP
      screen.blit(infantryHealthBlood.subsurface(
          0, 0, ngrid*3+1, 5), (self.x-offsetx, self.y-offsety))
    elif self.HP >= self.fullHP/4:
      ngrid = self.HP * mng / self.fullHP
      screen.blit(infantryHurtBlood.subsurface(
          0, 0, ngrid*3+1, 5), (self.x-offsetx, self.y-offsety))
    else:
      ngrid = self.HP * mng / self.fullHP
      screen.blit(infantryDangerBlood.subsurface(
          0, 0, ngrid*3+1, 5), (self.x-offsetx, self.y-offsety))
