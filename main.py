import pygame
from pygame import mixer
import random
import os
from spritesheet import SpriteSheet
from enemy import Enemy
mixer.init()
pygame.init()

#========================================== SETTINGS =====================================================

#setting game window size (in pixels) (constant variables):
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


#create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#defining color scheme:
WHITE = (255, 255, 255)
RED = (225, 137, 125)
BLACK = (0, 0, 0)
SCORE_PANEL_COLOR = (126, 108, 142)

#Font
font_small = pygame.font.SysFont('Lucida Sans', 14)
font_big = pygame.font.SysFont('Lucida Sans', 20)

#function for outputting text to screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#load music and sounds
mixer.music.load('assets/music/cottagecore.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1, 0.0)
jump_sound = mixer.Sound('assets/music/jump.mp3')
jump_sound.set_volume(0.2)
death_sound = mixer.Sound('assets/music/beefmow.mp3')
death_sound.set_volume(0.2)

#game variables (how fast the player falls down):
GRAVITY = 1
MAX_PLATFORMS = 40
SCROLL_THRESHOLD = 200
scroll = 0
background_scroll = 0
game_over = False
score = 0
fade_counter = 0

     
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0


#======================================= INICIATING BACKGROUND STUFF ========================================================

#loading game images:
startBtn_img = pygame.image.load('assets/start.png').convert_alpha()
restartBtn_img = pygame.image.load('assets/restart.png').convert_alpha()

player_sprite = pygame.image.load('assets/cat.png').convert_alpha()
platform_sprite = pygame.image.load('assets/platform.png').convert_alpha()
bg_image = pygame.image.load('assets/background.png').convert_alpha()
raven_sprites = pygame.image.load('assets/raven.png').convert_alpha()
raven_sheet = SpriteSheet(raven_sprites)




def draw_panel():
    pygame.draw.rect(screen, SCORE_PANEL_COLOR, (0,0, SCREEN_WIDTH, 30) )
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('YOUR SCORE: ' + str(score), font_small, WHITE, 0, 0)
    


# to draw infinite scrolling background
def draw_background (background_scroll):
    #make background appear at a certain position
    screen.blit(bg_image, (0, 0 + background_scroll))
    screen.blit(bg_image, (0, -SCREEN_HEIGHT + background_scroll))



#======================================= BUTTON ========================================================
class Button():
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (200, 50))

        self.rect = pygame.Rect(0, 0, 200, 50)
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)
        return action

#======================================== PLAYER =====================================================
class Player():
    def __init__(self, x, y): #starting coordinates for the player
        self.image = pygame.transform.scale(player_sprite, (50, 50))
        self.width = 35
        self.height = 40
        
        self.rect = pygame.Rect(0, 0, self.width, self.height) #the rect will be used to sense collision
        self.rect.center = (x, y)
        
        self.velocity_y = 0 #player speed y axis
        self.velocity_x = 0 #player speed x axis
        
        #self.mask = None
        self.flip = False
    
    def move(self):
        # reset variables
        scroll = 0
        dx = 0
        dy = 0
        
        # process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
      
            
        #gravity
        self.velocity_y += GRAVITY
        dy += self.velocity_y
            
       
        # ensure player does not go off edge of screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right  
        
        
        #check collision with platforms = jumping
        for platform in platform_group:
            #y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            #check if the player has a platform above it
                if self.rect.bottom < platform.rect.centery:
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.velocity_y = -20
                        jump_sound.play()
                        
                    
 
        #check if player has reached the top of the screen
        if self.rect.top <= SCROLL_THRESHOLD:
            #only scroll if player is jumping up
            if self.velocity_y < 0:
                scroll = -dy    
        
        # update rect position
        self.rect.x += dx
        self.rect.y += dy + scroll
        # update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        return scroll
        
    def draw(self):
        screen.blit( pygame.transform.flip(self.image, self.flip, False ), ( self.rect.x - 12, self.rect.y - 5 ))
        #pygame.draw.rect(screen, WHITE, self.rect, 2 )



#========================================== PLATFORM =====================================================

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_sprite, (width, 10) )
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1,2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        #move side to side if the type is moving
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
            
            
        #change platform direction if it has hit a wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
            
        
        #update platform's vertical position
        self.rect.y += scroll
        
        #check if platform has gone off the screen and then delete it
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



#========================================== CREATING INSTANCES OF THE CLASSES =====================================================
#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, startBtn_img)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, restartBtn_img)

player = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )

#creasting sprite groups
platform_group = pygame.sprite.Group()
raven_group = pygame.sprite.Group()

#starting platform - stationary
platform = Platform(SCREEN_WIDTH // 2 - 50 , SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)


#========================================== GAME LOOP =====================================================
#without a loop the game screen wont stay on because the code is executed line by line and after the creation of the window the code ends and so does the program
main_menu = True
run = True
while run:
    clock.tick(FPS)
    
    #draw infinite scrolling backgroud otherwise we will reach the end of it at some point
    background_scroll += scroll
    if background_scroll >= SCREEN_HEIGHT:
        background_scroll = 0
    draw_background (background_scroll)
        
    if main_menu == True:
        if start_button.draw():
            main_menu = False
    
    else:
        if game_over == False: 
            scroll = player.move()
            
            #generate platforms
            if len(platform_group) < MAX_PLATFORMS:
                platform_width = random.randint(40, 100)
                platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
                platform_y = platform.rect.y - random.randint(80, 120)
                
                platform_type = random.randint(1, 2)
                if platform_type == 1 and score > 500:
                    platform_moving = True
                else:
                    platform_moving = False
                
                platform = Platform(platform_x, platform_y, platform_width, platform_moving)
                platform_group.add(platform)  
            #update platforms
            platform_group.update(scroll)
            
            
            #generate enemies
            if len(raven_group) == 0:
                raven = Enemy(SCREEN_WIDTH, 100, raven_sheet, 1.5 )
                raven_group.add(raven)
            
            #update enemies
            raven_group.update(scroll, SCREEN_WIDTH)
            
            #updating the score
            if scroll > 0:
                score += scroll
            
            #========================================== DRAWING =====================================================

            #draw line at previous highest score
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESHOLD), (SCREEN_WIDTH, score - high_score + SCROLL_THRESHOLD), 3 )
            draw_text('HIGHEST SCORE', font_small, WHITE, SCREEN_WIDTH - 150, score - high_score + SCROLL_THRESHOLD)
            
            #draw sprites:
            platform_group.draw(screen)
            raven_group.draw(screen)
            player.draw()     
            
            '''draw enemy rect
            for enemy in raven_group:
                pygame.draw.rect(screen , WHITE, raven.rect, 2 )'''
            
            #draw panel
            draw_panel()
            
            #========================================== FALLING =====================================================
            #check for game over
            #fall off
            if player.rect.top > SCREEN_HEIGHT:
                game_over = True
                death_sound.play()
            #collision with enemies
            if pygame.sprite.spritecollide(player, raven_group, False):
                if pygame.sprite.spritecollide(player, raven_group, False, pygame.sprite.collide_mask):
                    game_over = True
                    death_sound.play()
        
        
        #========================================== WHEN GAME OVER =====================================================
        else:
            if fade_counter < SCREEN_WIDTH:
                fade_counter += 5 
                for y in range(0, 6, 2):
                    pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, SCREEN_HEIGHT / 6 ))
                    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y+1)*100, SCREEN_WIDTH, SCREEN_HEIGHT/ 6 ))
            else:    
                draw_text('GAME OVER!', font_big, RED, 230, 200)
                draw_text('SCORE: ' + str(score), font_big, RED, 250, 250)
                draw_text('PRESS SPACE TO PLAY AGAIN', font_big, RED, 150, 300)
                #update highest score
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                
                key = pygame.key.get_pressed()
                if restart_button.draw() or key[pygame.K_SPACE]:
                    #reset variables
                    game_over = False
                    score = 0
                    scroll = 0
                    fade_counter = 0
                    
                    #reposition player
                    player.rect.center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )
                    #reset enemies
                    raven_group.empty
                    #reset platforms
                    platform_group.empty()
                    #create starting platform
                    platform = Platform(SCREEN_WIDTH // 2 - 50 , SCREEN_HEIGHT - 50, 100, False)
                    platform_group.add(platform)

                
#========================================== CREATING INSTANCES OF THE CLASSESEVENT HANDLER =====================================================
    # click 'X' to close game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #update highest score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            
            run = False
    
    #update display window
    pygame.display.update()
            

pygame.quit()