from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    game     = State()
    paused   = State()
    lost = State()
    
    pause = game.to(paused) | paused.to(game) | \
            mainMenu.to.itself(internal=True)
    
    startGame = mainMenu.to(game)
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
    lose = game.to(lost)
    
    def isInGame(self):
        return self == "game" or self == "paused"
    
    def on_enter_game(self):
        self.obj.game.archer.updateMovement()
    