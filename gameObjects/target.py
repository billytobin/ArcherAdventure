from . import Mobile,Drawable
from FSMs import WalkingFSM
from utils import vec, magnitude, scale, RESOLUTION


from pygame.locals import *

import pygame
import numpy as np


class Target(Drawable):
   def __init__(self, position, orientation):
      super().__init__(position, "targetSmaller.png")
      
      
   def handleEvent(self, event):
      pass

   def updateMovement(self):
      #keep it going after unpause
      pass
      


   def update(self, seconds, arrow, end_update=None):
      super().update(seconds) 

      hitBox = pygame.Rect((self.position), (self.image.get_width(), self.image.get_height()))
      arrow_hitBox = pygame.Rect((arrow.position), (arrow.image.get_width(), arrow.image.get_height()))
      #
      # print("hi")
      #print(hitBox.colliderect(arrow_hitBox))
      
      return hitBox.colliderect(arrow_hitBox)
         
      
      
   
   
  