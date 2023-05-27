import pygame
import random
import os
from spritesheet import SpriteSheet
from enemy import Enemy
pygame.init()

#setting game window size (in pixels) (constant variables):
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variables (how fast the player falls down):
GRAVITY = 1
MAX_PLATFORMS = 10
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

#defining color scheme:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_COLOR = (153, 217, 234)

#Font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#function for outputting text to screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))




#loading game images:
player_sprite = pygame.image.load('assets/cat.png').convert_alpha()
platform_sprite = pygame.image.load('assets/platform.png').convert_alpha()
bg_image = pygame.image.load('assets/background.jpg').convert_alpha()
raven_sprites = pygame.image.load('assets/raven.png').convert_alpha()
raven_sheet = SpriteSheet(raven_sprites)



def draw_panel():
    pygame.draw.rect(screen, PANEL_COLOR, (0,0, SCREEN_WIDTH, 30) )
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('YOUR SCORE: ' + str(score), font_small, WHITE, 0, 0)
    


# to draw infinite scrolling background
def draw_background (background_scroll):
    #make background appear at a certain position
    screen.blit(bg_image, (0, 0 + background_scroll))
    screen.blit(bg_image, (0, -600 + background_scroll))



# class for the player:
class Player():
    def __init__(self, x, y): #starting coordinates for the player
        self.image = pygame.transform.scale(player_sprite, (50, 50))
        self.width = 35
        self.height = 40
        
        #self.rectangle = self.image.get_rect() ->the rectangle will be used to sense collision
        self.rectangle = pygame.Rect(0, 0, self.width, self.height) #the rectangle will be used to sense collision
        self.rectangle.center = (x, y)
        
        self.velocity_y = 0
        self.flip = False
    
    def move(self):
        #reset variables
        scroll = 0
        dx = 0
        dy = 0
        
        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
            
        #gravity
        self.velocity_y += GRAVITY
        dy += self.velocity_y
        
        #ensure player does not go off edge of screen
        if self.rectangle.left + dx < 0:
            dx = -self.rectangle.left
        if self.rectangle.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rectangle.right  
        
        
        #check collision with platforms
        for platform in platform_group:
            #y direction
            if platform.rect.colliderect(self.rectangle.x, self.rectangle.y + dy, self.width, self.height):
            #check if the player has a platform above it
                if self.rectangle.bottom < platform.rect.centery:
                    if self.velocity_y > 0:
                        self.rectangle.bottom = platform.rect.top
                        dy = 0
                        self.velocity_y = -20
                    
 
        #check if player has reached the top of the screen
        if self.rectangle.top <= SCROLL_THRESHOLD:
            #only scroll if player is jumping up
            if self.velocity_y < 0:
                scroll = -dy    
        
        #update rectangle position
        self.rectangle.x += dx
        self.rectangle.y += dy + scroll
        
        return scroll
        
    def draw(self):
        screen.blit( pygame.transform.flip(self.image, self.flip, False ), ( self.rectangle.x - 12, self.rectangle.y - 5 ))
        pygame.draw.rect(screen, WHITE, self.rectangle, 2 )


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



#instances:
player = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )

#creasting sprite groups
platform_group = pygame.sprite.Group()
raven_group = pygame.sprite.Group()

#starting platform - stationary
platform = Platform(SCREEN_WIDTH // 2 - 50 , SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)

#without a loop the game screen wont stay on because the code is executed line by line and after the creation of the window the code ends and so does the program
run = True
while run:
    clock.tick(FPS)
    
    if game_over == False: 
        scroll = player.move()
        
        #draw infinite scrolling backgroud otherwise we will reach the end of it at some point
        background_scroll += scroll
        if background_scroll >= 600:
            background_scroll = 0
        draw_background (background_scroll)
        
        
        #generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            platform_width = random.randint(40, 60)
            platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
            platform_y = platform.rect.y - random.randint(80, 120)
            
            platform_type = random.randint(1, 2)
            if platform_type == 1 and score > 500:
                platform_moving = True
            else:
                platform_moving= False
            
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
        #draw line at previous highest score
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESHOLD), (SCREEN_WIDTH, score - high_score + SCROLL_THRESHOLD), 3 )
        draw_text('HIGHEST SCORE', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESHOLD)
        
        #draw sprites:
        platform_group.draw(screen)
        raven_group.draw(screen)
        player.draw()        
        #draw panel
        draw_panel()
        
        #check for game over
        if player.rectangle.top > SCREEN_HEIGHT:
            game_over = True
    
    
    else:
        
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5 
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, SCREEN_HEIGHT / 6 ))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y+1)*100, SCREEN_WIDTH, SCREEN_HEIGHT/ 6 ))
        else:    
            draw_text('GAME OVER!', font_big, WHITE, 130, 200)
            draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
            #update highest score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                
                #reposition player
                player.rectangle.center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )
                #reset enemies
                raven_group.empty
                #reset platforms
                platform_group.empty()
                #create starting platform
                platform = Platform(SCREEN_WIDTH // 2 - 50 , SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)

                
          
    #event handler - click 'X' to close game window
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