import pygame
import random

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
SCROLL_THRESHOLD = 200
scroll = 0
background_scroll = 0
GRAVITY = 1
MAX_PLATFORMS = 10

#defining color scheme:
WHITE = (255, 255, 255)


#loading game images:
player_sprite = pygame.image.load('Desktop/PygamePlatformer/assets/cat.png').convert_alpha()
platform_sprite = pygame.image.load('Desktop/PygamePlatformer/assets/platform.png').convert_alpha()
bg_image = pygame.image.load("Desktop/PygamePlatformer/assets/background.jpg").convert_alpha()

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
                    

        
        #check collision with ground
        if self.rectangle.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.velocity_y = -20 # how hard the player bounces off the ground
           
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
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_sprite, (width, 10) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        #update platform's vertical position
        self.rect.y += scroll
        
        #check if platform has gone off the screen and then delete it
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



#instances:
player = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )

#temporary platforms
platform_group = pygame.sprite.Group()


platform = Platform(SCREEN_WIDTH // 2 - 50 , SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)



#without a loop the game screen wont stay on because the code is executed line by line and after the creation of the window the code ends and so does the program
run = True
while run:
    clock.tick(FPS)
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
        
        platform = Platform(platform_x, platform_y, platform_width)
        platform_group.add(platform)
    
    
    #update platforms
    platform_group.update(scroll)
    
    #draw sprites:
    platform_group.draw(screen)
    player.draw()
    
    #draw temporary scroll threshold
    #pygame.draw.line(screen, WHITE, (0, SCROLL_THRESHOLD), (SCREEN_WIDTH, SCROLL_THRESHOLD))
    
    
    #event handler - click 'X' to close game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    #update display window
    pygame.display.update()
            

pygame.quit()