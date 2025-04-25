import pygame
import sys
import random
from pygame.math import Vector2

class FROGCAT:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.dir = Vector2(1,0)
        self.new_longcat = False
        
        self.head_up = pygame.image.load('icons/frogcat_up.png').convert_alpha()
        self.head_down = pygame.image.load('icons/frogcat_down.png').convert_alpha()
        self.head_right = pygame.image.load('icons/frogcat_right.png').convert_alpha()
        self.head_left = pygame.image.load('icons/frogcat_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('icons/cat_up.png').convert_alpha()
        self.tail_down = self.tail_up
        self.tail_right = pygame.image.load('icons/cat_right.png').convert_alpha()
        self.tail_left = self.tail_right
        
        self.body_vertical = self.tail_up
        self.body_horizontal = self.tail_right
        
        self.body_tr = self.tail_up
        self.body_tl = pygame.image.load('icons/cat_tl.png').convert_alpha()
        self.body_br = pygame.image.load('icons/rainbow_br2.png').convert_alpha()
        self.body_bl = self.tail_right
          
        self.yummy_sound = pygame.mixer.Sound('sounds/yummy.wav')

    def draw_frogcat(self):
        self.update_head_icons()
        self.update_tail_icons()
        
        for index, block in enumerate(self.body):
            x_pstn = int(block.x * cell_measure)
            y_pstn = int(block.y * cell_measure)
            block_rect = pygame.Rect(x_pstn, y_pstn, cell_measure, cell_measure)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block   
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                
    def update_head_icons(self):
        head_change = self.body[1] - self.body[0]
        if head_change == Vector2(1,0):
            self.head = self.head_left
        elif head_change == Vector2(-1,0):
            self.head = self.head_right
        elif head_change == Vector2(0,1):
            self.head = self.head_up
        elif head_change == Vector2(0,-1):
            self.head = self.head_down
            
    def update_tail_icons(self):
        tail_change = self.body[-2] - self.body[-1]
        if tail_change == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_change == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_change == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_change == Vector2(0,-1):
            self.tail = self.tail_down
                
    def move_frogcat(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.dir)
        if not self.new_longcat:
            body_copy.pop()
        self.body = body_copy
        self.new_longcat = False

    def long_cat(self):
        self.new_longcat = True
        
    def play_yummy_sound(self):
        self.yummy_sound.play()
        
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.dir = Vector2(1,0)

class HEART:
    def __init__(self):
        self.randomheart()

    def draw_heart(self):
        heart_rect = pygame.Rect(self.pstn.x * cell_measure, self.pstn.y * cell_measure, cell_measure, cell_measure)
        screen.blit(heart, heart_rect)

    def randomheart(self):
        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pstn = pygame.math.Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.start_screen = True  
        self.game_active = False  
        self.frogcat = FROGCAT()
        self.heart = HEART()

    def update(self):
        if self.game_active:
            self.frogcat.move_frogcat()
            self.check_crossing()
            self.check_error()

    def draw_elems(self):
        self.frogcat.draw_frogcat()
        self.heart.draw_heart()
        self.draw_score()

    def draw_start_screen(self):
        font = pygame.font.Font('fonts/font.ttf', 70)
        bg_color = (255, 245, 238)
        line1_surface = font.render('press', True, (103,49,71))
        line2_surface = font.render('˚space˚', True, (103,49,71))
        line3_surface = font.render('to start', True, (103,49,71))
        line1_rect = line1_surface.get_rect(center=(cell_count * cell_measure / 2, cell_count * cell_measure / 2 - 60))
        line2_rect = line2_surface.get_rect(center=(cell_count * cell_measure / 2, cell_count * cell_measure / 2))
        line3_rect = line3_surface.get_rect(center=(cell_count * cell_measure / 2, cell_count * cell_measure / 2 + 60))
        bg_rect = pygame.Rect(line1_rect.left - 55, line1_rect.top - 10,
                          line1_rect.width + 115, line1_rect.height + line2_rect.height + line3_rect.height - 25)
        pygame.draw.rect(screen, bg_color, bg_rect)
        pygame.draw.rect(screen, (103,49,71), bg_rect, 10)
        screen.blit(line1_surface, line1_rect)
        screen.blit(line2_surface, line2_rect)
        screen.blit(line3_surface, line3_rect)

 
    def check_crossing(self):
        if self.heart.pstn == self.frogcat.body[0]:
            self.heart.randomheart()
            self.frogcat.long_cat()
            self.frogcat.play_yummy_sound()
            
        for block in self.frogcat.body[1:]:
            if block == self.heart.pstn:
                self.heart.randomheart()   

    def check_error(self):
        if not (0 <= self.frogcat.body[0].x < cell_count) or not (0 <= self.frogcat.body[0].y < cell_count):
            self.game_active = False
            pygame.mixer.music.stop() 
            pygame.mixer.music.load('sounds/game_over.mp3')
            pygame.mixer.music.play()
            
        for block in self.frogcat.body[1:]:
            if block == self.frogcat.body[0]:
                self.game_active = False
                pygame.mixer.music.stop() 
                pygame.mixer.music.load('sounds/game_over.mp3')
                pygame.mixer.music.play()

    def reset_game(self):
        self.frogcat.reset()
        self.game_active = True
        pygame.mixer.music.load('sounds/background_song.mp3')
        pygame.mixer.music.play(-1)

    def draw_game_over(self):
       font1 = pygame.font.Font('fonts/font.ttf', 70)
       font2 = pygame.font.Font('fonts/font.ttf', 30)
       game_over_surface = font1.render('Game Over', True, (103, 49, 71))
       restart_surface = font2.render('˚press space to restart˚', True, (103, 49, 71))
       game_over_rect = game_over_surface.get_rect()
       restart_rect = restart_surface.get_rect()
       game_over_rect.midtop = (cell_count * cell_measure / 2, cell_count * cell_measure / 4)
       restart_rect.midtop = (cell_count * cell_measure / 2, game_over_rect.bottom + 10)
       bg_rect = pygame.Rect(game_over_rect.left - 22, game_over_rect.top, 
                          max(game_over_rect.width, restart_rect.width) + 40, 
                          restart_rect.bottom - game_over_rect.top + 14) 
       pygame.draw.rect(screen, (255, 245, 238), bg_rect)
       screen.blit(game_over_surface, game_over_rect)
       screen.blit(restart_surface, restart_rect)
       pygame.draw.rect(screen, (103, 49, 71), bg_rect, 10)
       pygame.display.flip()


    def draw_score(self):
        score_text = str(len(self.frogcat.body) - 3)
        score_surface = frogcat_font.render(score_text,True,(103,49,71))
        score_x = int(cell_measure * cell_count - 60)
        score_y = int(cell_measure * cell_count - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        heart_rect = heart.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(heart_rect.left,heart_rect.top,heart_rect.width + score_rect.width + 6,heart_rect.height)
        pygame.draw.rect(screen,(255, 245, 238),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(heart,heart_rect)
        pygame.draw.rect(screen,(103,49,71),bg_rect,2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.mixer.music.load('sounds/background_song.mp3')
pygame.mixer.music.play(-1)

cell_measure = 34
cell_count = 17
screen = pygame.display.set_mode((cell_measure * cell_count, cell_measure * cell_count))
pygame.display.set_caption("Lovesick Frogcat")
clock = pygame.time.Clock()
heart = pygame.image.load('icons/heart.png').convert_alpha()
heart = pygame.transform.scale(heart, (cell_measure, cell_measure))
frogcat_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 160)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            if main_game.game_active:
                main_game.update()
        if event.type == pygame.KEYDOWN:
            if main_game.start_screen:
                if event.key == pygame.K_SPACE:
                    main_game.start_screen = False
                    main_game.game_active = True
                    pygame.mixer.music.load('sounds/background_song.mp3')
                    pygame.mixer.music.play(-1)
            elif main_game.game_active:
                if event.key == pygame.K_UP and main_game.frogcat.dir.y != 1:
                    main_game.frogcat.dir = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.frogcat.dir.y != -1:
                    main_game.frogcat.dir = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.frogcat.dir.x != 1:
                    main_game.frogcat.dir = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.frogcat.dir.x != -1:
                    main_game.frogcat.dir = Vector2(1, 0)
            else:
                if event.key == pygame.K_SPACE:
                    main_game.reset_game()
          
    screen.fill((243, 207, 198))
    if main_game.start_screen:
        main_game.draw_start_screen()
    elif main_game.game_active:
        main_game.draw_elems()
    else:
        main_game.draw_game_over()
    pygame.display.update()
    clock.tick(70)
