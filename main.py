import pygame

pygame.init()

#setting game window size (in pixels) (constant variables):
SREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create the game window
screen = pygame.display.set_mode((SREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#loading images:
player_sprite = pygame.image.load('assets/')
bg_image = pygame.image.load("assets/background.jpg").convert_alpha()


#without a loop the game screen wont stay on because the code is executed line by line and after the creation of the window the code ends and so does the program
run = True
while run:
    #make background appear at a certain position
    screen.blit(bg_image, (0,0))
    
    
    #event handler - click 'X' to close game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    #update display window
    pygame.display.update()
            

pygame.quit()