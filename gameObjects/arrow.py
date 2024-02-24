from . import Mobile,Drawable
from FSMs import WalkingFSM
from utils import vec, magnitude, scale, RESOLUTION


from pygame.locals import *

import pygame
import numpy as np


class Arrow(Drawable):
   def __init__(self, position,angle):
      super().__init__(position, "arrowMed.png")

      #setting speed and direction
      self.speed=400
   

      #new velocity
      self.velocity = vec(np.cos(angle)*self.speed, np.sin(angle)* self.speed)
        

      
      
   def handleEvent(self, event):
      #collides with target
      pass



   def updateMovement(self):
      #keep it going after unpause
      pass
      

   

   def update(self, seconds, colliders, targets):
       
      # if magnitude(self.velocity) > self.maxVelocity:
      #       self.velocity = scale(self.velocity, self.maxVelocity)
      self.position += self.velocity * seconds

      #hit = self.doesCollideList(targets)
      #print("hi")

      hitBox = pygame.Rect((self.position), (self.image.get_width(), self.image.get_height()))

###################### ASK ABOUT LR COLLISIONS
      hit=False
      for block in colliders:
         if hitBox.colliderect(block):
            #print("hi")
            hit = True

      super().update(seconds)
      return hit
      
      
   
   
  