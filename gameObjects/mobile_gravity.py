from . import Mobile
from FSMs import constVelocityFSM,GravityFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class MobileGravity(Mobile):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)

        self.LR = constVelocityFSM(self)
        self.UD = GravityFSM(self)

    def update(self, seconds, colliders=None): 
        self.LR.update(seconds)
        self.UD.update(seconds)

        #handle collisions with each thing in colliders
        hitBox = pygame.Rect((self.position), (self.image.get_width(), self.image.get_height()))
        
        fallFlag = True

        for block in colliders:
            clip_box = hitBox.clip(block)
            #print("clip"+ str(clip_box))
            if self.UD != "grounded" and hitBox.colliderect(block):
###########  #if self.UD == "grounded" and self.doesCollide(block):
                if block.y >= hitBox.y and self.UD == "falling":
                    self.position[1] -= clip_box.height
                    self.UD.land()
                    
                elif block.y < hitBox.y:
                    if self.UD != "falling":

                        self.UD.fall()
                        
                    self.UD.jumpTimer=0
                    self.velocity[1]=0
                    self.position[1] += clip_box.height*2
            if self.UD == "grounded" and hitBox.colliderect(block):
############ #if self.UD == "grounded" and self.doesCollide(block):
                if block.y>hitBox.y:
                    fallFlag= False
            #if moving left, collide with wall, and the wall is to left, stop
            # if self.LR =="left" and hitBox.colliderect(block) and block.x < hitBox.x and clip_box.y==block.y:
            #     self.position[1] -= clip_box.height
            #     print(clip_box.height)
            #     self.LR.stop()
            # if self.LR =="right" and hitBox.colliderect(block) and block.x > hitBox.x and clip_box.y==block.y:
            #     self.position[1] -= clip_box.height
            #     self.LR.stop()
                
        
        if self.UD == "grounded" and fallFlag==True:
            self.UD.fall()



        super().update(seconds)