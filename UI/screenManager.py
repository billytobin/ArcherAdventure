from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects import GameEngine

from pygame.locals import *
import pygame

class ScreenManager(object):
      
    def __init__(self):
        self.game = GameEngine()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.lose_text= TextEntry(vec(0,0), "Press M to go to menu")

        self.game_timer = 30
        self.isPlaying = True

        self.font = pygame.font.SysFont("Arial", 50)

        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        self.lose_text.position = vec(*midpoint)-vec(70,0)
        
        self.mainMenu = EventMenu("forestMenu.jpg", fontName="default8", color=(0,0,0))
        self.mainMenu.addOption("level1", "Press 1 to play Level 1",
                                 RESOLUTION // 2 - vec(0,100),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        self.mainMenu.addOption("level2", "Press 2 to play Level 2",
                                 RESOLUTION // 2 - vec(0,33),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        self.mainMenu.addOption("level3", "Press 3 to play Level 3",
                                 RESOLUTION // 2 + vec(0,33),
                                 lambda x: x.type == KEYDOWN and x.key == K_3,
                                 center="both")
        self.mainMenu.addOption("chars", "Press C to pick your character",
                                 RESOLUTION // 2 + vec(0,100),
                                 lambda x: x.type == KEYDOWN and x.key == K_c,
                                 center="both")
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            if self.isPlaying:
                self.game.draw(drawSurf)
            
                if self.state == "paused":
                    self.pausedText.draw(drawSurf)
                
                message = self.font.render(str(round(self.game_timer,1)), False, (0,0,0))
                
            else:
                self.state.lose()
                #print("hi")
                self.lose_text.draw(drawSurf)

                message = self.font.render("0.0", False, (0,0,0))
            

            drawSurf.blit(message, (5,0))
        
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
        
        elif self.state == "lost":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()

        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            
            if choice == "level1":
                self.game.level=1
                self.isPlaying = True
                self.state.startGame()
            elif choice == "level2":
                self.game.level=2
                self.isPlaying = True
                self.state.startGame()
            elif choice == "level3":
                self.game.level=3
                self.isPlaying = True
                self.state.startGame()
            elif choice == "chars":
                pass
     
    
    def update(self, seconds):      
        
            
        if self.state == "mainMenu":
            self.mainMenu.update(seconds)

        if self.state == "game":
            #doing timer
            self.game_timer-= seconds
            if self.game_timer > 0:
                # end the game
                self.game.update(seconds)
    
            else: 
                self.isPlaying = False
                self.game_timer=30