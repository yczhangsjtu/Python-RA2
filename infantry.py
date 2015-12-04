import pygame

from unit import Unit
from map import getAbsPos, getGridPos
from animation import Animation, AnimationSet
from data import images, classmap
from consts import *


e3Animation = None
adogAnimation = None
directions = ["n","nw","w","sw","s","se","e","ne"]
infantryRect = pygame.Rect(0,0,15,25)
    
def initInfantryAnimations():
    global bloodbarimg, infantryHealthBlood, infantryHurtBlood, infantryDangerBlood
    global e3Animation, adogAnimation, engineerAnimation
    bloodbarimg = images["bloodbar"]
    infantryHealthBlood = bloodbarimg.subsurface(0,0,25,5)
    infantryHurtBlood = bloodbarimg.subsurface(0,4,25,5)
    infantryDangerBlood = bloodbarimg.subsurface(0,8,25,5)
    e3Animation = E3Animation()
    adogAnimation = AdogAnimation()
    engineerAnimation = EngineerAnimation()

class Infantry(Unit):
    def __init__(self,player,animationset,animation=None):
        super(Infantry,self).__init__(player,animationset,animation)
        self.rect = infantryRect
    
    def drawBloodBar(self,screen):
        if self.HP >= self.fullHP/2:
            ngrid = self.HP * 8 / self.fullHP
            screen.blit(infantryHealthBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
        elif self.HP >= self.fullHP/4:
            ngrid = self.HP * 8 / self.fullHP
            screen.blit(infantryHurtBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
        else:
            ngrid = self.HP * 8 / self.fullHP
            screen.blit(infantryDangerBlood.subsurface(0,0,ngrid*3+1,5),(self.x-12,self.y-40))
    
    def step(self,map,characters):
        super(Infantry,self).step(map,characters)
        if self.target != None:
            if isinstance(self.target,tuple):
                x,y = self.target
                self.moveTo(x,y,characters)
            else:
                x,y = self.target.offsetx,self.target.offsety
                if dist(self.offsetx,self.offsety,x,y) > self.range:
                    self.moveTo(x,y,characters)
        
        
class Adog(Infantry):
    def __init__(self,player,animation=None):
        animationset = adogAnimation
        super(Adog,self).__init__(player,animationset,animation)
        self.speed = 10
        self.size = sizeofunit["Adog"]
        self.range = 0
        self.fullHP = 100
        self.HP = self.fullHP
        self.name = "Adog"
classmap["Adog"] = Adog

class E3(Infantry):
    def __init__(self,player,animation=None):
        animationset = e3Animation
        super(E3,self).__init__(player,animationset,animation)
        self.speed = 4
        self.size = sizeofunit["E3"]
        self.range = 100
        self.fullHP = 100
        self.HP = self.fullHP
        self.name = "E3"
classmap["E3"] = E3

class Engineer(Infantry):
    def __init__(self,player,animation=None):
        animationset = engineerAnimation
        super(Engineer,self).__init__(player,animationset,animation)
        self.speed = 7
        self.size = sizeofunit["Engineer"]
        self.range = 0
        self.fullHP = 100
        self.HP = self.fullHP
        self.name = "Engineer"
classmap["Engineer"] = Engineer

class E3Animation(AnimationSet):
    def __init__(self):
        super(E3Animation,self).__init__()
        image = images["E3"]
        offsetx,offsety = 57,37
        self.originalAnimation = "runsw"
        width,height = 118,72
        playeroffset = 504
        
        y,m,n = 0,1,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                self.addAnimation("stand%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        y,m,n = 216,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("run%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
            
        y,m,n = 288,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("crawl%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        y,m,n = 360,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("attack%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
            
        y,m,n = 432,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("crawlattack%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        x,y,m,n = 1110,72,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("cheer_%d"%(player),animation)
            y += playeroffset
            
        x,y,m,n = 0,72,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("squeez_%d"%(player),animation)
            y += playeroffset
        
        x,y,m,n = 2220,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die1_%d"%(player),animation)
            y += playeroffset
            
        x,y,m,n = 3330,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die2_%d"%(player),animation)
            y += playeroffset
            
class AdogAnimation(AnimationSet):
    def __init__(self):
        super(AdogAnimation,self).__init__()
        image = images["adog"]
        offsetx,offsety = 36,38
        self.originalAnimation = "runsw"
        width,height = 74,72
        playeroffset = 288
        
        y,m,n = 0,1,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                self.addAnimation("stand%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        y,m,n = 72,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("run%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        y,m,n = 216,6,1
        for player in range(2):
            x = 0
            for direction in directions:
                animation = Animation()
                animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("attack%s_%d"%(direction,player),animation)
                x += width * m
            y += playeroffset
        
        x,y,m,n = 0,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("tail_%d"%(player),animation)
            y += playeroffset
            
        x,y,m,n = 1110,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("squeez_%d"%(player),animation)
            y += playeroffset
        
        x,y,m,n = 2220,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die1_%d"%(player),animation)
            y += playeroffset
            
        x,y,m,n = 3330,144,15,1
        for player in range(2):
            animation = Animation()
            animation.addImageSpriteSheet(image,x,y,width,height,m,n,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die2_%d"%(player),animation)
            y += playeroffset
            
class EngineerAnimation(AnimationSet):
    def __init__(self):
        super(EngineerAnimation,self).__init__()
        image = images["engineer"]
        offsetx,offsety = 37,38
        self.originalAnimation = "runsw"
        width,height = 76,80
        playeroffset = 880
        left,right = 0,23
        x,y = 0,0
        
        for player in range(2):
            i0,j0 = 0,0

            count = 1
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                self.addAnimation("stand%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right
        
            count = 6
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("run%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right
        
            count = 15
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("stool_%d"%(player),animation)
            i0 += count
            j0 += i0 / right
            i0 %= right
            
            count = 15
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            animation.next = self.getAnimation("standsw_%d"%(player))
            self.addAnimation("read_%d"%(player),animation)
            i0 += count
            j0 += i0 / right
            i0 %= right

            count = 6
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("crawl%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right
        
            count = 15
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die1_%d"%(player),animation)
            i0 += count
            j0 += i0 / right
            i0 %= right
            
            count = 15
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            self.addAnimation("die2_%d"%(player),animation)
            i0 += count
            j0 += i0 / right
            i0 %= right

            count = 6
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("search%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right

            count = 2
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                animation.loop = False
                self.addAnimation("getdown%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right

            count = 2
            for direction in directions:
                animation = Animation()
                animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
                animation.loop = False
                animation.next = self.getAnimation("stand%s_%d"%(direction,player))
                self.addAnimation("getup%s_%d"%(direction,player),animation)
                i0 += count
                j0 += i0 / right
                i0 %= right

            count = 9
            animation = Animation()
            animation.addBrokenSpriteSheet(image,x,y,i0,j0,width,height,left,right,count,offsetx,offsety)
            animation.loop = False
            self.addAnimation("cheer_%d"%(player),animation)
            i0 += count
            j0 += i0 / right
            i0 %= right

            y += playeroffset
            
