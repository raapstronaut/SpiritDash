import pygame
from game import Game

def main():
    "main entry point of the game"

    pygame.init()

    game = Game()
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()    