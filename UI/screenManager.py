from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects import GameEngine

from pygame.locals import *

class ScreenManager(object):
      
    def __init__(self):
        self.game = GameEngine()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.lose_text= TextEntry(vec(0,0), "You Lost! Press exc to quit.")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        self.lose_text.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("forest.jpg", fontName="default8")
        self.mainMenu.addOption("start", "Press 1 to start Game",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        self.mainMenu.addOption("exit", "Press 2 to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
            
            if self.state == "lost":
                #print("hi")
                self.lose_text.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
    
    def handleEvent(self, event):
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            
            # if len(self.game.active_targets) == len(self.game.targets):
            #     self.state.lose()
                
            else:
                self.game.handleEvent(event)
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
            
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
    