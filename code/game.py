import pygame
import random
from pygame import mixer
from pygame.locals import *

from settings import (
    screen, clock, FPS, windowH, windowW, bgGameSprites,
    ground_width, transparentBg, bgm, tap, die, tapButton,
    skillactive, bgmStategame, gameInteruptScreen, menuSprites,
    charDescription, gameStartBtn, yellow, hpSprites, gameover_font, character_speed
)
from characters import char1, char2, char3
from objects import Ground, get_random_obstacle
from utils import show_score, load_highscore, change_highscore, is_off_screen, show_text

class Game:
    "main class untuk game state dan loop"

    def __init__(self):
        #inisialisasi sprite
        self.ghost_objects = pygame.sprite.Group()
        self.ground_objects = pygame.sprite.Group()
        self.obstacle_objects = None

        #inisialisasi karakter 
        self.gotoku = None
        self.onre = None
        self.yurei = None
        self.reset_all_characters() #memanggil fungsi reset karakter

        #variabel game state
        self.isgamerun = True
        self.isgamepause = False
        self.isfromdie = False
        self.gamestate = "menu game"
        self.after_collide = False
        self.after_collide_interval = 4
        self.isfrompause = False

        #sound effect
        self.sfxbutton = mixer.Sound(tapButton)
        self.sfxcharacter = [
            mixer.Sound(skillactive[0]),
            mixer.Sound(skillactive[1]),
            mixer.Sound(skillactive[2])
        ]

        #backgorund music
        mixer.music.load(bgm)
        mixer.music.play(-1)

        #select character
        self.charselected = None
        self.ischarchoose = False

    def reset_all_characters(self):
        "reset semua karakter ke posisi awal"
        self.ghost_objects.empty()

        #buat instace karakter baru
        self.gotoku = char1()
        self.onre = char2()
        self.yurei = char3()

        #reset karakter
        self.charselected = None
        self.ischarchoose = False

    def run(self):
        "main game loop"
        while self.isgamerun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = "netral state"
                    return
            if self.gamestate == "game over":
                self.game_over()
            elif self.gamestate == "menu game":
                self.menu_game()
            elif self.gamestate == "choose character":
                self.choose_character()
            elif self.gamestate == "play game":
                self.play_game()
            elif self.gamestate == "game pause":
                self.pause_game()
            elif self.gamestate == "netral state":
                break
                
    def setup_bg(self):
        "setup background dan ground untuk screen menu"
        self.bgmenugame = pygame.image.load(bgGameSprites[random.randint(0,2)])
        self.bgmenugame = pygame.transform.scale(self.bgmenugame, (windowW, windowH))

        ground_menu_choise = [self.gotoku, self.onre, self.yurei]
        self.groundmenugame = ground_menu_choise[random.randint(0,2)]

        self.ground_objects.empty()
        for i in range(2):
            ground = Ground(ground_width * i, self.groundmenugame)
            self.ground_objects.add(ground)

    def menu_game(self):
        "menu utama game"
        self.setup_bg()

        while self.gamestate == "menu game":
            screen.blit(self.bgmenugame, (0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = pygame.image.load(menuSprites[0])
            menu_rect = menu_text.get_rect(center=(windowW / 2, 100))

            btn_play = pygame.image.load(menuSprites[3])
            btn_play_rect = btn_play.get_rect(center=(windowW / 2, 300))
            btn_quit = pygame.image.load(menuSprites[5])
            btn_quit_rect = btn_quit.get_rect(center=(windowW / 2, 370))

            #update ground
            if is_off_screen(self.ground_objects.sprites()[0]):
                self.ground_objects.remove(self.ground_objects.sprites()[0])
                new_ground = Ground(ground_width - 1, self.groundmenugame)
                self.ground_objects.add(new_ground)

            self.ground_objects.update()
            self.ground_objects.draw(screen)

            screen.blit(menu_text, menu_rect)
            screen.blit(btn_play, btn_play_rect)
            screen.blit(btn_quit, btn_quit_rect)

            #button effect
            if (menu_mouse_pos[0] in range(btn_play_rect.left, btn_play_rect.right) and
                menu_mouse_pos[1] in range(btn_play_rect.top, btn_play_rect.bottom)):
                btn_play = pygame.image.load(menuSprites[4])
                screen.blit(btn_play, btn_play_rect)
            
            if (menu_mouse_pos[0] in range(btn_quit_rect.left, btn_quit_rect.right) and
                menu_mouse_pos[1] in range(btn_quit_rect.top, btn_quit_rect.bottom)):
                btn_quit = pygame.image.load(menuSprites[6])
                screen.blit(btn_quit, btn_quit_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = "netral state"
                    self.isgamerun = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (menu_mouse_pos[0] in range(btn_play_rect.left, btn_play_rect.right) and
                        menu_mouse_pos[1] in range(btn_play_rect.top, btn_play_rect.bottom)):
                        self.reset_all_characters()
                        self.gamestate = "choose character"

                        self.sfxbutton.play()
                        return

                    if (menu_mouse_pos[0] in range(btn_quit_rect.left, btn_quit_rect.right) and
                        menu_mouse_pos[1] in range(btn_quit_rect.top, btn_quit_rect.bottom)):
                        self.gamestate = "netral state"
                        self.isgamerun = False

            pygame.display.update()
            clock.tick(FPS)
        
    def choose_character(self):
        
        "menu untuk memilih karakter"
        # reset karakter ketika masuk ke menu ini
        if self.isfromdie:
            self.reset_all_characters()
            mixer.music.load(bgm)
            mixer.music.play(-1)
            self.isfromdie = False

        self.setup_bg()

        while self.gamestate == "choose character":
            clock.tick(FPS)
            screen.blit(self.bgmenugame, (0, 0))

            select_mouse_pos = pygame.mouse.get_pos()

            startbtn = pygame.image.load(gameStartBtn)
            startbtn = pygame.transform.scale(startbtn, (100, 75))
            startbtn_rect = startbtn.get_rect(center=(windowW / 2, (windowH / 2 - 50) + 300))

            #memuat popup select character
            try:
                select_text = pygame.image.load("assets/menu/select_character.png")
            except (pygame.error, FileNotFoundError):
                select_text = pygame.image.load(menuSprites[0])

            select_rect = select_text.get_rect(center=(windowW / 2, 100))

            #character
            btn_gotoku = pygame.image.load("assets/actor/gotoku/gotoku_normal.png")
            btn_gotoku = pygame.transform.scale(btn_gotoku, (150, 150))
            btn_gotoku_rect = btn_gotoku.get_rect(center=(300, windowH / 2 - 100))
            btn_onre = pygame.image.load("assets/actor/onre/onre_normal.png")
            btn_onre = pygame.transform.scale(btn_onre, (150, 150))
            btn_onre_rect = btn_onre.get_rect(center=(windowW / 2, windowH / 2 - 100))
            btn_yurei = pygame.image.load("assets/actor/yurei/yurei_normal.png")
            btn_yurei = pygame.transform.scale(btn_yurei, (150, 150))
            btn_yurei_rect = btn_yurei.get_rect(center=(1000, windowH / 2 - 100))

            btn_exit = pygame.image.load(menuSprites[5])
            btn_exit = pygame.transform.scale(btn_exit, (100, 35))
            btn_exit_rect = btn_exit.get_rect(center=(60, 30))

            screen.blit(select_text, select_rect)
            screen.blit(btn_gotoku, btn_gotoku_rect)
            screen.blit(btn_onre, btn_onre_rect)
            screen.blit(btn_yurei, btn_yurei_rect)
            screen.blit(btn_exit, btn_exit_rect)

            #button hover
            if (select_mouse_pos[0] in range(btn_exit_rect.left, btn_exit_rect.right) and
                select_mouse_pos[1] in range(btn_exit_rect.top, btn_exit_rect.bottom)):
                btn_exit_hover = pygame.image.load(menuSprites[6])
                btn_exit_hover = pygame.transform.scale(btn_exit_hover, (100, 35))
                screen.blit(btn_exit_hover, btn_exit_rect)

            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = "netral state"
                    self.isgamerun = False

                #keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.sfxbutton.play()
                        self.gamestate = "menu game"
                        self.reset_all_characters()
                        break
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #back button
                    if (select_mouse_pos[0] in range (btn_exit_rect.left, btn_exit_rect.right) and
                        select_mouse_pos[1] in range (btn_exit_rect.top, btn_exit_rect.bottom)):
                        self.sfxbutton.play()
                        self.gamestate = "menu game"
                        self.reset_all_characters()
                        break

                    #gotoku selection
                    if (select_mouse_pos[0] in range(btn_gotoku_rect.left, btn_gotoku_rect.right) and
                        select_mouse_pos[1] in range(btn_gotoku_rect.top, btn_gotoku_rect.bottom)):
                        if not self.ischarchoose or self.charselected != self.gotoku:
                            try :
                                self.sfxcharacter[0].play()
                                self.ghost_objects.empty()
                                #membuat instance baru
                                self.gotoku = char1()
                                self.charselected = self.gotoku
                                self.ischarchoose = True
                                self.setup_game_assets()
                            except Exception as e:
                                print(f"Error selecting character: {e}")
                    
                    #onre selection
                    if (select_mouse_pos[0] in range(btn_onre_rect.left, btn_onre_rect.right) and
                        select_mouse_pos[1] in range(btn_onre_rect.top, btn_onre_rect.bottom)):
                        if not self.ischarchoose or self.charselected != self.onre:                        
                            try:
                                self.sfxcharacter[1].play()
                                self.ghost_objects.empty()
                                #membuat instance baru
                                self.onre = char2()
                                self.charselected = self.onre

                                self.ischarchoose = True
                                self.setup_game_assets()
                            except Exception as e:
                                print(f"Error selecting character: {e}")
                    
                    #yurei selection
                    if (select_mouse_pos[0] in range(btn_yurei_rect.left, btn_yurei_rect.right) and
                        select_mouse_pos[1] in range(btn_yurei_rect.top, btn_yurei_rect.bottom)):
                        if not self.ischarchoose or self.charselected != self.yurei:
                            try:
                                self.sfxcharacter[2].play()
                                #menghapus karakter sebelumnya
                                self.ghost_objects.empty()
                                #membuat instance baru
                                self.yurei = char3()
                                self.charselected = self.yurei
                                print(f"select character with id: {self.charselected.GetID()}")
                                self.ischarchoose = True
                                self.setup_game_assets()
                            except Exception as e:
                                print(f"Error selecting character: {e}")
                    
                    #start game button
                    if (select_mouse_pos[0] in range (startbtn_rect.left, startbtn_rect.right) and
                        select_mouse_pos[1] in range (startbtn_rect.top, startbtn_rect.bottom)):
                        if self.ischarchoose and self.charselected:
                            self.sfxbutton.play()
                            self.setup_game_assets()
                            self.gamestate = "play game"
                            return

            #deskripsi char dan start button ketika dipilih
            if self.ischarchoose:
                deskripsiGhost = pygame.image.load(charDescription[int(self.charselected.GetID()) - 1])
                deskripsiGhost = pygame.transform.scale(deskripsiGhost, (375, 250))
                deskripsiGhost_rect = deskripsiGhost.get_rect(center=(windowW / 2, (windowH / 2 - 50) + 150))
                screen.blit(deskripsiGhost, deskripsiGhost_rect)

          
                screen.blit(startbtn, startbtn_rect)
                
            pygame.display.update()

    def setup_game_assets(self):
        "setup base asset pemilihan karakter"
        #set background berdasarkan karakter
                
        char_id = int(self.charselected.GetID()) - 1
        bg_image = pygame.image.load(bgGameSprites[char_id])
        bg_scaled = pygame.transform.scale(bg_image, (windowW, windowH))
        self.bggame = bg_scaled
        self.bgmenugame = bg_scaled
        
        self.charselected.rect.x = 35
        self.charselected.rect.y = int (windowH / 2)
        self.charselected.speed = character_speed
        self.ghost_objects.add(self.charselected)
        self.charselected.reset_passed_obs()

        self.ground_objects.empty()
        for i in range(2):
            ground = Ground(ground_width * i, self.charselected)
            self.ground_objects.add(ground)

        self.obstacle_objects = pygame.sprite.Group()
        first_obstacle = get_random_obstacle(windowW + 400, self.charselected)
        second_obstacle = get_random_obstacle(windowW + 550, self.charselected)
    
        self.obstacle_objects.add(first_obstacle[0])
        self.obstacle_objects.add(first_obstacle[1])
        self.obstacle_objects.add(second_obstacle[0])
        self.obstacle_objects.add(second_obstacle[1])

    def play_game(self):
        """play game state handler"""
        if not self.charselected:
            print("tidak ada karakter yang dipilih")
            return
        if not self.ischarchoose:
            print("no character selected")
            self.gamestate = "menu game"
            return
        if self.obstacle_objects is None:
            print("obstacle objects not initialized")
            self.setup_game_assets()
        
        if self.isfrompause:
            self.isfrompause = False

        else:
            mixer.music.stop()
            char_id = int(self.charselected.GetID()) - 1
            mixer.music.load(bgmStategame[char_id])
            mixer.music.play(-1)

        while self.gamestate == "play game":
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gamestate = "netral state"
                    self.isgamerun = False
                    return 
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        self.charselected.up_move()
                        tap_sound = mixer.Sound(tap)
                        tap_sound.play()
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        mixer.music.pause()
                        self.gamestate = "game pause"
                        return
                    elif event.key == pygame.K_m:
                        mixer.music.stop()
                        self.reset_all_characters()
                        self.gamestate = "menu game"
                        return
                    elif event.key == pygame.K_r:
                        mixer.music.stop()
                        self.reset_all_characters()
                        self.gamestate = "choose character"
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.charselected.up_move()
                    tap_sound = mixer.Sound(tap)
                    tap_sound.play()

            if self.charselected.getHP() == 3:
                hpImg = pygame.image.load(hpSprites[2])
                hpImg = pygame.transform.scale(hpImg, (47, 20))
            elif self.charselected.getHP() == 2:
                hpImg = pygame.image.load(hpSprites[1])
                hpImg = pygame.transform.scale(hpImg, (33, 20))
            else:
                hpImg = pygame.image.load(hpSprites[0])
                hpImg = pygame.transform.scale(hpImg, (20, 20))

            self.charselected.fall_move()

            screen.blit(self.bggame, (0, 0))
            screen.blit(hpImg, (0, 5))

            #update ground
            if is_off_screen(self.ground_objects.sprites()[0]):
                self.ground_objects.remove(self.ground_objects.sprites()[0])
                new_ground = Ground(ground_width - 20, self.charselected)
                self.ground_objects.add(new_ground)

            if is_off_screen(self.obstacle_objects.sprites()[0]):
                self.charselected.update_score()
                old_obs = self.obstacle_objects.sprites()[0:2]
                self.obstacle_objects.remove(old_obs)
                last_obstacle_x = self.obstacle_objects.sprites()[-1].rect[0]
                new_obs = get_random_obstacle(last_obstacle_x + 700, self.charselected)
                self.obstacle_objects.add(new_obs[0])
                self.obstacle_objects.add(new_obs[1])
            
            self.ground_objects.update()
            self.obstacle_objects.update()

            self.ghost_objects.draw(screen)
            self.ground_objects.draw(screen)
            self.obstacle_objects.draw(screen)

            self.charselected.cast_skill(self.obstacle_objects, self.ghost_objects)

            
            if self.ground_objects.sprites() and is_off_screen(self.ground_objects.sprites()[0]):
                self.ground_objects.remove(self.ground_objects.sprites()[0])
                new_ground = Ground(ground_width - 20, self.charselected)
                self.ground_objects.add(new_ground)
                
            show_score(str(self.charselected.score), yellow, int(windowW / 2 + 20) - 30, 20)
            show_text("P or ESC for Pause", 10, (255, 255, 255), 10, windowH - 70)
            show_text("R for Character Select", 10, (255, 255, 255), 10, windowH - 55) 
            show_text("M for Main Menu", 10, (255, 255, 255), 10, windowH - 40)

            pygame.display.update()

            if pygame.sprite.groupcollide(self.ghost_objects, self.ground_objects, False, False, pygame.sprite.collide_mask):
                if self.charselected.getHP() <= 0:
                    die_sound = mixer.Sound(die)
                    die_sound.play()
                    self.gamestate = "game over"
                    return

                self.charselected.drownHP()
                self.charselected.rect.x = 35
                self.charselected.rect.y = int(windowH / 2) - 20
                self.charselected.speed = character_speed
                continue 

            if pygame.sprite.groupcollide(self.ghost_objects,self.obstacle_objects, False, False, pygame.sprite.collide_mask):
                if not hasattr(self.charselected, '_is_collide') or not self.charselected._is_collide:
                    self.charselected.drownHP()
                    self.charselected._is_collide = True

                if self.charselected.getHP() <= 0:
                    die_sound = mixer.Sound(die)
                    die_sound.play()
                    self.gamestate = "game over"
                    return
                continue        
            else:
                if hasattr(self.charselected, '_is_collide'):
                    self.charselected._is_collide = False        

    def pause_game(self):
        """Pause game state handler"""
        isPauseRunOnce = True
        
        while self.gamestate == "game pause":
            pause_mouse_pos = pygame.mouse.get_pos()

            btn_continue = pygame.image.load("assets/menu/conti.png") #
            btn_continue = pygame.transform.scale(btn_continue, (200, 50))
            btn_continue_rect = btn_continue.get_rect(center=(windowW / 2, windowH / 2 ))

            btn_character_menu = pygame.image.load("assets/menu/select_character.png")#
            btn_character_menu = pygame.transform.scale(btn_character_menu, (200, 50))
            btn_character_menu_rect = btn_character_menu.get_rect(center=(windowW / 2, windowH / 2 + 70))

            btn_main_menu = pygame.image.load("assets/menu/main_menu.png")#
            btn_main_menu = pygame.transform.scale(btn_main_menu, (200, 50))
            btn_main_menu_rect = btn_main_menu.get_rect(center=(windowW / 2, windowH / 2 + 140))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = "netral state"
                    self.isgamerun = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_continue_rect.collidepoint(pause_mouse_pos):
                        mixer.music.unpause()
                        self.isfrompause = True
                        self.gamestate = "play game"
                        
                    elif btn_character_menu_rect.collidepoint(pause_mouse_pos):
                        mixer.music.stop()
                        self.reset_all_characters()
                        self.gamestate = "choose character"
        
                    elif btn_main_menu_rect.collidepoint(pause_mouse_pos):
                            mixer.music.stop()
                            self.reset_all_characters()
                            self.gamestate = "menu game"
                
            screen.blit(transparentBg, (0, 0))
            text_banner = pygame.image.load(gameInteruptScreen[0][0])
            text_banner_rect = text_banner.get_rect(center=(windowW / 2, 100))
            screen.blit(text_banner, text_banner_rect)
            screen.blit(btn_continue, btn_continue_rect)
            screen.blit(btn_character_menu, btn_character_menu_rect)
            screen.blit(btn_main_menu, btn_main_menu_rect)

            if btn_continue_rect.collidepoint(pause_mouse_pos):
                btn_continue_hover = pygame.image.load("assets/menu/conti_hov.png")
                btn_continue_hover = pygame.transform.scale(btn_continue_hover, (200, 50))
                screen.blit(btn_continue_hover, btn_continue_rect)

            if btn_character_menu_rect.collidepoint(pause_mouse_pos):
                btn_character_menu_hover = pygame.image.load("assets/menu/select_character_hover.png")
                btn_character_menu_hover = pygame.transform.scale(btn_character_menu_hover, (200, 50))
                screen.blit(btn_character_menu_hover, btn_character_menu_rect)   

            if btn_main_menu_rect.collidepoint(pause_mouse_pos):
                    btn_main_hover = pygame.image.load("assets/menu/main_menu_hover.png")
                    btn_main_hover = pygame.transform.scale(btn_main_hover, (200, 50))
                    screen.blit(btn_main_hover, btn_main_menu_rect)

            if isPauseRunOnce:
                pygame.display.update()
                isPauseRunOnce = False
                    
            pygame.display.update()
            clock.tick(30)

    def game_over(self):
        """Game over state handler"""
        mixer.music.stop()
        isGameOverScr = True


        while self.gamestate == "game over":
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gamestate = "netral state"
                    self.isgamerun = False
                if event.type == KEYDOWN:
                    if event.key == pygame.K_r:
                        self.gamestate = "choose character"
                        self.isfromdie = True

            screen.blit(transparentBg, (0, 0))
            text_banner = pygame.image.load("assets/menu/gameover_txt_bnnr.png")
            text_banner_rect = text_banner.get_rect(center=(windowW / 2, 200))
            screen.blit(text_banner, text_banner_rect)
            
            # cek highscore
            if self.charselected.score > int(load_highscore()):
                    show_text("New Highscore " + str(self.charselected.score), 30, (255, 255, 255),
                              windowW // 2 - 150, windowH // 2)
                    change_highscore(self.charselected.score)
            else:
                show_text("HighScore " + str(load_highscore()), 20, (255, 255, 255), windowW // 2 - 70, windowH // 4 + 150)
                show_text(f"Score Anda  {self.charselected.score}", 20, (255, 255, 255), windowW // 2 - 70, windowH // 4 + 150 + (20 + 10))
                show_text("Press R to Character Menu", 20, (255, 255, 255), windowW // 2 - 115, windowH // 4 + 150 + (30 + 10) + (10 + 10))
            
            if isGameOverScr:
                pygame.display.update()
                isGameOverScr = False
            
            clock.tick(5)