import pygame
from pygame import mixer
import os
import random


# Initialize Pygame
pygame.init()

# enviroment seting
windowW = 1280
windowH = 800
FPS = 30

# Game setting
obstacle_width = 200
obstacle_height = 500
obstacle_gap = 1

ground_height = 200
ground_width = windowW

#mekanism
gravity = 0.5
character_speed = 6
game_speed = 10
highscore_file = "code/highscore.txt"

#ASSET
#font
fntGame = "assets/font/Bloodlust.ttf"
fntover = "assets/font/EuroHorror.ttf"

#music
bgm = "assets/sound/bgm_menu.wav"
tap = "assets/sound/jump.wav"
die = "assets/sound/die.wav"
tapButton = "assets/sound/tap_button.wav"
skillactive = [
    "assets/sound/sound_gotoku.wav",
    "assets/sound/sound_onre.wav",
    "assets/sound/sound_yurei.wav",
]

bgmStategame = [
    "assets/sound/bgm_main.wav",
    "assets/sound/bgm_main.wav",
    "assets/sound/bgm_main.wav"
]

#image
bgGameSprites = [
    "assets/map/gotoku/bg_gotoku.png",
    "assets/map/onre/bg_onre.png",
    "assets/map/yurei/bg_yurei.png",
]

baseGroundSprites = [
    "assets/map/gotoku/ground_gotoku.png",
    "assets/map/onre/ground_onre.png",
    "assets/map/yurei/ground_yurei.png",
]

obstacleSprites = [
    "assets/map/gotoku/obs_gotoku.png",
    "assets/map/onre/obs_onre.png",
    "assets/map/yurei/obs_yurei.png",
]

hpSprites = [
    "assets/atribute/hp1.png",
    "assets/atribute/hp2.png",
    "assets/atribute/hp3.png",
]

menuSprites = [
    "assets/menu/menu_header_title.png",
    "assets/menu/menu_btn_start.PNG",
    "assets/menu/menu_btn_quit.png",
    "assets/menu/menu_btn_start_normal.png",
    "assets/menu/menu_btn_start_hover.png",
    "assets/menu/menu_btn_quit_normal.png",
    "assets/menu/menu_btn_quit_hover.png",
]

charDescription = [
    "assets/actor/gotoku/gotoku_desc.png",
    "assets/actor/onre/onre_desc.png",
    "assets/actor/yurei/yurei_desc.png",
]

gameInteruptScreen = [
    [
        "assets/menu/pause_txt_bnnr.png",
        "assets/menu/gameover_txt_bnnr.png",
    ]

]

gameStartBtn = "assets/menu/game_btn_start.png"

# inisialisasi screen dan game setting
score_font = pygame.font.Font(fntGame, 45)
gameover_font = pygame.font.Font(fntover, 25)
white = (0, 0, 0)
screen = pygame.display.set_mode((windowW, windowH))
pygame.display.set_caption("Spirit Dash - 1.0.0-Beta")
clock = pygame.time.Clock()

# load transparent
transparentBg = pygame.image.load("assets/map/bg_transparent.png")
transparentBg = pygame.transform.scale(transparentBg, (windowW, windowH))

# color
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 234, 0)  