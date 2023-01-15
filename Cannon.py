# === Imported Libraries ===
import pygame
from pygame import *
import inspect
import os
import math
from pygame import mixer
mixer.init()

from Enemies import Enemies

# === Check Directory ===
filename = inspect.getframeinfo(inspect.currentframe()).filename #<--Finds the file name.
path = os.path.dirname(os.path.abspath(filename))                #<--Finds the path to the file.

# === Audio ===
shoot_sfx = pygame.mixer.Sound(path + "/assets/audio/sfx/shooting.mp3")
reload_sfx = pygame.mixer.Sound(path + "/assets/audio/sfx/reload.mp3")

charge_1 = pygame.mixer.Sound(path + "/assets/audio/sfx/charge_1.mp3")
charge_2 = pygame.mixer.Sound(path + "/assets/audio/sfx/charge_2.mp3")
charge_3 = pygame.mixer.Sound(path + "/assets/audio/sfx/charge_3.mp3")

# === Sprites ===
bullet_img = pygame.image.load(path + "/assets/images/bullet.png")

# === Font ===
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 16)

class Bullet():
    def __init__(self, angle, display_surface, speed, dmg):
        self.angle = angle
        self.img = bullet_img

        self.rotated_img = pygame.transform.rotate(self.img, math.degrees(self.angle))
        self.rotated_img.set_colorkey((255,255,255))

        self.x = 50 - (self.rotated_img.get_width() / 2)
        self.y = 145 - (self.rotated_img.get_height() / 2)
        
        self.rect = self.rotated_img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.speed = speed
        self.display_surface = display_surface

        self.dmg = dmg

    def draw(self, coords):
        self.rotated_img = pygame.transform.rotate(self.img, math.degrees(self.angle))
        self.rotated_img.set_colorkey((255,255,255))
        self.display_surface.blit(self.rotated_img, (coords))


class cannon():
    def __init__(self, display_surface,loaded_sprite, empty_sprite):
        self.display_surface = display_surface
        self.enemies = Enemies(display_surface)

        self.bullet_speed = 10

        self.score = 0

        gui_scale = 0.5

        self.scaled_bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_width() * gui_scale, bullet_img.get_height() * gui_scale))
        self.rotated_bullet_img = pygame.transform.rotate(self.scaled_bullet_img, 90)
        self.rotated_bullet_img.set_colorkey((255,255,255))

        self.angle = 0

        self.loaded_sprite = loaded_sprite
        self.empty_sprite = empty_sprite

        self.og_empty_sprite = self.empty_sprite
        self.og_loaded_sprite = self.loaded_sprite

        self.x = 50
        self.y = 145

        self.sprite = self.loaded_sprite
        self.bullet_group = []
        self.ammo = 2
        self.fired = False

        self.current_time = 0
        self.shot_time = 0
        self.points_time = 0

        self.time_points = 0

        self.bullet_hitbox = self.sprite.get_rect()
        self.bullet_dmg = 0

        self.charged1 = False
        self.charged2 = False
        self.charged3 = False

    def draw_cannon(self, mouse_pos):
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.points_time > 1000:
            self.points_time = self.current_time
            self.time_points += 1

        if len(self.bullet_group) < 2 and self.current_time - self.shot_time > 1000:
            self.current_sprite_og = self.og_loaded_sprite
        else:
            self.current_sprite_og = self.og_empty_sprite
        
        x_distance = mouse_pos[0] - self.x - (self.sprite.get_width() / 2)
        y_distance = -(mouse_pos[1] - self.y - (self.sprite.get_height() / 2))

        self.angle = (math.atan2(y_distance, x_distance))


        self.sprite = pygame.transform.rotate(self.current_sprite_og, math.degrees(self.angle))
        
        self.sprite.set_colorkey((255,255,255))  
        # pygame.draw.line(self.display_surface, (255,255,255), (self.x, self.y), (mouse_pos[0],mouse_pos[1]))
        
        if len(self.bullet_group) > 0:
                for bullet in self.bullet_group:
                    if bullet.x > 1015 or bullet.x < -15 or bullet.y < -50 or bullet.y > 395:
                        self.bullet_group.remove(bullet)
                        self.ammo += 1
                        reload_sfx.play()
                        self.bullet_hitbox = self.sprite.get_rect()
                    else:
                        bullet.x += (math.cos(bullet.angle) * bullet.speed) 
                        bullet.y += -(math.sin(bullet.angle) * bullet.speed) 
                        bullet.rect.x = bullet.x
                        bullet.rect.y = bullet.y
                        Bullet(bullet.angle, self.display_surface, bullet.speed, bullet.dmg).draw((bullet.x,bullet.y))

                        self.bullet_hitbox = bullet.rect
                        self.bullet_dmg = bullet.dmg

                        if self.enemies.got_hit() == True:
                            self.bullet_hitbox = self.sprite.get_rect()
                            self.bullet_group.remove(bullet)
                            self.ammo += 1
                            reload_sfx.play()
                        
        
        self.display_surface.blit(self.sprite,(self.x - (self.sprite.get_width() / 2), self.y - (self.sprite.get_height() / 2)))

        self.score = self.enemies.points + self.time_points
        score = font.render("Score:  " + str(self.score), True, (255,255,255))
        score_rect = score.get_rect()
        score_rect.topright = (995,5) # align to right to 150px

        self.display_surface.blit(score,score_rect)

        if self.ammo == 2:
            self.display_surface.blit(self.rotated_bullet_img,(980,60))
            self.display_surface.blit(self.rotated_bullet_img,(960,60))
        elif self.ammo == 1:
            self.display_surface.blit(self.rotated_bullet_img,(980,60))

        return score

    def shoot(self):
        if pygame.mouse.get_pressed()[0] == True and self.current_time - self.shot_time > 1000:
            if self.fired == False and len(self.bullet_group) < 2:
                if self.charged1 == False and self.bullet_speed >= 12.5:
                    self.charged1 = True
                    charge_1.play()
                if self.charged2 == False and self.bullet_speed >= 15:
                    self.charged2 = True
                    charge_2.play()
                if self.charged3 == False and self.bullet_speed >= 17.7:
                    self.charged3 = True
                    charge_3.play()
                self.bullet_speed += 0.1
                if self.bullet_speed >= 20:
                    self.shot_time = self.current_time
                    dmg = 4
                    shoot_sfx.play()
                    bullet = Bullet(self.angle, self.display_surface, int(self.bullet_speed), dmg)
                    self.bullet_group.append(bullet)
                    self.fired = True
                    self.ammo -= 1
                    self.bullet_speed = 10
                    self.charged1 = False
                    self.charged2 = False
                    self.charged3 = False

        elif pygame.mouse.get_pressed()[0] == False and self.current_time - self.shot_time > 1000 and self.bullet_speed > 10:
            self.shot_time = self.current_time
            dmg = int(int(self.bullet_speed - 5) / 4)
            shoot_sfx.play()
            bullet = Bullet(self.angle, self.display_surface, int(self.bullet_speed), dmg)
            self.bullet_group.append(bullet)
            self.fired = True
            self.ammo -= 1
            self.bullet_speed = 10
            self.charged1 = False
            self.charged2 = False
            self.charged3 = False

        else:
            self.fired = False

    def draw_enemies(self):
        self.enemies.spawn_enemies()
        self.enemies.draw(self.bullet_hitbox, self.bullet_dmg)

    def return_if_GameOver(self):
        return self.enemies.player_HP()

    def scored(self):
        return self.score