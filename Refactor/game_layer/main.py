from game import Game
from ..system_layer.main_system import MainSystem

if __name__ == "__main__":
    game = Game(800, 600, 12)
    game.add_system(MainSystem())
    game.run()