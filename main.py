import pygame

pygame.init()

#setting game window size (in pixels) (constant variables):
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#defining color scheme:
WHITE = (255,255,255)





#loading game images:
player_sprite = pygame.image.load('assets/cat.png').convert_alpha()
bg_image = pygame.image.load("assets/background.jpg").convert_alpha()


# class for the player:
class Player():
    def __init__(self, x, y): #starting coordinates for the player
        self.image = pygame.transform.scale(player_sprite, (50, 50))
        self.width = 35
        self.height = 40
        
        #self.rectangle = self.image.get_rect() ->the rectangle will be used to sense collision
        self.rectangle = pygame.Rect(0, 0, self.width, self.height) #the rectangle will be used to sense collision
        self.rectangle.center = (x, y)
        
    def draw(self):
        screen.blit(self.image, ( self.rectangle.x - 12, self.rectangle.y - 5 ))
        pygame.draw.rect(screen, WHITE, self.rectangle, 2 )


player = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150 )



#without a loop the game screen wont stay on because the code is executed line by line and after the creation of the window the code ends and so does the program
run = True
while run:
    #make background appear at a certain position
    screen.blit(bg_image, (0,0))
    
    #draw sprites:
    player.draw()
    
    
    #event handler - click 'X' to close game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    #update display window
    pygame.display.update()
            

pygame.quit()