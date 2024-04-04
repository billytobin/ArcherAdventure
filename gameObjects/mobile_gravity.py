from . import Mobile
from FSMs import constVelocityFSM,GravityFSM
from utils import vec, RESOLUTION, OFFSETS

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
        #hitBox = pygame.Rect((self.position), (self.image.get_width(), self.image.get_height()))
        #print(hitBox)
        hitBox = pygame.Rect((self.position[0]+OFFSETS[0], self.position[1]+OFFSETS[1]), (OFFSETS[2],OFFSETS[3]))
        #print(hitBox)


        fallFlag = True
        #print(hitBox[3])
        for blck in colliders:
            block=blck.getCollisionRect()
            clip_box = hitBox.clip(block)
            #print("clip"+ str(clip_box))

            if self.LR =="left" and hitBox.colliderect(block) and block.x<hitBox.x and (block.x+block.width) > hitBox.x and clip_box.height >=5: # and (clip_box.x+clip_box.width)==block.y:
                #print(clip_box)
                self.position[0] += clip_box.width
                #print(clip_box.height, "hi")
                self.LR.stop()
            if self.LR =="right" and hitBox.colliderect(block) and block.x < (hitBox.x+hitBox.width) and (block.x+block.width) > (hitBox.x+hitBox.width) and clip_box.height >=5:
                self.position[1] -= clip_box.width
                self.LR.stop()
            
        


            if self.UD != "grounded" and hitBox.colliderect(block):
###########  #if self.UD == "grounded" and self.doesCollide(block):
                if block.y >= (hitBox.top+hitBox.height-5) and self.UD == "falling":
                    #print(self.position[1])
                    self.UD.land()
                    #print("landed")
                    #self.position[1] -= clip_box.height -5
                    self.position[1] = block.y - hitBox[3]-24
                    #print(self.position[1])
                    # self.UD.land()
                    
                elif block.y < hitBox.y:
                    if self.UD != "falling":

                        self.UD.fall()
                    
                    # if self.UD ==  "jumping":
                    #print(self.position[1])    
                    self.UD.jumpTimer=0
                    self.velocity[1]=0
                    self.position[1] += clip_box.height*2
            if self.UD == "grounded" and hitBox.colliderect(block):
                #if block.x<hitBox.x and (block.x+block.width) > hitBox.x:
############ #if self.UD == "grounded" and self.doesCollide(block):
                #print(block.y, hitBox.top)
                if block.y>=hitBox.top:
                    fallFlag= False
                    #print("yes")
           ### if moving left, collide with wall, and the wall is to left, stop
            # if self.LR =="left" and hitBox.colliderect(block) and block.x<hitBox.x and (block.x+block.width) > hitBox.x and clip_box.height >=5: # and (clip_box.x+clip_box.width)==block.y:
            #     #print(clip_box)
            #     self.position[0] += clip_box.width
            #     #print(clip_box.height, "hi")
            #     self.LR.stop()
            # if self.LR =="right" and hitBox.colliderect(block) and block.x < (hitBox.x+hitBox.width) and (block.x+block.width) > (hitBox.x+hitBox.width) and clip_box.height >=5:
            #     self.position[1] -= clip_box.width
            #     self.LR.stop()
                
        
        if self.UD == "grounded" and fallFlag==True:
            self.UD.fall()



        super().update(seconds)