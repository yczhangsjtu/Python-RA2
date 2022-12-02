import pygame

from unit import *
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *


e3Animation = None
adogAnimation = None
directions = ["n", "nw", "w", "sw", "s", "se", "e", "ne"]
infantryRect = pygame.Rect(0, 0, 15, 25)


def initInfantryAnimations():
  global e3Animation, adogAnimation, engineerAnimation
  e3Animation = E3Animation()
  adogAnimation = AdogAnimation()
  engineerAnimation = EngineerAnimation()


class Infantry(MobileUnit):
  def __init__(self, player, animationset, animation=None):
    super(Infantry, self).__init__(player, animationset, animation)
    self.rect = infantryRect

  def drawBloodBar(self, screen):
    self.drawMobBloodBar(screen, 8, 12, 40)


class Adog(Infantry):
  def __init__(self, player, animation=None):
    animationset = adogAnimation
    super(Adog, self).__init__(player, animationset, animation)
    self.speed = 10
    self.size = sizeofunit["Adog"]
    self.range = 0
    self.fullHP = 100
    self.HP = self.fullHP
    self.name = "Adog"


classmap["Adog"] = Adog


class E3(Infantry):
  def __init__(self, player, animation=None):
    animationset = e3Animation
    super(E3, self).__init__(player, animationset, animation)
    self.speed = 4
    self.size = sizeofunit["E3"]
    self.range = 100
    self.fullHP = 100
    self.HP = self.fullHP
    self.name = "E3"


classmap["E3"] = E3


class Engineer(Infantry):
  def __init__(self, player, animation=None):
    animationset = engineerAnimation
    super(Engineer, self).__init__(player, animationset, animation)
    self.speed = 7
    self.size = sizeofunit["Engineer"]
    self.range = 0
    self.fullHP = 100
    self.HP = self.fullHP
    self.name = "Engineer"


classmap["Engineer"] = Engineer


class E3Animation(AnimationSet):
  def __init__(self):
    super(E3Animation, self).__init__()
    image = images["E3"]
    offsetx, offsety = 57, 37
    self.originalAnimation = "runsw"
    width, height = 118, 72
    playeroffset = 504

    y, m, n = 0, 1, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "stand")
    y, m, n = 216, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "run",
        False, "stand")
    y, m, n = 288, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "crawl",
        False, "stand")
    y, m, n = 360, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "attack",
        False, "stand")
    y, m, n = 432, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "crawlattack",
        False, "stand")
    x, y, m, n = 2220, 144, 15, 1
    self.addAnimationFromSpriteSheet(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "die1",
        False)
    x, y, m, n = 3330, 144, 15, 1
    self.addAnimationFromSpriteSheet(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "die2",
        False)

    x, y, m, n = 1110, 72, 15, 1
    for player in range(2):
      animation = Animation()
      animation.addImageSpriteSheet(
          image, x, y, width, height, m, n, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("cheer_%d" % (player), animation)
      y += playeroffset

    x, y, m, n = 0, 72, 15, 1
    for player in range(2):
      animation = Animation()
      animation.addImageSpriteSheet(
          image, x, y, width, height, m, n, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("squeez_%d" % (player), animation)
      y += playeroffset


class AdogAnimation(AnimationSet):
  def __init__(self):
    super(AdogAnimation, self).__init__()
    image = images["adog"]
    offsetx, offsety = 36, 38
    self.originalAnimation = "runsw"
    width, height = 74, 72
    playeroffset = 288

    y, m, n = 0, 1, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "stand")
    y, m, n = 72, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "run",
        False, "stand")
    y, m, n = 216, 6, 1
    self.addAnimationFromSpriteSheetDir(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "attack",
        False, "stand")
    x, y, m, n = 2220, 144, 15, 1
    self.addAnimationFromSpriteSheet(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "die1",
        False)
    x, y, m, n = 3330, 144, 15, 1
    self.addAnimationFromSpriteSheet(
        image, 0, y, width, height, m, n,
        offsetx, offsety, playeroffset, "die2",
        False)

    x, y, m, n = 0, 144, 15, 1
    for player in range(2):
      animation = Animation()
      animation.addImageSpriteSheet(
          image, x, y, width, height, m, n, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("tail_%d" % (player), animation)
      y += playeroffset

    x, y, m, n = 1110, 144, 15, 1
    for player in range(2):
      animation = Animation()
      animation.addImageSpriteSheet(
          image, x, y, width, height, m, n, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("squeez_%d" % (player), animation)
      y += playeroffset


class EngineerAnimation(AnimationSet):
  def __init__(self):
    super(EngineerAnimation, self).__init__()
    image = images["engineer"]
    offsetx, offsety = 37, 38
    self.originalAnimation = "runsw"
    width, height = 76, 80
    playeroffset = 880
    left, right = 0, 23
    x, y = 0, 0

    for player in range(2):
      i0, j0 = 0, 0

      count = 1
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        self.addAnimation("stand%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 6
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        animation.loop = False
        animation.next = self.getAnimation("stand%s_%d" % (direction, player))
        self.addAnimation("run%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 15
      animation = Animation()
      animation.addBrokenSpriteSheet(
          image, x, y, i0, j0,
          width, height, left, right, count, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("stool_%d" % (player), animation)
      i0 += count
      j0 += int(i0 / right)
      i0 %= right

      count = 15
      animation = Animation()
      animation.addBrokenSpriteSheet(
          image, x, y, i0, j0,
          width, height, left, right, count, offsetx, offsety)
      animation.loop = False
      animation.next = self.getAnimation("standsw_%d" % (player))
      self.addAnimation("read_%d" % (player), animation)
      i0 += count
      j0 += int(i0 / right)
      i0 %= right

      count = 6
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        animation.loop = False
        animation.next = self.getAnimation("stand%s_%d" % (direction, player))
        self.addAnimation("crawl%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 15
      animation = Animation()
      animation.addBrokenSpriteSheet(
          image, x, y, i0, j0,
          width, height, left, right, count, offsetx, offsety)
      animation.loop = False
      self.addAnimation("die1_%d" % (player), animation)
      i0 += count
      j0 += int(i0 / right)
      i0 %= right

      count = 15
      animation = Animation()
      animation.addBrokenSpriteSheet(
          image, x, y, i0, j0,
          width, height, left, right, count, offsetx, offsety)
      animation.loop = False
      self.addAnimation("die2_%d" % (player), animation)
      i0 += count
      j0 += int(i0 / right)
      i0 %= right

      count = 6
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        animation.loop = False
        animation.next = self.getAnimation("stand%s_%d" % (direction, player))
        self.addAnimation("search%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 2
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        animation.loop = False
        self.addAnimation("getdown%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 2
      for direction in directions:
        animation = Animation()
        animation.addBrokenSpriteSheet(
            image, x, y, i0, j0,
            width, height, left, right, count, offsetx, offsety)
        animation.loop = False
        animation.next = self.getAnimation("stand%s_%d" % (direction, player))
        self.addAnimation("getup%s_%d" % (direction, player), animation)
        i0 += count
        j0 += int(i0 / right)
        i0 %= right

      count = 9
      animation = Animation()
      animation.addBrokenSpriteSheet(
          image, x, y, i0, j0,
          width, height, left, right, count, offsetx, offsety)
      animation.loop = False
      self.addAnimation("cheer_%d" % (player), animation)
      i0 += count
      j0 += int(i0 / right)
      i0 %= right

      y += playeroffset
