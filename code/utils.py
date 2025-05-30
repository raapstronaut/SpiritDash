import pygame
from settings import screen, highscore_file, fntGame, fntover

def show_score(text, color, x, y):
    "Display Score menggunakan font"

    font = pygame.font.Font(fntGame, 30)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def show_gameover(text, color, x, y):
    font = pygame.font.Font(fntover, 30)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def load_highscore():
    "mengimport high score dari file"
    try:
        with open(highscore_file, 'r') as file:
            highscore_data = int(file.read())
        return highscore_data
    except (FileNotFoundError, ValueError):
        #jika file tidak ada atau data tidak valid, buat file baru dengan nilai awal 0
        change_highscore(0)
        return 0
    
def change_highscore(new_highscore):
    "update file high score "
    with open(highscore_file, 'w') as f:
        f.write(str(new_highscore))

def is_off_screen(sprite):
    "Cek character keluar dari layar"
    return sprite.rect.right < 0   

def show_text(text, size, color, x, y):
    "Display text on the screen"
    font = pygame.font.Font(fntover, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))