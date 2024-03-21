from . import Mobile,Drawable
from FSMs import WalkingFSM
from utils import vec, magnitude, scale, RESOLUTION


from pygame.locals import *

import pygame
import numpy as np


class Arrow(Drawable):
   def __init__(self, position,angle):
      super().__init__(position, "arrowMed.png", angle=angle*-180/np.pi)

      #setting speed and direction
      self.speed=400

      # self.angle = 0
      self.rotated_image = pygame.transform.rotate(self.image, angle*-180/np.pi)
      
      #new velocity
      self.velocity = vec(np.cos(angle)*self.speed, np.sin(angle)* self.speed)
        

      
      
   def handleEvent(self, event):
      #collides with target
      pass



   def updateMovement(self):
      #keep it going after unpause
      pass

   def draw(self, drawSurface):
            
      drawSurface.blit(self.rotated_image, list(map(int, self.position)))
      

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
      
      for block in targets:
         if hitBox.colliderect(block.getHitBox()):
            hit=True

      super().update(seconds)
      return hit
      
      
   
   
  