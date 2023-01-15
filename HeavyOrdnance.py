# === Imported Libraries ===
import os
import inspect
import pygame
from pygame import *
from pygame import mixer

# === Initiate Libraries ===
pygame.init()
mixer.init()

# === Imported Classes ===
from Cannon import cannon
from Menus import Main_Menu

# === Font ===
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)

# === Check Directory ===
filename = inspect.getframeinfo(inspect.currentframe()).filename    #<--- Finds the file name.
path = os.path.dirname(os.path.abspath(filename))                   #<--- Finds the path to the file.

# === Display Surface Settings ===
screen = pygame.display.set_mode((1000,380))                        #<--- Creates the display surface.
pygame.display.set_caption("Heavy Ordnance")                        #<--- Sets the window name.

# === Game Loop Variables ===
runing_game = False
menus = True

# === Audio Settings ===
pygame.mixer.music.load(path + "/assets/audio/music/Finding Nemo Videogame OST 05 - Mask Chase.mp3")
mixer.music.set_volume(0.1)

# === Game Images ===
bg = pygame.image.load(path + "/assets/images/land.png")
loaded_cannon_sprite = pygame.image.load(path + "/assets/images/loaded_canon.png")
cannon_sprite = pygame.image.load(path + "/assets/images/canon.png")

game_over_img = pygame.image.load(path + "/assets/images/game_over_placeholder.jpg")

#=== Clock Object ===
clock = pygame.time.Clock()

# === Game loop ===
while True:
    player = cannon(screen,loaded_cannon_sprite, cannon_sprite)

    while menus:
        if Main_Menu().draw_menu(screen) == False:
            menus = False
            running_game = True

        pygame.display.update()                 #<--- Updates the display surface.


    pygame.mixer.music.play(-1)                 #<--- Plays the music on loop.


    while running_game:
        if player.return_if_GameOver():
            score = player.scored()
            running_game = False
            GameOver = True
        clock.tick(60)                          #<--- Limits the Framerate to 60 frames per second.
        mouse_pos = pygame.mouse.get_pos()      #<--- Updates mouse position.
        screen.fill((0,30,90))                   #<--- Fills the screen.
                
        for event in pygame.event.get():        #<--- Detects every event happening.
            if event.type == QUIT:              #<--- Checks for a specific event type, QUIT, wich occurs when the user presses the red cross at the upper right corner of the window.
                pygame.QUIT()                   #<--- Exits the program.

        player.draw_cannon(mouse_pos)
        player.shoot()                          #<--- Detects if the player is shooting.
                #<--- Draws the cannon.
        
        screen.blit(bg,(0,0))                   #<--- Draws the background
        player.draw_enemies()

        pygame.display.update()                 #<--- Updates the display surface.
        

    pygame.mixer.music.stop()                   #<--- Plays the music on loop.

    player_nick = ""

    while GameOver:
        screen.blit(game_over_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_nick = player_nick[:-1]# get text input from 0 to -1 i.e. end.

                elif len(player_nick) == 3 and event.key == pygame.K_RETURN:
                    open(path + "/assets/scores.txt", 'a').write(("\n" + player_nick.upper() + " " + str(score)))
                    menus = True
                    GameOver = False

            
                elif len(player_nick) < 3 and event.key != pygame.K_SPACE:
                    player_nick += event.unicode

                    
        phrase = font.render("Choose a nickname and check the leaderboard", True, (0, 0, 0))
        nick = font.render(player_nick.upper(), True, (0, 255, 255))

        screen.blit(phrase,(275, 100))    
        screen.blit(nick, (475, 190))

        pygame.display.update()
