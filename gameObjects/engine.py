import pygame

from . import Drawable, Archer, Arrow, Target

import random

from math import atan2, degrees, pi

from utils import vec, RESOLUTION, SCALE, WORLD_SIZE
import numpy as np

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.archer = Archer((300,300))
        self.size = vec(*RESOLUTION)
        #self.background = Drawable((0,0), "background.png")
        self.background = Drawable((0,0), "forest.jpg")


        #things that can collide
        self.colliders = []


        self.drawLevel("level1")
        

        #self.colliders = [self.ledge1,self.ledge2, self.ledge3, self.ledge4]
        #self.colliders=self.floor
        #print(self.colliders)

        #targets 
        self.t1 = Target((10,200),1)
        self.t2=Target((50, 300),1)
        self.t3=Target((300,20),1)
        self.t4=Target((200,50),1)
        self.t5=Target((390,70),1)
        self.t6=Target((340,300),1)


        self.targets = [self.t1,self.t2, self.t3,self.t4,self.t5,self.t6]
        self.active_targets=[]#[self.t1,self.t2, self.t3]#,self.t4,self.t5]
        self.timer = 0.5

        self.bow_timer=0
        self.bow_timer_start=False

        self.target_timer_max=1.5
        self.target_timer=0

        self.count=0
        self.font = pygame.font.SysFont("Arial", 50)

        #arrows
        self.arrows = []
        
    
    def drawLevel(self, levelName):
        f = open("utils/levels/"+levelName+".txt")
        for line_num, line in enumerate(f):
            for char_num, char in enumerate(line):
                if char == "x":
                    self.colliders.append(Drawable(vec(char_num*16, line_num*16), "grass.png"))
                elif char == "a":
                    self.colliders.append(Drawable(vec(char_num*16, line_num*16), "wood.png"))

    


    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.archer.draw(drawSurface)

        for i in self.arrows:
            i.draw(drawSurface)

        message = self.font.render(str(self.count), False, (0,0,0))

        drawSurface.blit(message, (RESOLUTION[0]-(message.get_width()),0))
        
        
        #print(self.targets)
        for i in self.active_targets:
            i.draw(drawSurface)

        for i in self.colliders:
            #pygame.draw.rect(drawSurface,(0,0,0), i)
            i.draw(drawSurface)
            
    def handleEvent(self, event):
        self.archer.handleEvent(event)

        #print(self.archer.timer)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bow_timer_start=True


        if event.type == pygame.MOUSEBUTTONUP:
            
            
            position = self.archer.position +vec(18,20)
            click_location = vec(*event.pos) // SCALE -vec(0,0)

            dx = click_location[0] - position[0]
            dy = click_location[1] - position[1]
            angle = atan2(dy,dx)
            #rads %= 2*pi
            #print(str(self.archer.timer) + "       xxxxxxxxxxxxxxxxxxxxxxxxxx")#, angle)
            if self.archer.timer == self.archer.shoot_time:
                speed= 200
                if self.bow_timer>0.1:
                    speed = 500 * self.bow_timer + 200
                elif self.bow_timer>0.8:
                    speed = 600
                self.arrows.append(Arrow(position, angle, speed) )
                #print(str(self.arrows) + ' self.arrows')
                
            self.bow_timer_start=False
            self.bow_timer=0
        
        
        
    
    def update(self, seconds):
        
        self.archer.update(seconds, self.colliders)

        not_hit_arrows=[]
        hit_targets = []
        for i in self.arrows:
            
            hit_arrow=i.update(seconds, self.colliders, self.active_targets)

            #print("97")
            
            for j in self.active_targets:
                #print("hi"+ str(j))
                hit_target = j.update(seconds, i)
                #print("hi")
                if hit_target == True:
                    self.count+=1
                    hit_targets.append(j)
            
            if hit_arrow == False:
                not_hit_arrows.append(i)

        for i in hit_targets:

            self.active_targets.remove(i)
        
            
        #print("after update 111")

        self.arrows = not_hit_arrows

        #add new target every 3 seconds and
        #get complement of active targets and random targets
        #choose random
        if self.target_timer<0:
             if len(self.active_targets)!= len(self.targets):
                self.active_targets.append(random.choice(list(set(self.targets)-set(self.active_targets))))
                #self.active_targets.append(random.choice(self.targets))
                self.target_timer=self.target_timer_max
        else:
             self.target_timer -= seconds

        

       #self.active_targets.append(target)
        if self.bow_timer_start:
            self.bow_timer+= seconds
        
        
        Drawable.updateOffset(self.archer, self.size)
    

