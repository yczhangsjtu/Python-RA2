import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *

buildingRect = pygame.Rect(0,0,1,1)
aircmdAnimation = None
gcnstAnimation = None
powerAnimation = None
gpileAnimation = None
grefnAnimation = None
gyardAnimation = None
gweapAnimation = None
gpillAnimation = None

def initBuildingAnimations():
    global longBuildingHealthBlood, longBuildingHurtBlood,\
           longBuildingDangerBlood, shortBuildingHealthBlood,\
           shortBuildingHurtBlood, shortBuildingDangerBlood,\
           defenceHealthBlood, defenceHurtBlood, defenceeDangerBlood
    global aircmdAnimation, gcnstAnimation, powerAnimation, gpileAnimation,\
           grefnAnimation, gyardAnimation, gweapAnimation
    global gpillAnimation
    bloodbarimg = images["buildingbloodbar"]
    longBuildingHealthBlood  = bloodbarimg.subsurface(0,0,300,10)
    longBuildingHurtBlood    = bloodbarimg.subsurface(0,10,300,10)
    longBuildingDangerBlood  = bloodbarimg.subsurface(0,20,300,10)
    shortBuildingHealthBlood = bloodbarimg.subsurface(0,0,150,10)
    shortBuildingHurtBlood   = bloodbarimg.subsurface(0,10,150,10)
    shortBuildingDangerBlood = bloodbarimg.subsurface(0,20,150,10)
    defenceHealthBlood = bloodbarimg.subsurface(0,0,40,10)
    defenceHurtBlood   = bloodbarimg.subsurface(0,10,40,10)
    defenceDangerBlood = bloodbarimg.subsurface(0,20,40,10)
    aircmdAnimation = AirCmdAnimation()
    gcnstAnimation = GcnstAnimation()
    powerAnimation = PowerAnimation()
    grefnAnimation = GrefnAnimation()
    gpileAnimation = GpileAnimation()
    gyardAnimation = GyardAnimation()
    gweapAnimation = GweapAnimation()
    gpillAnimation = GpillAnimation()

class Building(Unit):
    def __init__(self,player,animationset,animation=None):
        super(Building,self).__init__(player,animationset,animation)
        self.rect = buildingRect
        self.modifyx = 0
        self.modifyy = 0
        self.regionselectable = False
    
    def get_rect(self):
        self.rect.width = self.size * 8
        self.rect.height = self.size * 4
        self.rect.center = (self.x,self.y)
        return self.rect
    
    def __drawBuildingBloodBar(self,screen,mng,offsetx,offsety):
        rotate = 30
        if self.HP >= self.fullHP/2:
            ngrid = self.HP * mng / self.fullHP
            blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
            screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
        elif self.HP >= self.fullHP/4:
            ngrid = self.HP * mng / self.fullHP
            blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
            screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))
        else:
            ngrid = self.HP * mng / self.fullHP
            blood = longBuildingHealthBlood.subsurface(0,0,ngrid*10,10)
            screen.blit(pygame.transform.rotate(blood,rotate),(self.x-offsetx,self.y-offsety))

    def drawLongBloodBar(self,screen):
        self.__drawBuildingBloodBar(screen,30,200,200)
    def drawShortBloodBar(self,screen):
        self.__drawBuildingBloodBar(screen,15,100,150)
    def drawDefenceBloodBar(self,screen):
        self.__drawBuildingBloodBar(screen,4,50,50)

class AirCmd(Building):
    def __init__(self,player,animation=None):
        animationset = aircmdAnimation
        super(AirCmd,self).__init__(player,animationset,animation)
        self.size = sizeofunit["AirCmd"]
        self.fullHP = 1000
        self.HP = self.fullHP
        self.name = "AirCmd"
        self.power = -25
    def drawBloodBar(self,screen):
        self.drawShortBloodBar(screen)
classmap["AirCmd"] = AirCmd

class Power(Building):
    def __init__(self,player,animation=None):
        animationset = powerAnimation
        super(Power,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Power"]
        self.fullHP = 1000
        self.HP = self.fullHP
        self.name = "Power"
        self.power = 200
    def drawBloodBar(self,screen):
        self.drawShortBloodBar(screen)
classmap["Power"] = Power
        
class Grefn(Building):
    def __init__(self,player,animation=None):
        animationset = grefnAnimation
        super(Grefn,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Grefn"]
        self.fullHP = 2000
        self.HP = self.fullHP
        self.name = "Grefn"
        self.power = -35
    def drawBloodBar(self,screen):
        self.drawShortBloodBar(screen)
classmap["Grefn"] = Grefn
        
class Gpile(Building):
    def __init__(self,player,animation=None):
        animationset = gpileAnimation
        super(Gpile,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Gpile"]
        self.fullHP = 1000
        self.HP = self.fullHP
        self.name = "Gpile"
        self.power = -25
    def drawBloodBar(self,screen):
        self.drawShortBloodBar(screen)
classmap["Gpile"] = Gpile
        
class Gyard(Building):
    def __init__(self,player,animation=None):
        animationset = gyardAnimation
        super(Gyard,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Gyard"]
        self.fullHP = 1500
        self.HP = self.fullHP
        self.name = "Gyard"
        self.power = -25
    def drawBloodBar(self,screen):
        self.drawLongBloodBar(screen)
classmap["Gyard"] = Gyard
        
class Gweap(Building):
    def __init__(self,player,animation=None):
        animationset = gweapAnimation
        super(Gweap,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Gweap"]
        self.fullHP = 1000
        self.HP = self.fullHP
        self.name = "Gweap"
        self.power = -25
    def drawBloodBar(self,screen):
        self.drawShortBloodBar(screen)
classmap["Gweap"] = Gweap
        
class Gcnst(Building):
    def __init__(self,player,animation=None):
        animationset = gcnstAnimation
        super(Gcnst,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Gcnst"]
        self.fullHP = 3000
        self.HP = self.fullHP
        self.name = "Gcnst"
    def drawBloodBar(self,screen):
        self.drawLongBloodBar(screen)
classmap["Gcnst"] = Gcnst
        
class Gpill(Building):
    def __init__(self,player,animation=None):
        animationset = gpillAnimation
        super(Gpill,self).__init__(player,animationset,animation)
        self.size = sizeofunit["Gpill"]
        self.fullHP = 400
        self.HP = self.fullHP
        self.name = "Gpill"
    def drawBloodBar(self,screen):
        self.drawDefenceBloodBar(screen)
classmap["Gpill"] = Gpill

class PowerAnimation(AnimationSet):
    def __init__(self):
        super(PowerAnimation,self).__init__()
        image = images["power"]
        offsetx,offsety = 99,132
        self.originalAnimation = "build"
        width,height = 213,165
        playeroffset = 330
        
        x,y,m,n = 0,165,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,8,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 1704,0,8,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class GrefnAnimation(AnimationSet):
    def __init__(self):
        super(GrefnAnimation,self).__init__()
        image = images["grefn"]
        offsetx,offsety = 180,224
        self.originalAnimation = "build"
        width,height = 315,294
        playeroffset = 294
        
        x,y,m,n = 630,0,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,1,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 315,0,1,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class GpileAnimation(AnimationSet):
    def __init__(self):
        super(GpileAnimation,self).__init__()
        image = images["gpile"]
        offsetx,offsety = 209,161
        self.originalAnimation = "build"
        width,height = 375,222
        playeroffset = 666
        
        x,y,m,n = 0,444,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,8,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 0,222,8,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class AirCmdAnimation(AnimationSet):
    def __init__(self):
        super(AirCmdAnimation,self).__init__()
        image = images["aircmd"]
        offsetx,offsety = 140,170
        self.originalAnimation = "build"
        width,height = 282,243
        playeroffset = 486
        
        x,y,m,n = 0,243,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,6,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 1692,0,6,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class GyardAnimation(AnimationSet):
    def __init__(self):
        super(GyardAnimation,self).__init__()
        image = images["gyard"]
        offsetx,offsety = 118,282
        self.originalAnimation = "build"
        width,height = 324,345
        playeroffset = 3105
        
        x,y,m,n = 0,2760,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,15,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 0,345,15,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")
        x,y,m,n = 0,690,21,2
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normalbigrepair")
        x,y,m,n = 0,1380,21,2
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroybigrepair")
        x,y,m,n = 0,2070,18,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normalsmallrepair")
        x,y,m,n = 0,2415,18,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroysmallrepair")
            
class GweapAnimation(AnimationSet):
    def __init__(self):
        super(GweapAnimation,self).__init__()
        image = images["gweap"]
        offsetx,offsety = 228,234
        self.originalAnimation = "build"
        width,height = 399,336
        playeroffset = 1008
        
        x,y,m,n = 0,672,25,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        
        x,y,m,n = 0,0,15,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        
        x,y,m,n = 0,336,15,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class GcnstAnimation(AnimationSet):
    def __init__(self):
        super(GcnstAnimation,self).__init__()
        image = images["gcnst"]
        offsetx,offsety = 213,263
        self.originalAnimation = "build"
        width,height = 426,339
        playeroffset = 1356
        
        x,y,i0,j0,left,right,count = 0,678,0,0,0,20,29
        for player in range(numofplayer):
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            self.addAnimation("build_%d"%player,animation)
            y += playeroffset
        
        x,y,m,n = 0,0,20,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 0,339,20,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")

class GpillAnimation(AnimationSet):
    def __init__(self):
        super(GpillAnimation,self).__init__()
        image = images["gpill"]
        offsetx,offsety = 49,64
        self.originalAnimation = "build"
        width,height = 102,96
        playeroffset = 96
        
        x,y,m,n = 204,0,8,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"build",False)
        x,y,m,n = 0,0,1,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"normal",True,None,"build")
        x,y,m,n = 102,0,1,1
        self.addAnimationFromSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety,playeroffset,"destroy")
