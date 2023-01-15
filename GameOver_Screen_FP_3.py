import pygame, sys
import numpy as np
from pygame.locals import *
import os
import inspect

pygame.init()
res = (1000, 380)
Screen = pygame.display.set_mode((res))
width = Screen.get_width()
height = Screen.get_height()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
DARK_BLUE = (0, 0, 102)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (51, 153, 255)
GREY = (64, 64, 64)
LIGHT_GREY = (96, 96, 96)
DARK_GREY = (32, 32, 32)
RED = (100, 20, 20)
LIGHT_RED = (241, 86, 86)

v_pos = [50, 50]
v_direção = [1, 0]

# === Check Directory ===
filename = inspect.getframeinfo(inspect.currentframe()).filename    #<--- Finds the file name.
path = os.path.dirname(os.path.abspath(filename))                   #<--- Finds the path to the file.

image1 = pygame.image.load(path + "/assets/images/barco_pequeno.png")
image2 = pygame.image.load(path + "/assets/images/barco_semi_pequeno.png")
image5 = pygame.image.load(path + "/assets/images/barco_medio.png")
image6 = pygame.image.load(path + "/assets/images/barco_grande.png")
Default_size = (150, 150)
image3 = pygame.transform.scale(image1, Default_size)
image4 = pygame.transform.scale(image2, Default_size)

current_image = image3
        
def fill(color):
    Screen.fill(color)

#Game loop
running_game = False
start_screen = True

#Font and text
pygame.font.init()
Font = pygame.font.SysFont("Showcard Gothic", 30)
Font1 = pygame.font.SysFont("Showcard Gothic", 60)
text = Font1.render ("GAME OVER", True, RED)
text1 = Font.render ("Start new Game" , True , WHITE)
text2 = Font.render ("Leaderboard", True, WHITE)
text3 = Font.render ("Quit", True, WHITE)




while start_screen == True:
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
                    if width - 705 <= mouse[0] <= width - 445 and height - 255 <= mouse[1] <= height - 215:
                        start_screen = False
                        running_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
                    if width - 705 <= mouse[0] <= width - 480 and height - 195 <= mouse[1] <= height - 155:
                        start_screen = False
                        running_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
                    if width - 705 <= mouse[0] <= width - 615 and height - 135 <= mouse[1] <= height - 95:
                        pygame.quit()
                        sys.exit()
    
    fill((DARK_BLUE))

    mouse = pygame.mouse.get_pos() 

    if width - 705 <= mouse[0] <= width - 445 and height - 255 <= mouse[1] <= height - 215:
        pygame.draw.rect(Screen,BLACK,[width - 705, height - 255, 260, 40])
    if width - 705 <= mouse[0] <= width - 480 and height - 195 <= mouse[1] <= height - 155:
        pygame.draw.rect(Screen,BLACK,[width - 705, height - 195, 225, 40])
    if width - 705 <= mouse[0] <= width - 615 and height - 135 <= mouse[1] <= height - 95:
        pygame.draw.rect(Screen,BLACK,[width - 705, height - 135, 90, 40])
    
            
      
    Screen.blit(text, (width - 685, height - 300))
    #Screen.blit(text1 , (width - 700, height - 250))
    #Screen.blit(text2, (width - 700, height - 190))
    #Screen.blit(text3, (width - 700, height - 130))
      
    
    pygame.display.update()