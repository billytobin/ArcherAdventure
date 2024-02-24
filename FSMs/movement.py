from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION
import pygame

from statemachine import State

class MovementFSM(AbstractGameFSM):

    
    
    def __init__(self, obj):
        super().__init__(obj)
        #self.direction = vec(0,0)
        
    
    def update(self, seconds):
        # Add out of bounds checks here
        moveHitBox = pygame.Rect((self.obj.position), (self.obj.image.get_width(), self.obj.image.get_height()))
        if moveHitBox.bottom > RESOLUTION[1]:
            if self.obj.velocity[1]>0:
                self.obj.velocity[1]=0
        elif moveHitBox.top < 0:
            if self.obj.velocity[1]<0:
                self.obj.velocity[1]=0
        if moveHitBox.right > RESOLUTION[0]:
            if self.obj.velocity[0]>0:
                self.obj.velocity[0]=0
        elif moveHitBox.left < 0:
            if self.obj.velocity[0]<0:
                self.obj.velocity[0]=0
                

                
        super().update(seconds)
        


class constVelocityFSM(MovementFSM):
    # Axis-based acceleration with gradual stopping.
    not_moving = State(initial=True)
    left = State()
    right = State()

    moveLeft  = not_moving.to(left) | right.to(left)
    moveRight = not_moving.to(right) | left.to(right)

    stop      = not_moving.to.itself(internal=True) | left.to(not_moving) | \
                    right.to(not_moving)
    
    def __init__(self, obj):
        # self.axis      = axis
        # self.direction = vec(0,0)
        # self.direction[self.axis] = 1
        # self.accel = 200
        self.speed = 100

        super().__init__(obj)

    def update(self, seconds=0):
        if self == "right":
            self.obj.velocity[0] = self.speed
        elif self == "left":
            self.obj.velocity[0] = -self.speed
        else:
            self.obj.velocity[0] = 0
        
        
    
        super().update(seconds)