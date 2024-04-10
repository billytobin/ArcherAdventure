from . import MobileGravity, SpriteManager
from FSMs import WalkingFSM
from utils import vec, RESOLUTION, SCALE
import math


from pygame.locals import *

import pygame
import numpy as np


class Archer(MobileGravity):
   def __init__(self, position):
      #super().__init__(position, "archer_SL.png")
      super().__init__(position, "Shinobi_Spritelist.png")
      #super().__init__(position, "Samurai_Spritelist.png")
        
      # Animation variables specific to archer character
      self.animate = True
      self.framesPerSecond = 2 
      self.nFrames = 2
      self.shoot_time = 0.5
      self.timer = 0
      self.bow =SpriteManager.getInstance().getSprite("bow1.png")
      self.bow_pivot = (2,6)
      self.bowCopy = self.bow.copy()
      self._angle = 0
      
      self.nFramesList = {
         "moving"   : 8,
         "standing" : 6,
         "jumping" : 10
      }
      
      self.rowList = {
         "moving"   : 2,
         "standing" : 0,
         "jumping" : 3
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 6,
         "jumping": 10
      }
            
      self.FSManimated = WalkingFSM(self)

      
      
   def handleEvent(self, event):

      if event.type == pygame.MOUSEMOTION:

         position = self.position +vec(24,24)
         click_location = vec(*event.pos) // SCALE -vec(0,0)

         dx = click_location[0] - position[0]
         dy = click_location[1] - position[1]
         self._angle = math.atan2(dy,dx)
         self._angle *= -180/np.pi
         self._angle-=45



      if event.type == KEYDOWN:
         if event.key == K_w and self.UD != "jumping" and self.UD != "falling":
             self.UD.on_enter_jumping()
             self.UD.jump()
             
         # elif event.key == K_DOWN:
         #    self.UD.increase()
            
         elif event.key == K_a:
            self.LR.moveLeft()
            
         elif event.key == K_d:
            self.LR.moveRight()
            
      elif event.type == KEYUP:
         # if event.key == K_UP:
         #    self.UD.stop_decrease()
             
         # elif event.key == K_DOWN:
         #    self.UD.stop_increase()
             
            
         if event.key == K_a:
            self.LR.stop()
            
         elif event.key == K_d:
            self.LR.stop()
      elif event.type == MOUSEBUTTONUP:
          if self.timer == 0:
             
            self.timer = self.shoot_time

   def updateMovement(self):
      pressed = pygame.key.get_pressed()

      # if not pressed[pygame.K_UP] and self.UD == "decrease":
      #    self.UD.stop_decrease()
      # if not pressed[pygame.K_DOWN] and self.UD == "increase":
      #    self.UD.stop_increase()
         
      if not pressed[pygame.K_LEFT] and self.LR == "left":
         self.LR.stop()
      if not pressed[pygame.K_RIGHT] and self.LR == "right":
         self.LR.stop()


   def draw(self, drawSurface):
         self.setDrawPosition()
            
         drawSurface.blit(self.image, list(map(int, self.drawPosition)))

         rotate= pygame.transform.rotate(self.bow, int(self._angle))
         new_rect =rotate.get_rect(center = self.bow.get_rect(topleft = (self.position+vec(3,9))).center)
         #
            
         drawSurface.blit(self.image, list(map(int, self.drawPosition)))
         self.bowCopy= pygame.transform.rotate(self.bow, int(self._angle))
         drawSurface.blit(rotate, new_rect)

         #drawSurface.blit(self.bowCopy,bow_drawPosition+vec(12,12))

        #)

         # image_rect =  self.bowCopy.get_rect(topleft = (self.position[0] - self.bow_pivot[0], self.position[1]-self.bow_pivot[1]))
         # offset_center_to_pivot = pygame.math.Vector2(self.bow_pivot) - image_rect.center
         # rotated_offset = offset_center_to_pivot.rotate(-self._angle)
         # rotated_image_center = (self.position[0] - rotated_offset.x, self.position[1] - rotated_offset.y)
         # rotated_image = pygame.transform.rotate(self.bowCopy, self._angle)
         # rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
         # drawSurface.blit(rotated_image, rotated_image_rect)
           
        #drawSurface.blit(self.bowCopy,bow_drawPosition+vec(12,12)) 
    
      

   

   def update(self, seconds, colliders=None):
      if self.timer > 0:
         self.timer -= seconds
      else:
         self.timer = 0
   

      super().update(seconds, colliders)
   
   
  