from . import Drawable
from utils import SpriteManager
import pygame

class Animated(Drawable):
    
    def __init__(self, position=(0,0), fileName=""):
        super().__init__(position, fileName, (0,0))
        self.fileName = fileName
        self.row = 0
        self.frame = 0
        self.nFrames = 1
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None
        self.orientation = 0
    
    def update(self, seconds):
        if self.FSManimated:
            self.FSManimated.updateState()
            
        if not self.animate:
            return
        
        self.animationTimer += seconds 
           
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond
            if self.orientation ==0:

                self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                        (self.frame, self.row))
            else:
                self.image = pygame.transform.flip(SpriteManager.getInstance().getSprite(self.fileName,
                                        (self.frame, self.row)), True, False)
