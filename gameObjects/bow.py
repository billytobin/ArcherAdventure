from . import Mobile,Drawable
from FSMs import WalkingFSM
from utils import vec, magnitude, scale, RESOLUTION


from pygame.locals import *

import pygame
import numpy as np


class Bow(Drawable):
   def __init__(self, position,angle):
      super().__init__(position, "arrowMed.png", angle=angle*-180/np.pi)

      #setting speed and direction
      self.speed=400

      # self.angle = 0
      self.rotated_image = pygame.transform.rotate(self.image, angle*-180/np.pi)
      self.center = vec(*self.rotated_image.get_rect().center)

      #new velocity
      self.velocity = vec(np.cos(angle)*self.speed, np.sin(angle)* self.speed)
        

      
      
   def handleEvent(self, event):
      if event.type == pygame.MOUSEMOTION:
         mousePos = Vector2(*event.pos)
         self._angle = math.atan2(*(mousePos - (self.getPosition() + Vector2(*self.getCenter()))).normalize()) \
            - math.pi / 2



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
      
      #create a moving center based on the position and center of the rotated image      
      moving_center = (self.position[0]+self.center[0],self.position[1]+self.center[1])
      #the create hitbox from it
      hitBox = pygame.Rect((moving_center[0]-3, moving_center[1]-3), (6, 6))

      hit=False
      for block in colliders:
         if hitBox.colliderect(block):
            #print("hi")
            hit = True
      
      for block in targets:
         if hitBox.colliderect(block.getHitBox()):
            hit=True
           # print("hi!!")

      super().update(seconds)
      return hit
      

   def get_center(self):
      '''Returns the moving center of the arrow -- for collisions with target and wall.'''
      moving_center = (self.position[0]+self.center[0],self.position[1]+self.center[1])
      #the create hitbox from it
      hitBox = pygame.Rect((moving_center[0]-3, moving_center[1]-3), (6, 6))
      return hitBox
   
  