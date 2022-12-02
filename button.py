import pygame

from data import images
from imagesprite import ImageSprite
from spritecontainer import ExtendSprite
from consts import *


class Button(ExtendSprite):
  def __init__(self, normal, over, pressed):
    super(Button, self).__init__()
    self.normal = normal
    self.over = over
    self.pressed = pressed
    self.setimage(self.normal)
    self.mouseListener = None

  def setMouseListener(self, callback):
    self.mouseListener = callback

  def recover(self):
    self.setimage(self.normal)

  def shade(self):
    self.setimage(self.over)

  def under(self):
    self.setimage(self.pressed)

  def onMouseMove(self, x, y):
    if not self.contains(x, y):
      self.recover()
    else:
      self.shade()

  def onMouseDown(self, x, y, button):
    if button != 1:
      return
    if not self.contains(x, y):
      return
    self.under()

  def onMouseUp(self, x, y, button):
    if button != 1:
      return
    if not self.image == self.pressed:
      return
    self.recover()
    if self.contains(x, y):
      if self.mouseListener is not None:
        self.mouseListener()


class PressedButton(Button):
  def __init__(self, normal, pressed):
    super(PressedButton, self).__init__(normal, normal, pressed)
    self.ispressed = False

  def onMouseMove(self, x, y):
    pass

  def onMouseUp(self, x, y, button):
    pass

  def onMouseDown(self, x, y, button):
    if button != 1:
      return
    if self.contains(x, y):
      if self.ispressed:
        self.recover()
        self.ispressed = False
      else:
        self.under()
        self.ispressed = True
      if self.mouseListener is not None:
        if self.mouseListener is not None:
          self.mouseListener()


class TextButton(Button):
  def __init__(self, text, font, normal, over, pressed):
    textimg = font.render(text, False, WHITE)
    textrect = textimg.get_rect()

    normalimg = normal.copy()
    textrect.center = normalimg.get_rect().center
    normalimg.blit(textimg, textrect)

    overimg = over.copy()
    textrect.center = overimg.get_rect().center
    overimg.blit(textimg, textrect)

    pressedimg = pressed.copy()
    textrect.center = pressedimg.get_rect().center
    pressedimg.blit(textimg, textrect)

    super(TextButton, self).__init__(normalimg, overimg, pressedimg)


class RA2Button(TextButton):
  def __init__(self, text):
    font = pygame.font.Font(None, 26)
    img = images["menubttn"]
    btnwidth = img.get_rect().width/3
    btnheight = img.get_rect().height
    normalimg = images["menubttn"].subsurface(0, 0, btnwidth, btnheight)
    overimg = images["menubttn"].subsurface(btnwidth, 0, btnwidth, btnheight)
    pressedimg = images["menubttn"].subsurface(
        btnwidth*2, 0, btnwidth, btnheight)
    super(RA2Button, self).__init__(text, font, normalimg, overimg, pressedimg)


class CreateButton(Button):
  def __init__(self, name):
    normal = images["create%s" % name]
    if "disable%s" % name not in images:
      images["disable%s" % name] = images["create%s" % name].copy()
      images["disable%s" % name].blit(images["black"], (0, 0))
    over = normal
    pressed = normal
    super(CreateButton, self).__init__(normal, over, pressed)
    self.disableimg = images["disable%s" % name]
    self.disabled = False
    self.name = name
    self.rightMouseListener = None

  def disable(self):
    self.disabled = True
    self.setimage(self.disableimg)

  def recover(self):
    self.disabled = False
    self.setimage(self.normal)

  def setRightMouseListener(self, callback):
    self.rightMouseListener = callback

  def onMouseDown(self, x, y, button):
    if button == 1:
      if self.contains(x, y):
        if self.mouseListener is not None:
          self.mouseListener(self.name)
    elif button == 3:
      if self.contains(x, y):
        if self.rightMouseListener is not None:
          self.rightMouseLisener(self.name)

  def onMouseUp(self, x, y, button):
    pass

  def onMouseMove(self, x, y, button1=None, button2=None, button3=None):
    pass


class GameCtrlButton(Button):
  def __init__(self, index):
    img = images["button%d%d" % (index/10, index % 10)]
    normal = img.subsurface(0, 0, img.get_width()/2, img.get_height())
    over = img.subsurface(img.get_width()/2, 0,
                          img.get_width()/2, img.get_height())
    pressed = over
    super(GameCtrlButton, self).__init__(normal, over, pressed)


class GamePanelPressedButton(PressedButton):
  def __init__(self, name):
    img = images[name]
    normal = img.subsurface(0, 0, img.get_width()/2, img.get_height())
    pressed = img.subsurface(
        img.get_width()/2, 0, img.get_width()/2, img.get_height())
    super(GamePanelPressedButton, self).__init__(normal, pressed)


class GamePanelButton(Button):
  def __init__(self, name):
    img = images[name]
    normal = img.subsurface(0, 0, img.get_width()/2, img.get_height())
    over = normal
    pressed = img.subsurface(
        img.get_width()/2, 0, img.get_width()/2, img.get_height())
    super(GamePanelButton, self).__init__(normal, over, pressed)


class TabButton(Button):
  def __init__(self, index, tab, children):
    img = images["tabbtn%d" % index]
    w = img.get_width()/5
    h = img.get_height()
    normal = img.subsurface(0, 0, w, h)
    over = normal
    pressed = img.subsurface(w, 0, w, h)
    super(TabButton, self).__init__(normal, over, pressed)
    self.tab = tab
    self.children = children

  def onMouseDown(self, x, y, button):
    if button != 1:
      return
    if not self.contains(x, y):
      return
    for tabb in self.tab:
      tabb.recover()
    self.under()

  def onMouseUp(self, x, y, button):
    pass

  def under(self):
    self.setimage(self.pressed)
    self.children.visible = True

  def recover(self):
    self.setimage(self.normal)
    self.children.visible = False

  def onMouseMove(self, x, y):
    pass


class ButtonSet(set):
  def __init__(self):
    super(ButtonSet, self).__init__()
    self.visible = False
    self.group = pygame.sprite.Group()
    self.overgroup = None
    self.createProgress = None
    self.scroll = 0
