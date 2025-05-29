import pygame
import random
from settings import (
    obstacle_width, obstacle_height, game_speed,
    ground_height, ground_width, windowH,
    baseGroundSprites, obstacleSprites
)

class Obstacle(pygame.sprite.Sprite):
    "kelas untuk objek rintangan"

    def __init__(self, inverted, xpos, ysize, image_dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_dir).convert_alpha()
        self.image = pygame.transform.scale(self.image, (obstacle_width, obstacle_height))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = obstacle_height - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        "update posisi rintangan ke kiri"
        self.rect[0] -= game_speed

class Ground(pygame.sprite.Sprite):
    "kelas untuk objek tanah/ground"

    def __init__(self, xpos, choose_character):
        super().__init__()
        
        # memilih sprite tanah berdasarkan karakter ID
        char_id = int(choose_character.GetID()) -1 
        image_dir = baseGroundSprites[char_id]

        self.image = pygame.image.load(image_dir).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ground_width, ground_height))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = windowH - ground_height

    def update(self):
        "update posisi tanah ke kiri"
        self.rect[0] -= game_speed

def get_random_obstacle(xpos, chosen_character):
    "mengembalikan objek rintangan dengan posisi acak"
    MINIMUM_GAP = 500  # Increase minimum gap to 500px
    gap_size = random.randint(MINIMUM_GAP, MINIMUM_GAP + 100)  # Random gap 500-600px
    
    # Buat obstacle atas lebih pendek
    top_size = random.randint(30, 100)  # Decrease top obstacle size
    bottom_size = windowH - top_size - gap_size  # Bottom size will adjust automatically
    
    # get obstacle sprite based on the character ID
    char_id = int(chosen_character.GetID()) - 1
    image_dir = obstacleSprites[char_id]

    # create bottom and top obstacles
    bottom_obstacle = Obstacle(False, xpos, bottom_size, image_dir)
    top_obstacle = Obstacle(True, xpos, top_size, image_dir)

    return bottom_obstacle, top_obstacle