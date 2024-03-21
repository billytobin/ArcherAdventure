import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec


class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None, angle=0, rotate=0):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
            if rotate != 0:
                self.unrotated = SpriteManager.getInstance().getSprite(fileName, offset)
        self.position  = vec(*position)
        self.imageName = fileName
        self.angle = angle
        #for Bow
        # if self.angle == 0:
        #     self.rotate =  False
        # else:
        #     self.rotate= True
        self.rotate=False
        #print(self.angle)
        
    def setDrawPosition(self):
        if self.rotate:
            center = vec(*self.unrotated.get_rect().center)
            self.image = pygame.transform.rotate(self.unrotated, self.angle)
            rotatedCenter = vec(*self.image.get_rect().center)
            self.drawPosition = self.position - center - rotatedCenter
            #print("adf")    
        else:
            self.drawPosition = self.position

    def draw(self, drawSurface):
        self.setDrawPosition()
            
        drawSurface.blit(self.image, list(map(int, self.drawPosition)))
       
    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect =  self.image.get_rect()
        newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        #print(rects)
        return self.getCollisionRect().collidelist(rects)   