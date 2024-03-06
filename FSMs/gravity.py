from . import AbstractGameFSM

from statemachine import State

class GravityFSM(AbstractGameFSM):

    #states
    grounded = State(initial=True)
    jumping = State()
    falling = State()

    #events
    jump = grounded.to(jumping) #| falling.to.itself(internal=True)
    fall = jumping.to(falling)  | grounded.to(falling)
    land = falling.to(grounded) | jumping.to(grounded)


    def __init__(self, obj):
        super().__init__(obj) 
        self.jumpTimer = 0
        self.gravity = 220
        self.jumpSpeed = 200
        self.jumpTime = 0.2

        

    def updateState(self):
        if self.canFall() and self == "jumping":
            self.fall()

    def canFall(self):
        return self.jumpTimer < 0
    
    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime

    def update(self, seconds=0):
        self.updateState()

        #print(self.current_state)
        if self == "falling":
            #if head bonks
            # if self.jumpTimer > 0:
            #     #self.jumpTimer = 0
            #     self.obj.velocity[1]=0
            self.obj.velocity[1] += self.gravity * seconds
        elif self == "jumping":
            self.obj.velocity[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        else:
            self.obj.velocity[1] = 0

