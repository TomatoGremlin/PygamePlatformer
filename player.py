import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, player_sprite


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
