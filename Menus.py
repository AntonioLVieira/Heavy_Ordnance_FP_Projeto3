# === Imported Libraries ===
import pygame
from pygame import *
pygame.init()
import inspect
import os

# === Check Directory ===
filename = inspect.getframeinfo(inspect.currentframe()).filename #<--- Finds the file name.
path = os.path.dirname(os.path.abspath(filename))                #<--- Finds the path to the file.

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

# === Font ===
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)

#Font and text
pygame.font.init()
Font = pygame.font.SysFont("Showcard Gothic", 30)
Font1 = pygame.font.SysFont("Showcard Gothic", 50)
text = Font1.render ("Heavy Ordnance", True, RED)
text1 = Font.render ("Start new Game" , True , WHITE)
text2 = Font.render ("Leaderboard", True, WHITE)
text3 = Font.render ("Quit", True, WHITE)

# === Menu Variables ===
current_menu = 0
numbers = "0123456789"
game_over = False

# === Colors ===
gold = (255, 215, 0)
silver = (192, 192, 192)
bronze = (205, 127, 50)
white = (255, 255, 255)

# === Menu Image Files ===
main_menu_img = pygame.image.load(path + "/assets/images/main_menu_placeholder.jpg")
leaderboard_menu_img = pygame.image.load(path + "/assets/images/leaderboard_placeholder.jpg")

image1 = pygame.image.load(path + "/assets/images/barco_pequeno.png")
image2 = pygame.image.load(path + "/assets/images/barco_semi_pequeno.png")
image5 = pygame.image.load(path + "/assets/images/barco_medio.png")
image6 = pygame.image.load(path + "/assets/images/barco_grande.png")
Default_size = (150, 150)
image3 = pygame.transform.scale(image1, Default_size)
image4 = pygame.transform.scale(image2, Default_size)

# === Button images ===
start_button_img = pygame.image.load(path + "/assets/images/button.png")
leaderboard_button_img = pygame.image.load(path + "/assets/images/leaderboard_button.png")
back_button_img = pygame.image.load(path + "/assets/images/back_button.png")

# === Button class === 
class button():# Taken from this tutorial ---> (https://www.youtube.com/watch?v=G8MYGDf_9ho&ab_channel=CodingWithRuss)
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw_button(self, display_surface):

        action = False
        mouse_pos = pygame.mouse.get_pos()                                                      #<--- Updates mouse position.

        if self.rect.collidepoint(mouse_pos):                                                   #<--- Detects if the mouse position is in a coordinate where, according to the button image rectangle, the cursor would be on top of the button.
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:                 #<--- Only detects left clicks.
                action = True                                                                   #<--- Informs that the action needs to be activated.
                self.clicked = True                                                             #<--- Informs that the button is being pressed.

        if pygame.mouse.get_pressed()[0] == False:                                              #<--- Detects if the player isn't left clicking.
            self.clicked = False                                                                #<--- Informs that the button is no longer being pressed.

        display_surface.blit(self.image, (self.rect.x, self.rect.y))                            #<--- Draws the button.
        return action                                                                           #<--- Informs the caller if the action needs to be done or not.

# === Buttons ===
start_button = button(230,150,start_button_img)
leaderboard_button = button(230,220,leaderboard_button_img)
exit_leaderboard_button = button(910,10,back_button_img)

# === Menu classes ===
class Menu():
    def __init__(self):
        self.main_menu_img = main_menu_img
        self.leaderboard_img = leaderboard_menu_img
        self.leaderboard = []
        self.state = True
    
    # === Organizing ===
    def get_leaderboard(self):
        leaderboard =  self.leaderboard
        scores = open(path + "/assets/scores.txt", 'r').readlines()                             #<--- Opens the file where the scores information is stored and gets all the lines of text

        for line in scores:                                                                     #<--- Goes through each line in the text file.
            nickname = line[0] + line[1] + line[2] + line[3]                                    #<--- Gets the first 3 characters in the line and stores it as the current nickname.
            score = ""                                                                          #<--- Empty string variable that will later be used to store the current player's score.

            for character in line:                                                              #<--- Goes through each line in the line.
                if character in numbers:                                                        #<--- Detects if the character is a number.
                    score += character                                                          #<--- Adds that charcter to the score variable.

            current_player = nickname + score                                                   #<--- Joins the nickname withe the score for ease of ccess to these informations.

            if len(leaderboard) < 1:                                                            #<--- Detects if there are less than 1 player in the leaderboard.
                leaderboard.append(current_player)                                              #<--- Adds the current player to the leaderboard.

            else:                                                                               #<--- Detects if there are more than 1 player in the leaderboard.
                turn = 0                                                                        #<--- Variable used to track the amount of turns it takes to find a player with a higher score than the current one.

                for player in leaderboard:                                                      #<--- Goes through each player in the leaderboard.
                    other_player_score = ""                                                     #<--- Empty string variable that will later be used to store the OTHER player's score.

                    for character in player:                                                    #<--- Goes through each line in the current comparing player's line.
                        if character in numbers:                                                #<--- Detects if the character is a number.
                            other_player_score += character                                     #<--- Adds that charcter to the other player's score variable.

                    if current_player not in leaderboard:                                       #<--- Checks if the current player isn't already on the leaderboard.
                        if int(score) == int(other_player_score):                               #<--- Checks if the scores are equal.
                            leaderboard.insert(leaderboard.index(player) + 1,current_player)    #<--- Adds the current player to the leaderboard in the position after the other player

                        elif int(score) > int(other_player_score):                              #<--- Checks if the current player score is greater than the other player's.
                            leaderboard.insert(leaderboard.index(player),current_player)        #<--- Adds the current player to the leaderboard in the other player's position.

                        elif turn == (len(leaderboard) - 1):                                    #<--- Checks if the amount of turns is equal to the leaderboard's lenght.
                            leaderboard.append(current_player)                                  #<--- Adds the current player to the last position in the leaderboard
                            turn = 0                                                            #<--- Resets the "turn" variable.

                        else:
                            turn += 1                                                           #<--- Adds 1 turn.
            
            self.leaderboard = leaderboard                                                      #<--- Updates the leaderboard information.

    def draw_leaderboard(self, display_surface):
        leaderboard = self.leaderboard

        x = 260
        y = 80

        for player in leaderboard:                                                              #<--- Goes through each player in the leaderboard.
            nickname = player[0] + player[1] + player[2] + player[3]                            #<--- Gets the first 3 characters in the current player's line and stores it as the current nickname.
            score = ""                                                                          #<--- Empty string variable that will later be used to store the current player's score.

            for character in player:                                                            #<--- Goes through each line in the current player's line.
                if character in numbers:                                                        #<--- Detects if the character is a number.
                    score += character                                                          #<--- Adds that charcter to the score variable.
            if leaderboard.index(player) < 10:
                if leaderboard.index(player) == 0:                                                  #<--- Checks if the current player is in the first place.

                    player_nickname = font.render("#" + str(leaderboard.index(player) + 1) + " " + nickname, True, gold)
                    player_score = font.render(score, True, gold)

                    nick_rect = player_nickname.get_rect()
                    score_rect = player_score.get_rect()

                    nick_rect.topleft = (x,y)
                    score_rect.topright = (x + 429,y)

                    display_surface.blit(player_nickname,nick_rect)
                    display_surface.blit(player_score, score_rect)

                elif leaderboard.index(player) == 1:                                                  #<--- Checks if the current player is in the second place.

                    player_nickname = font.render("#" + str(leaderboard.index(player) + 1) + " " + nickname, True, silver)
                    player_score = font.render(score, True, silver)

                    nick_rect = player_nickname.get_rect()
                    score_rect = player_score.get_rect()

                    nick_rect.topleft = (x,y)
                    score_rect.topright = (x + 429,y)

                    display_surface.blit(player_nickname,nick_rect)
                    display_surface.blit(player_score, score_rect)

                elif leaderboard.index(player) == 2:                                                  #<--- Checks if the current player is in the third place.

                    player_nickname = font.render("#" + str(leaderboard.index(player) + 1) + " " + nickname, True, bronze)
                    player_score = font.render(score, True, bronze)

                    nick_rect = player_nickname.get_rect()
                    score_rect = player_score.get_rect()

                    nick_rect.topleft = (x,y)
                    score_rect.topright = (x + 429,y)

                    display_surface.blit(player_nickname,nick_rect)
                    display_surface.blit(player_score, score_rect)

                else:

                    player_nickname = font.render("#" + str(leaderboard.index(player) + 1) + " " + nickname, True, white,)
                    player_score = font.render(score, True, white)

                    nick_rect = player_nickname.get_rect()
                    score_rect = player_score.get_rect()

                    nick_rect.topleft = (x,y)
                    score_rect.topright = (x + 429,y)

                    display_surface.blit(player_nickname,nick_rect)
                    display_surface.blit(player_score, score_rect)

                y += 29                                                                                 #<--- Moves the next text 50 units down.

class Main_Menu(Menu):
    def draw_menu(self, displaysurface):
        global current_menu
        global game_over 

        width = displaysurface.get_width()
        height = displaysurface.get_height()    

        game_over = False
        mouse = pygame.mouse.get_pos() 

        if current_menu == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("working")
                    if width - 705 <= mouse[0] <= width - 445 and height - 255 <= mouse[1] <= height - 215:
                        print("working")
                        return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if width - 705 <= mouse[0] <= width - 480 and height - 195 <= mouse[1] <= height - 155:
                        current_menu = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if width - 705 <= mouse[0] <= width - 615 and height - 135 <= mouse[1] <= height - 95:
                        pygame.quit()
        
            displaysurface.fill((DARK_BLUE))

            displaysurface.blit(image1, (650, 170))
            displaysurface.blit(image2, (75, 25))
            displaysurface.blit(image5, (720, 90))
            displaysurface.blit(image6, (60, 170))



            if width - 705 <= mouse[0] <= width - 445 and height - 255 <= mouse[1] <= height - 215:
                pygame.draw.rect(displaysurface,BLACK,[width - 705, height - 255, 260, 40])
            if width - 705 <= mouse[0] <= width - 480 and height - 195 <= mouse[1] <= height - 155:
                pygame.draw.rect(displaysurface,BLACK,[width - 705, height - 195, 225, 40])
            if width - 705 <= mouse[0] <= width - 615 and height - 135 <= mouse[1] <= height - 95:
                pygame.draw.rect(displaysurface,BLACK,[width - 705, height - 135, 90, 40])
            
                    
            
            displaysurface.blit(text, (width - 750, height - 330))
            displaysurface.blit(text1 , (width - 700, height - 250))
            displaysurface.blit(text2, (width - 700, height - 190))
            displaysurface.blit(text3, (width - 700, height - 130))
            
            

        
            return True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            displaysurface.blit(self.leaderboard_img, (0,0))
            super().get_leaderboard()
            super().draw_leaderboard(displaysurface)

            if exit_leaderboard_button.draw_button(displaysurface) == True:
                current_menu = 0

    


