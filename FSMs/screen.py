from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    game     = State()
    game2 = State()
    paused   = State()
    lost = State()
    
    pause = game.to(paused) | paused.to(game) | \
            game2.to(paused) | paused.to(game2) | \
            mainMenu.to.itself(internal=True)
    
    startGame = mainMenu.to(game)
    startGame2 = mainMenu.to(game2)
    quitGame  = game.to(mainMenu) | \
                game2.to(mainMenu) | \
                paused.to.itself(internal=True)
    lose = game.to(lost)
    
    def isInGame(self):
        return self == "game" or self == "paused" or self == "game2"
    
    def on_enter_game(self):
        self.obj.game.startLevel()
        self.obj.game.archer.updateMovement()
    