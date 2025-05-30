import pygame
from pygame import mixer
from abc import ABC, abstractmethod
from settings import (
    windowH, gravity, character_speed, skillactive, ground_height
)

class Character(pygame.sprite.Sprite, ABC):
    "kelas abstrak karakter yang akan digunakan dalam game"

    def __init__(self):
        super().__init__()
        self.score = 0
        self.speed = character_speed
        self.passed_obs = set()

    def reset_char(self):
        "reset karakter ke posisi awal permainan"
        self.score = 0
        self.speed = character_speed
        self.passed_obs = set()
        self.rect.x = 30
        self.rect.y = int (windowH / 2)
        self.current_img = 0
        self.image = self.images[self.current_img]

    def fall_move(self):
        "gerakan jatuh karakter"
        self.speed += gravity
        self.rect.y += self.speed
        if self.rect.bottom > windowH - ground_height:
            self.rect.bottom = windowH - ground_height
            self.speed = character_speed
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = character_speed
        self.current_img = (self.current_img + 1) % 3
        self.image = self.images[self.current_img]

    def up_move(self):
        "gerakan naik karakter"
        self.speed = -character_speed

    def get_score(self, obstacle_object, ghost_object):
        "menghitung skor karakter setelah melewati obstacle"
        if not obstacle_object or not ghost_object:
            return
        
        for obs in obstacle_object:
            if obs.rect.y > 100:
                #jika karakter melewati obstacle dan belum menghitungnya
                if (ghost_object.sprites()[0].rect.centerx > obs.rect.right and
                    id(obs) not in self.passed_obs):
                    self.score += 1
                    self.passed_obs.add(id(obs))
                    break

    def reset_passed_obs(self):
        "reset obstacle yang sudah dilewati"
        self.passed_obs = set()

    @abstractmethod
    def cast_skill(self):
        "menggunakan skill spesial karakter"
        pass

    @abstractmethod
    def drownHP(self):
        "mengurangi HP karakter"
        pass

    @abstractmethod
    def getHP(self):
        "mengembalikan HP karakter"
        pass

    @abstractmethod
    def GetID(self):
        "mendapatkan ID karakter"
        pass

class char1(Character):
    "kelas karakter 1 - Gotoku - Healing Ability"

    def __init__(self):
        super().__init__()
        self.__hp = 3
        self.__idObject = "001"
        self.skill = False
        self.__healing_done = False
        self.images = [
            pygame.image.load("assets/actor/gotoku/gotoku_up.png").convert_alpha(),
            pygame.image.load("assets/actor/gotoku/gotoku_normal.png").convert_alpha(),
            pygame.image.load("assets/actor/gotoku/gotoku_down.png").convert_alpha()
        ]
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = int (windowH / 2)

    def reset_char(self):
        "reset karakter ke posisi awal permainan"
        super().reset_char()
        self.__hp = 3
        self.skill = False
        self.__healing_done = False

    def cast_skill(self, obstacle_objects = None, ghost_object = None):
        "healing skill, mengembalikan HP karakter ketika mendapat 10 score"
        if self.__idObject != "001":
            return
    
    # Cek kondisi untuk aktivasi skill
        if (self.score % 10 == 0 and 
        self.__hp < 3 and 
        self.score > 0 and 
        not self.__healing_done and 
        ghost_object and 
        obstacle_objects and 
        len(obstacle_objects.sprites()) > 0):
        
        # Cek posisi karakter terhadap obstacle
            if (ghost_object.sprites()[0].rect.left > obstacle_objects.sprites()[0].rect.left
            and ghost_object.sprites()[0].rect.right < obstacle_objects.sprites()[0].rect.right):
                self.__hp += 1
                self.__healing_done = True
                self.skill = True  # Menandakan skill aktif
                self.sound = mixer.Sound(skillactive[0])
                self.sound.play()
    
    # Reset healing ketika score bukan kelipatan 10
        elif self.score % 10 != 0:
             self.__healing_done = False
             self.skill = False

    def drownHP(self):
        "mengurangi HP karakter"
        self.__hp -= 1

    def getHP(self):
        "mengembalikan HP karakter"
        return self.__hp
    
    def GetID(self):
        "mendapatkan ID karakter"
        return self.__idObject
    
    def update_score(self):
        "mengupdate skor karakter"
        self.score += 1

class char2(Character):
    "kelas karakter 2 - Onre - Invicible Ability"

    def __init__(self):
        super().__init__()
        self.__hp = 3
        self.__idObject = "002"
        self.skill = False
        self.__ghost_mode = False
        self.__frame_counter = 0
        self.images = [
            pygame.image.load("assets/actor/onre/onre_up.png").convert_alpha(),
            pygame.image.load("assets/actor/onre/onre_normal.png").convert_alpha(),
            pygame.image.load("assets/actor/onre/onre_down.png").convert_alpha()
        ]
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = int (windowH / 2)

    def reset_char(self):
        "reset karakter ke posisi awal permainan"
        super().reset_char()
        self.__hp = 3
        self.skill = False
        self.__ghost_mode = False
        self.__frame_counter = 0

    def cast_skill(self, obstacle_objects = None, ghost_object = None):
        "Ghost Mode, Dapat menembus rintangan selama 3 detik"
        if self.__idObject != "002":
            return
        
        # aktif ketika score kelipatan 10
        if self.score % 10 == 0 and self.score > 0 and not self.__ghost_mode:
            self.__ghost_mode = True
            self.skill = True
            self.__frame_counter = 90 # 3 detik skill aktif
            self.sound = mixer.Sound(skillactive[1])
            self.sound.play()
            # membuat character transparan untuk menandakan skill aktif
            for i in range(len(self.images)):
                self.images[i].set_alpha(128)
            self.image = self.images[self.current_img]
            print("Onre Ghost Mode Activ at score {self.score}")

        #menngembalikan transparansi karakter
        if self.__ghost_mode:
            self.__frame_counter -= 1
            if self.__frame_counter <= 0:
                self.__ghost_mode = False
                self.skill = False
                for i in range(len(self.images)):
                    self.images[i].set_alpha(255)
                self.image = self.images[self.current_img]
                print("Onre Ghost Mode Deactiv at score {self.score}")

    def drownHP(self):
        "mengurangi HP karakter, tetapi tidak mengurangi HP jika dalam mode ghost"
        if not self.__ghost_mode:
            self.__hp -= 1
            return True
        return False #tidak mengurangi HP jika dalam mode ghost

    def getHP(self):
        "mengembalikan HP karakter"
        return self.__hp
    
    def GetID(self):
        "mendapatkan ID karakter"
        return self.__idObject
    
    def is_ghost_mode(self):
        "mengembalikan status ghost mode"
        return self.__ghost_mode
    
    def update_score(self):
        "mengupdate skor karakter"
        self.score += 1
    
class char3(Character):
    "kelas karakter 3 - Yurei - Double Score Ability"

    def __init__(self):
        super().__init__()
        self.__hp = 3
        self.__idObject = "003"
        self.skill = False
        self.__double_score = False
        self.images = [
            pygame.image.load("assets/actor/yurei/yurei_up.png").convert_alpha(),
            pygame.image.load("assets/actor/yurei/yurei_normal.png").convert_alpha(),
            pygame.image.load("assets/actor/yurei/yurei_down.png").convert_alpha()
        ]
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = int (windowH / 2)
        self.__frame_counter = 0

    def reset_char(self):
        "reset karakter ke posisi awal permainan"
        super().reset_char()
        self.__hp = 3
        self.skill = False
        self.__double_score = False
        self.__frame_counter = 0

    def cast_skill(self, obstacle_objects = None, ghost_object = None):
        "double score skill, memberikan x2 score karakter selama 3 detik"
        if self.__idObject != "003":
            return
        
        # aktif ketika score kelipatan 10
        if self.score % 10 == 0 and self.score > 0 and not self.__double_score:
            self.__double_score = True
            self.skill = True
            self.__frame_counter = 90

            for i in range(len(self.images)):
                self.images[i].set_alpha(90)
            self.image = self.images[self.current_img]
            self.sound = mixer.Sound(skillactive[2])
            self.sound.play()
            self.score += 1

        #nonaktifkan skill setelah 3 detik
        elif self.__double_score:
            self.__frame_counter -= 1
            if self.__frame_counter <= 0:
                self.__double_score = False
                self.skill = False
        
        for i in range(len(self.images)):
            self.images[i].set_alpha(255)
            self.image = self.images[self.current_img]
                        
    def drownHP(self):
        "mengurangi HP karakter"
        self.__hp -= 1

    def getHP(self):
        "mengembalikan HP karakter"
        return self.__hp
    
    def GetID(self):
        "mendapatkan ID karakter"
        return self.__idObject

    def update_score(self):
        if self.__double_score:
            self.score += 2
        else:
            self.score += 1