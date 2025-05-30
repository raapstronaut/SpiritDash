import pygame
from game import Game

def main():
    "fungsi utama game"

    pygame.init()

    game = Game()
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()    