import pygame
import random
import math
from config  import * 

class Spritesheet:
    def __init__(self,file) :
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width , height])
        sprite.blit(self.sheet, (0,0) , (x , y , width , height) )
        sprite.set_colorkey(WHITE)
        return sprite
        


class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        self.game = game
        self.player_layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x_change = 0
        self.y_change = 0
        self.facing =  'Idle'
        self.Last_Move = "Down"
        

        self.x = (SCREEN_WIDTH-(PLAYER_SIZE_X * MUTIPIE_SIZE))/2
        self.y = (SCREEN_HEIGHT-(PLAYER_SIZE_Y * MUTIPIE_SIZE))/2
        self.width = TILESIZE
        self.height = TILESIZE
        self.count_Move = 0
        self.count_Move_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(160,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (TILESIZE * MUTIPIE_SIZE , TILESIZE * MUTIPIE_SIZE ))
        
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.Hitbox = Hitbox(game,self.x+(8*MUTIPIE_SIZE),self.y+(18*MUTIPIE_SIZE),16*MUTIPIE_SIZE,10*MUTIPIE_SIZE)
        
    def update(self):
        self.movement()
        self.update_animation()
        
        old_x = self.rect.x
        old_y = self.rect.y
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.Hitbox.Move(self.x_change ,self.y_change)
        
        self.x_change = 0
        self.y_change = 0
        
        self.facing = "Idle"



    def update_animation(self):
        self.anime_walk()
        self.anime_stop()
        
        

    def anime_walk(self):
        move_anime = {"Down" : 32 , "Up" : 224 , "Right" : 160 , "Left": 96}
        if self.facing != "Idle" :
            self.image = self.game.character_spritesheet.get_sprite(self.count_Move * TILESIZE,move_anime[self.facing] , self.width,self.height)
            self.count_Move_loop += 1
                    
            if self.Last_Move == "Down":
                if self.count_Move == 5:
                    self.count_Move = 0  

            else:
                if self.count_Move == 6:
                    self.count_Move = 0
            
            # set speed animetion
            if self.count_Move_loop >= 6:
                self.count_Move_loop = 0
                self.count_Move += 1
    
    def anime_stop(self):
        if self.facing == "Idle" and self.Last_Move != "":
            
            if self.Last_Move == "Up":
                self.image = self.game.character_spritesheet.get_sprite(0,192,self.width,self.height)

            elif self.Last_Move == "Right":
                self.image = self.game.character_spritesheet.get_sprite(160,128,self.width,self.height)
            
            elif self.Last_Move == "Left":
                self.image = self.game.character_spritesheet.get_sprite(160,64,self.width,self.height)
                
            elif self.Last_Move == "Down" :
                self.image = self.game.character_spritesheet.get_sprite(160,0,self.width,self.height)
            self.count_Move_loop = 0
            self.count_Move = 0
            self.Last_Move = ""

        
        self.image = pygame.transform.scale(self.image, (TILESIZE * MUTIPIE_SIZE , TILESIZE * MUTIPIE_SIZE ))

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'Left'
            self.Last_Move = "Left"
        
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'Right'
            self.Last_Move = "Right"
        
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'Up'
            self.Last_Move = "Up"
        
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'Down'
            self.Last_Move = "Down"

class Map(pygame.sprite.Sprite):
    def __init__(self,game):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = self.game.Map_image.get_sprite(0,0,MAP_SIZE_X,MAP_SIZE_Y)
        self.image = pygame.transform.scale(self.image, (MAP_SIZE_X * MUTIPIE_SIZE , MAP_SIZE_Y * MUTIPIE_SIZE ))
        self.rect = self.image.get_rect()

        self.rect.x = MAP_START_POSITION_X
        self.rect.y = MAP_START_POSITION_Y
        
    def hit(self,data):
        # if self.wall.colliderect(data):
        #     return True
        return False

class Hitbox(pygame.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = 0

        self.groups = self.game.all_sprites , self.game.wall
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = pygame.Surface([self.width , self.height])
        self.image.set_colorkey(BLACK)
        self.hitbox = pygame.Rect(0, 0, width , height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(self.image, RED, self.hitbox, 2)

    def Move(self,x,y):
        self.rect.x += x
        self.rect.y += y

        
        

class Wall(pygame.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = 0

        self.groups = self.game.all_sprites , self.game.wall
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = pygame.Surface([self.width , self.height])
        self.image.set_colorkey(BLACK)
        self.hitbox = pygame.Rect(0, 0, width , height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(self.image, RED, self.hitbox, 2)
        
class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.npc
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.facing = ''
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.target_pos = (x, y)  
        
    def update(self):
        self.move_to_target()
    
    def move_to_target(self):
        if self.target_pos != None:
            self.facing = 'Moving'
            if self.rect.x < self.target_pos[0]:
                self.rect.x += self.speed
            elif self.rect.x > self.target_pos[0]:
                self.rect.x -= self.speed

            if self.rect.y < self.target_pos[1]:
                self.rect.y += PLAYER_SPEED
            elif self.rect.y > self.target_pos[1]:
                self.rect.y -= self.speed

        # ตรวจสอบว่าถึงจุดเป้าหมายแล้วหรือยัง
        if (self.rect.x, self.rect.y) == self.target_pos:
            self.target_pos = None  # เมื่อถึงเป้าหมายแล้ว
            self.facing = "Idel"

        
