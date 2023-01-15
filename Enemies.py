import pygame
from pygame import *
import inspect
import os
import math
import time
import random
from pygame import mixer
mixer.init()

# === Check Directory ===
filename = inspect.getframeinfo(inspect.currentframe()).filename #<--Finds the file name.
path = os.path.dirname(os.path.abspath(filename))                #<--Finds the path to the file.

# === Audio ===
hit_sfx = pygame.mixer.Sound(path + "/assets/audio/sfx/boat exploding.mp3")

# === Images ===
barco_placeholder = pygame.image.load(path + "/assets/images/barco.png")
enemie_img_semi_pequeno = pygame.image.load(path + "/assets/images/barco_semi_pequeno.png")
enemie_img_pequeno = pygame.image.load(path + "/assets/images/barco_pequeno.png")
enemie_img_medio = pygame.image.load(path + "/assets/images/barco_medio.png")
enemie_img_grande = pygame.image.load(path + "/assets/images/barco_grande.png")
player_full_hp = pygame.image.load(path + "/assets/images/HP_bar_full.png") 
player_2_hp = pygame.image.load(path + "/assets/images/HP_bar_2.png") 
player_1_hp = pygame.image.load(path + "/assets/images/HP_bar_1.png") 
player_no_hp = pygame.image.load(path + "/assets/images/HP_bar_empty.png") 

spawn_time = 0
spawned = False

cooldown = 300
category = 1
destroyed = 0
speed = 1
last_category = 0

class Enemies():
    def __init__(self, display_surface):
        self.player_hp = 3
        self.display_surface = display_surface
        self.enemie_group = []
        self.hit = False  
        self.updated_speed = False
        self.points = 0
        self.mul = 1
        self.big_spawned = False

    def draw(self, bullet, bullet_dmg):
        global destroyed
        global speed

        self.hit = False
        if len(str(destroyed)) > 1:
            if str(destroyed)[len(str(destroyed)) - 1] == "0" and self.updated_speed == False:
                speed += 0.2
                self.mul += 1
                print("SPEEDING UP")
                self.updated_speed = True
            elif (str(destroyed) + " ")[len(str(destroyed)) - 1]  == "0":
                self.updated_speed = True
            else:
                self.updated_speed = False

        if self.player_hp == 3:
            self.display_surface.blit(player_full_hp, (900,25))
        elif self.player_hp == 2:
            self.display_surface.blit(player_2_hp, (900,25))
        elif self.player_hp == 1:
            self.display_surface.blit(player_1_hp, (900,25))
        else:
            self.display_surface.blit(player_no_hp, (900,25))

        if len(self.enemie_group) > 0 and len(self.enemie_group) < 4:
            for enemie in self.enemie_group:
                if enemie.category == 4:
                    self.big_spawned = True
                self.display_surface.blit(enemie.image, (enemie.x,enemie.y))

                if enemie.hitbox.colliderect(bullet) and self.hit == False:
                    print(str(enemie.hp) + " " + str(bullet_dmg))
                    self.hit = True
                    enemie.hp -= bullet_dmg
                    hit_sfx.play()
                    
                    if enemie.hp <= 0:
                        if enemie.category == 4:
                            self.big_spawned = False
                        self.points += enemie.points * self.mul
                        self.enemie_group.remove(enemie)
                        destroyed += 1
                if enemie.x > 120:
                    enemie.x -= enemie.speed
                    enemie.hitbox.x = enemie.x
                else:
                    self.enemie_group.remove(enemie)
                    destroyed += 1
                    self.player_hp -= 1
                    hit_sfx.play()

    def player_HP(self):
        if self.player_hp > 0:
            return False
        else:
            return True
    
    def got_hit(self):
        return self.hit

    def spawn_enemies(self):
        global spawn_time
        global spawned
        global cooldown
        global category
        global last_category

        self.current_time = pygame.time.get_ticks()
        # print(len(self.enemie_group))

        if self.current_time - spawn_time > cooldown and spawned == False:
            category = random.randrange(1,21)
            if category == 4 and self.big_spawned == False:
                category = 4
            else:
                category = random.randrange(1,4)

            
            if category == last_category:
                self.spawn_enemies()

            if len(self.enemie_group) < 3:
                last_category = category
                cooldown = random.randrange(2,5)
                cooldown *= 1000
                print(cooldown)
                spawned = True
                enemie = Enemie()
                self.enemie_group.append(enemie)
                spawn_time = self.current_time
                spawned = False

class Enemie(Enemies):
    def __init__(self):
        self.category = category
        self.speed = speed
        self.x = 1050
        if category == 4:
            self.image = enemie_img_grande
            self.points = 2
            self.y = 150
            self.speed *= 0.25
            self.hp = 8
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (self.category / 4), self.image.get_height() * (self.category / 4)))
        elif category == 3:
            self.image = enemie_img_medio
            self.points = 3
            self.y = 250
            self.speed *= 0.5
            self.hp = 3
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (self.category / 4), self.image.get_height() * (self.category / 4)))
        elif category == 2:
            self.image = enemie_img_semi_pequeno
            self.points = 4
            self.y = 280
            self.speed *= 0.75
            self.hp = 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (self.category / 4), self.image.get_height() * (self.category / 4)))
        else:
            self.image = enemie_img_pequeno
            self.points = 5
            self.y = 300
            self.hp = 1
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (self.category / 4), self.image.get_height() * (self.category / 4)))

        self.hitbox = self.image.get_rect()
        self.hitbox.x = self.x
        self.hitbox.y = self.y

        self.current_time = 0
        self.destroyed = 0 

    def Is_big_spawned(self):
        return self.big_spawned