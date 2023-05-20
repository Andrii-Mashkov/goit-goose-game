# import modules
import random
import time
import os
import pygame

# import variable from modules
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

# initialization module
pygame.init()

# announcement colors constants
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE  = 0, 0, 255

# announcement sizes and font constants
WIDTH  = 800                                     # define constant of width screen
HEIGHT = 600                                     # define constant of heigh screen
FONT_SIZE = 28                                   # define constant of font size
FONT = pygame.font.SysFont('verdana', FONT_SIZE) # define constant of font

# announcement time constants - Frames Per Second (FPS) - waiting (ms)
FPS = pygame.time.Clock()                        # define constant

# working with window
screen = WIDTH, HEIGHT                           # define variable of resolution
my_display = pygame.display.set_mode(screen)     # create a graphic window by passing its resolution and getting an object of type Surface

# background picture
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))    # load & scale background picture
bg1_x = 0                                                                            # define variable left of background_1
bg2_x = bg.get_width()                                                               # define variable left of background_2
bg_move = 2                                                                          # define variable speed of background

# define variable and constants of player
PLAYER_SIZE = 91, 38            # 182, 76                   # define constant of player size (width, heigh)
player_speed = 3                                            # speed of the player
player = pygame.image.load('player.png').convert_alpha()    # load & convert player picture
player = pygame.transform.scale(player, (PLAYER_SIZE))      # scaling player picture
player_rect = player.get_rect()                             # class in pygame, that allow you to manage the placement of surfaces. Rect(left, top, width, height)
player_rect = player_rect.move([50, round(HEIGHT/3,0)])     # define first position of player 
player_lives = 1                                            # lives number of the player
IMAGE_PATH = "Goose"                                        # folder path constant
PLAYER_IMAGES = os.listdir(IMAGE_PATH)                      # read all file names from folder in collection
CHANGE_IMAGE  = pygame.USEREVENT +1                         # create event constant
pygame.time.set_timer(CHANGE_IMAGE, 200)                    # period change (animation) player in ms
imege_index = 0                                             # index of picture for animation

# define the direction of the player
player_move_down  = [ 0,  player_speed]
player_move_up    = [ 0, -player_speed]
player_move_right = [ player_speed,  0]
player_move_left  = [-player_speed,  0]

# define colection for enemies
enemies = []

# create enemy
def e_create():
  # define variable and constants of enemy
  ENEMY_SIZE  = 102, 31         # 205, 72                                  # define constant of enemy size (width, heigh)
  ENEMY_MAX_SPEED = 4                                                      # max speed of the enemy
  enemy = pygame.image.load('enemy.png').convert_alpha()                   # load & convert enemy picture
  enemy = pygame.transform.scale(enemy, (ENEMY_SIZE))                      # scaling enemy picture
  enemy_rect = pygame.Rect(WIDTH-ENEMY_SIZE[0], random.randint(0, round(HEIGHT*2/3, 0)), *ENEMY_SIZE)  # class in pygame, that allow you to manage the placement of surfaces
  enemy_move = [random.randint(-ENEMY_MAX_SPEED, -1), 0]                   # define speed of enemy
  return [enemy, enemy_rect, enemy_move]

ENEMY_CREATE = pygame.USEREVENT +2           # create event constant
pygame.time.set_timer(ENEMY_CREATE, 2000)    # period create enemy in ms

# define colection for bonuses
bonuses = []

# create bonus
def b_create():
  # define variable and constants of bonus
  BONUS_SIZE  = 60, 70        # 179, 208                                   # define variable of bonus size (width, heigh)
  BONUS_MAX_SPEED = 3                                                      # max speed of the enemy
  bonus = pygame.image.load('bonus.png').convert_alpha()                   # load & convert bonus picture
  bonus = pygame.transform.scale(bonus, (BONUS_SIZE))                      # scaling enemy picture
  bonus_rect = pygame.Rect(random.randint(round(WIDTH/3, 0), WIDTH-BONUS_SIZE[0]), 0, *BONUS_SIZE)     # class in pygame, that allow you to manage the placement of surfaces
  bonus_move = [0, random.randint(1, BONUS_MAX_SPEED)]                     # define speed of bonus
  return [bonus, bonus_rect, bonus_move]

BONUS_CREATE = pygame.USEREVENT +3           # create event constant
pygame.time.set_timer(BONUS_CREATE, 3000)    # period create bonus in ms

# placed number of lives on the screen
def font_blit():
  if   is_colliderect == -1 : font_color = RED 
  elif is_colliderect ==  1 : font_color = GREEN 
  else                      : font_color = BLACK
  my_display.blit(FONT.render(str(player_lives), True, font_color), (player_rect.left, player_rect.top-FONT_SIZE-2))
  return  

# begin game
is_game = True                                                 # define variable of cycle
while is_game:                                                 # start of cycle
  
  FPS.tick(60)                                                 # cycle speed, no more than frames per second 
  
  for event in pygame.event.get():                             # pygame.event.get() - function that takes events that have occurred from the queue
    if event.type == QUIT         : is_game = False               # if event type = QUIT - exit from cycle
    if event.type == ENEMY_CREATE : enemies.append(e_create())    # if event type = ENEMY_CREATE - create enemy
    if event.type == BONUS_CREATE : bonuses.append(b_create())    # if event type = BONUS_CREATE - create bonus
    if event.type == CHANGE_IMAGE : 
      player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[imege_index])).convert_alpha()  # load & convert player picture
      player = pygame.transform.scale(player, (PLAYER_SIZE))      # scaling player picture
      imege_index += 1                                            # index +1
      if imege_index >= len(PLAYER_IMAGES): imege_index = 0       # if index > max then index to to min

  bg1_x -= bg_move                                                # calculate left of background_1
  bg2_x -= bg_move                                                # calculate left of background_2
  if bg2_x == 0 :
    bg1_x = 0                                                     # define variable left of background_1
    bg2_x = bg.get_width()                                        # define variable left of background_2

  my_display.blit(bg, (bg1_x, 0))                                 # placed background_1 on the screen
  my_display.blit(bg, (bg2_x, 0))                                 # placed background_2 on the screen

  keys = pygame.key.get_pressed()                                 # get the index of the pressed key
  # take and recalculate (shift) the current player coordinates
  if keys[K_DOWN]  and player_rect.bottom < HEIGHT : player_rect = player_rect.move(player_move_down)
  if keys[K_UP]    and player_rect.top    > 0      : player_rect = player_rect.move(player_move_up)
  if keys[K_LEFT]  and player_rect.left   > 0      : player_rect = player_rect.move(player_move_left)
  if keys[K_RIGHT] and player_rect.right  < WIDTH  : player_rect = player_rect.move(player_move_right)
  
  my_display.blit(player, player_rect)              # placed the player on the screen

  # placed enemies on the screen
  is_colliderect = 0
  for enemy in enemies:
    enemy[1] = enemy[1].move(enemy[2])
    my_display.blit(enemy[0], enemy[1])             # placed the enemy on the screen
    if player_rect.colliderect(enemy[1]):           # if crossing player & enemy
      player_lives  -=  1                           # subtract 1 from number of lives
      is_colliderect = -1                           # define flag of colliderect with enemy
      enemies.pop(enemies.index(enemy))             # clear this enemy
  
  # placed bonuses on the screen
  for bonus in bonuses:
    bonus[1] = bonus[1].move(bonus[2])
    my_display.blit(bonus[0], bonus[1])             # placed the bonus on the screen
    if player_rect.colliderect(bonus[1]):           # if crossing player & enemy
      player_lives  +=  1                           # add 1 to number of lives
      is_colliderect =  1                           # define flag of colliderect with bonus
      bonuses.pop(bonuses.index(bonus))             # clear this bonus

  font_blit()                                       # placed the lives of player on the screen
  pygame.display.flip()                             # update the screen

  # clear bad enemies
  for enemy in enemies:
    if enemy[1].left < 0        : enemies.pop(enemies.index(enemy))
  
  # clear bad bonuses
  for bonus in bonuses:
    if bonus[1].bottom > HEIGHT : bonuses.pop(bonuses.index(bonus))
  
  # if colliderect was
  if is_colliderect != 0:
    time.sleep(0.5)           # Pause 0.5 seconds

  # if there are no more lives
  if player_lives < 1:
    is_game = False           # game over
    time.sleep(0.5)           # Pause 0.5 seconds

  #  end of cycle