import pygame
import random
import math
from config  import *
from stack_system import Stack 

class Spritesheet:
    def __init__(self,file) :
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width , height])
        sprite.blit(self.sheet, (0,0) , (x , y , width , height) )
        sprite.set_colorkey(WHITE)
        return sprite

# ==============================================PLAYER===============================================================

class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x_change = 0
        self.y_change = 0
        self.facing =  'Idle'
        self.Last_Move = "Down"
        self.iscarry = False
        self.objcarry = None
        

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

        self.Hitbox = Player_Hitbox(game,self.x+(8*MUTIPIE_SIZE),self.y+(20*MUTIPIE_SIZE),16*MUTIPIE_SIZE,10*MUTIPIE_SIZE)
        
    def update(self):
        self.movement()
        self.update_animation()        
        self.hit_check()
        self.x_change = 0
        self.y_change = 0
        self.facing = "Idle"
        if self.objcarry != None:
            if self.objcarry.type() == "NPC":
                if self.Last_Move == "Up":
                    self.objcarry.update_img(160,0,180)
                    self.objcarry.rect.x = self.rect.x + 1 * MUTIPIE_SIZE
                    self.objcarry.rect.y = self.rect.y - 10 * MUTIPIE_SIZE
                elif self.Last_Move == "Down":
                    self.objcarry.update_img(160,0,0)
                    self.objcarry.rect.x = self.rect.x + 0 * MUTIPIE_SIZE
                    self.objcarry.rect.y = self.rect.y - 13 * MUTIPIE_SIZE
                elif self.Last_Move == "Right":
                    self.objcarry.update_img(0,124,90)
                    self.objcarry.rect.x = self.rect.x + 0 * MUTIPIE_SIZE
                    self.objcarry.rect.y = self.rect.y - 13 * MUTIPIE_SIZE
                elif self.Last_Move == "Left":
                    self.objcarry.update_img(0,64,270)
                    self.objcarry.rect.x = self.rect.x + 0 * MUTIPIE_SIZE
                    self.objcarry.rect.y = self.rect.y - 13 * MUTIPIE_SIZE
            else:
                self.objcarry.rect.x = self.rect.x + 10 * MUTIPIE_SIZE
                self.objcarry.rect.y = self.rect.y - 11 * MUTIPIE_SIZE
                

    def update_animation(self):
        self.anime_walk()
        self.anime_stop()
        
    def anime_walk(self):
        if self.iscarry:
            move_anime = {"Down" : 287 , "Up" : 477 , "Right" : 414 , "Left": 350}
        else:
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
                if self.iscarry:
                    self.image = self.game.character_spritesheet.get_sprite(32,446,self.width,self.height)
                    
                else:
                    self.image = self.game.character_spritesheet.get_sprite(0,192,self.width,self.height)

            elif self.Last_Move == "Right":
                if self.iscarry:
                    self.image = self.game.character_spritesheet.get_sprite(160,383,self.width,self.height)
                else:
                    self.image = self.game.character_spritesheet.get_sprite(160,128,self.width,self.height)
                
            
            elif self.Last_Move == "Left":
                if self.iscarry:
                    self.image = self.game.character_spritesheet.get_sprite(160,319,self.width,self.height)
                else:
                    self.image = self.game.character_spritesheet.get_sprite(160,64,self.width,self.height)
                
            elif self.Last_Move == "Down" :
                if self.iscarry:
                    self.image = self.game.character_spritesheet.get_sprite(160,256,self.width,self.height)
                    
                else:
                    self.image = self.game.character_spritesheet.get_sprite(160,0,self.width,self.height)
                
            self.count_Move_loop = 0
            self.count_Move = 0
        self.image = pygame.transform.scale(self.image, (TILESIZE * MUTIPIE_SIZE , TILESIZE * MUTIPIE_SIZE ))

    def movement(self):
        cheack = self.Hitbox.check_Boolean_Wall_Hit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if cheack == False:
                self.x_change -= PLAYER_SPEED
            self.facing = 'Left'
            self.Last_Move = "Left"
        
        if keys[pygame.K_RIGHT]:
            if cheack == False:
                self.x_change += PLAYER_SPEED
            self.facing = 'Right'
            self.Last_Move = "Right"
        
        if keys[pygame.K_UP]:
            if cheack == False:
                self.y_change -= PLAYER_SPEED
            self.facing = 'Up'
            self.Last_Move = "Up"
            
        
        if keys[pygame.K_DOWN]:
            if cheack == False:
                self.y_change += PLAYER_SPEED
            self.facing = 'Down'
            self.Last_Move = "Down"
    
    def hit_check(self):
        hit = self.Hitbox.check_Wall_Hit()

        if hit:
            if self.Last_Move == "Left":
                self.rect.x += 1
            elif self.Last_Move == "Right":
                self.rect.x -= 1
            if self.Last_Move == "Up":
                self.rect.y += 1
            elif self.Last_Move == "Down":
                self.rect.y -= 1
            self.Hitbox.setposition(self.rect.x + (8 * MUTIPIE_SIZE), self.rect.y + (20 * MUTIPIE_SIZE))
        else:
            self.rect.x += self.x_change
            self.rect.y += self.y_change

            self.Hitbox.setposition(self.rect.x + (8 * MUTIPIE_SIZE), self.rect.y + (20 * MUTIPIE_SIZE))


    def popobjcarry(self):
        self.iscarry = False
        result = self.objcarry
        self.objcarry = None
        return result

class Player_Hitbox(pygame.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = 0

        self.groups = self.game.all_sprites , self.game.playerhitbox
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = pygame.Surface([self.width , self.height])
        self.image.set_colorkey(BLACK)
        self.hitbox = pygame.Rect(0, 0, width , height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if SHOWHITBOX:
            pygame.draw.rect(self.image, RED, self.hitbox, 2)

    def Move(self,x,y):
        self.rect.x += x
        self.rect.y += y
    
    def setposition(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
    def check_Wall_Hit(self):
        if pygame.sprite.spritecollide(self, self.game.wall, False):
            return pygame.sprite.spritecollide(self, self.game.wall, False)

    def check_Boolean_Wall_Hit(self):
        if pygame.sprite.spritecollide(self, self.game.wall, False):
            return True
        else:
            return False

# ==============================================Map===============================================================

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
        

class Wall(pygame.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = HITBOX_LAYER

        self.groups = self.game.all_sprites , self.game.wall
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = pygame.Surface([self.width , self.height])
        self.image.set_colorkey(BLACK)
        self.hitbox = pygame.Rect(0, 0, width , height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if SHOWHITBOX:
            pygame.draw.rect(self.image, RED, self.hitbox, 2)
        
class BloodStorage(pygame.sprite.Sprite):
    def __init__(self,game, x=0, y=0, bloodgroups = ""):
        self.game = game
        self._layer = BLOOD_STORAGE
        self.width = 20
        self.height = 26
        self.groups = self.game.all_sprites, self.game.blood_storage_Layer
        
        self.bloodgroups = bloodgroups
        pygame.sprite.Sprite.__init__(self, self.groups)
    

        self.image = self.game.blood_storage_image.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        
        if self.bloodgroups != "":
            self.inventory = Stack()
            self.text = self.bloodgroups
            self.update_text()    
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def Pop_Storage(self):
        if self.bloodgroups != "" and self.inventory.size() > 0:
            obj = self.inventory.pop()  
            self.game.all_sprites.add(obj)  
            self.update_text()  
            return obj  
        else:
            return None
            
    
    def Push_Storage(self,obj):
        if self.bloodgroups == obj.bloodgroups:
            if self.inventory.size() < 4:
                self.inventory.push(obj)
                self.update_text()
                obj.kill()

                return True
        return False
    
    def update_text(self):
        self.small_text = f"{self.inventory.size()}/4"
        
        shadow_surface = self.game.font.render(self.text, True, GRAY_SHADOW_FONT)
        shadow_rect = shadow_surface.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))  

        text_surface = self.game.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, 20))

        shadow_small = self.game.font.render(self.small_text, True, GRAY_SHADOW_FONT)
        shadow_small_rect = shadow_small.get_rect(center=(self.image.get_width() // 2 + 2, 60 + 2))  

        small_surface = self.game.font.render(self.small_text, True, WHITE)
        small_rect = small_surface.get_rect(center=(self.image.get_width() // 2, 60))

        if len(self.bloodgroups) == 1:
            text_rect.x = 7*MUTIPIE_SIZE
            text_rect.y = 10*MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1*MUTIPIE_SIZE
            shadow_rect.y = text_rect.y
        elif len(self.bloodgroups) == 2:
            text_rect.x = 5*MUTIPIE_SIZE
            text_rect.y = 10*MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1*MUTIPIE_SIZE
            shadow_rect.y = text_rect.y
            
        small_rect.x = 2*MUTIPIE_SIZE
        small_rect.y = 17*MUTIPIE_SIZE
        shadow_small_rect.x = small_rect.x + 1*MUTIPIE_SIZE
        shadow_small_rect.y = small_rect.y
        self.image.fill((0, 0, 0, 0))
        self.image = self.game.blood_storage_image.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        self.image.blit(shadow_surface, shadow_rect)
        self.image.blit(text_surface, text_rect)
        self.image.blit(shadow_small, shadow_small_rect)
        self.image.blit(small_surface, small_rect)

        

class Bed(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        self._layer = BED_LAYER
        self.game = game
        self.on_bed = None
        self.blood_bag = None
        self.width = 20
        self.height = 46
        self.status = ""
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.Bed_image.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.status == "Drawing blood":
            if self.blood_bag.status == "Full":
                self.status = "Success"
                self.on_bed.kill_text()
        

    def drawing_blood(self):
        self.status = "Drawing blood"
        self.blood_bag.status = "Drawing blood"
        self.blood_bag.bloodgroups = self.on_bed.blood_groups

    def add_blood_bag(self,obj):
        self.blood_bag = obj
        self.blood_bag.rect.x = self.rect.x + 15*MUTIPIE_SIZE
        self.blood_bag.rect.y = self.rect.y - 15*MUTIPIE_SIZE
    def add_to_bed(self,obj):
        self.on_bed = obj
        self.on_bed.rect.x = self.rect.x - 6*MUTIPIE_SIZE
        self.on_bed.rect.y = self.rect.y + 4*MUTIPIE_SIZE
        self.on_bed.update_img(160,0)
        self.on_bed._layer = NPC_LAYER_ON_BED 
        self.game.all_sprites.change_layer(self.on_bed, NPC_LAYER_ON_BED)

class Down_Bed(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        self._layer = BED_DOWN_LAYER
        self.game = game
        self.width = 20
        self.height = 46
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.Bed_image.get_sprite(20, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Iv_Stand(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        self._layer = MAP_LAYER
        self.game = game
        self.width = 20
        self.height = 36
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.iv_stand_image.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


# ==============================================NPC===============================================================

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img ,type ,blood_groups):
        self.game = game
        self._layer = SPAWN_NPC
        self.groups = self.game.all_sprites, self.game.npc
        self.typeofnpc = type
        self.blood_groups = blood_groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.facing = ''
        self.width = TILESIZE
        self.height = TILESIZE
        self.npcsprite = img
        self.image = self.npcsprite.get_sprite(0, 186, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.target_pos = (x, y)
        self.rotation_angle = 90  
        self.count_Move = 0
        self.count_Move_loop = 0
        self.text_follow = None

    def update_img(self, x, y ,angle = 0):
        self.rotation_angle = angle
        self.image = self.npcsprite.get_sprite(x, y, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.rotate(self.image, self.rotation_angle)

    def add_text(self,obj):
        self.text = obj

    def update(self):
        self.move_to_target()
        if self.text != None:
            self.text.rect.x = self.rect.x + 10*MUTIPIE_SIZE
            self.text.rect.y = self.rect.y - 10*MUTIPIE_SIZE
    
    def kill_text(self):
        self.text.kill()
        self.text = None

    def move_to_target(self):

        if self.target_pos != None:
            self.facing = 'Moving'
            
            if self.rect.x < self.target_pos[0]:
                self.rect.x += self.speed
            elif self.rect.x > self.target_pos[0]:
                self.rect.x -= self.speed
            if self.rect.y < self.target_pos[1]:
                self.rect.y += self.speed
            elif self.rect.y > self.target_pos[1]:
                self.rect.y -= self.speed


        if self.facing != "Idle" :
            self.image = self.npcsprite.get_sprite(self.count_Move * TILESIZE,217, self.width,self.height)
            self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
            self.count_Move_loop += 1
            if self.count_Move == 5:
                self.count_Move = 0  
           
            if self.count_Move_loop >= 12:
                self.count_Move_loop = 0
                self.count_Move += 1

        if (self.rect.x, self.rect.y) == self.target_pos:
            self.target_pos = None
            self.facing = "Idle"
            self.image = self.npcsprite.get_sprite(0, 186, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))

    def rotate(self, angle):
        self.rotation_angle = angle
        self.update_img(self.rect.x, self.rect.y) 
    
    def type(self):
        return "NPC"


# ==============================================TrigerBox===============================================================

class TrigerBox(pygame.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = HITBOX_LAYER
        self.groups = self.game.all_sprites , self.game.trigger_donate_zone
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = pygame.Surface([self.width , self.height])
        self.image.set_colorkey(BLACK)
        self.hitbox = pygame.Rect(0, 0, width , height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if SHOWHITBOX:
            pygame.draw.rect(self.image, BLUE, self.hitbox, 2)

    def Move(self,x,y):
        self.rect.x += x
        self.rect.y += y
    
    def setposition(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
    def check_Hit(self,hitbox):
        if pygame.sprite.spritecollide(self,hitbox, False):
            return True
        else:
            return False
        

class Blood_Bag(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0 , Status = "Empty" ,Blood_Groups = ""):
        self._layer = BLOOD_BAG
        self.game = game
        self.width = 14
        self.height = 18
        self.groups = self.game.all_sprites,
        self.status = Status
        self.bloodgroups = Blood_Groups
        self.count_Move = 0
        self.count_Move_loop = 0
        
        pygame.sprite.Sprite.__init__(self, self.groups)

        if Blood_Groups != "":
            self.image = self.game.blood_bag_image.get_sprite(0, 0, self.width, self.height)
            self.create_text()
            

        if self.status == "Empty":
            self.image = self.game.blood_bag_image.get_sprite(112, 0, self.width, self.height)
        
        self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def update(self):
        self.animation()

    def animation(self):
        if self.status == "Drawing blood" :
            self.image = self.game.blood_bag_image.get_sprite((self.width*8)-(self.count_Move * self.width),0, self.width,self.height)
            self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
            self.image.set_colorkey(BLACK)
            self.count_Move_loop += 1
            if self.count_Move == 9:
                self.count_Move = 0
                self.count_Move_loop = 0
                self.status = "Full"
           
            if self.count_Move_loop >= 60:
                self.count_Move_loop = 0
                self.count_Move += 1
        elif self.status == "Full":
            self.image = self.game.blood_bag_image.get_sprite(0, 0, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (self.width * MUTIPIE_SIZE, self.height * MUTIPIE_SIZE))
            self.create_text()
            self.image.set_colorkey(BLACK)
            
    def create_text(self):
        self.text = self.bloodgroups        
        shadow_surface = self.game.font.render(self.text, True, RED_BLOOD_SHADOW)
        shadow_rect = shadow_surface.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))  

        text_surface = self.game.font.render(self.text, True, RED_BLOOD)
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, 20))

        if len(self.bloodgroups) == 1:
            text_rect.x = 4*MUTIPIE_SIZE
            text_rect.y = 5*MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1*MUTIPIE_SIZE
            shadow_rect.y = text_rect.y
        elif len(self.bloodgroups) == 2:
            text_rect.x = 1*MUTIPIE_SIZE
            text_rect.y = 5*MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1*MUTIPIE_SIZE
            shadow_rect.y = text_rect.y
        
        self.image.blit(shadow_surface, shadow_rect)
        self.image.blit(text_surface, text_rect)


    def type(self):
        return "Blood_Bag"
    
class Text_Follow(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0, text=""):
        self.game = game
        self._layer = TEXT_LAYER
        self.width = 20 * MUTIPIE_SIZE
        self.height = 18 * MUTIPIE_SIZE
        self.text = text
        self.groups = self.game.all_sprites ,
        pygame.sprite.Sprite.__init__(self, self.groups)

        # สร้าง surface สำหรับ image
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if len(self.text) == 1:
            shadow_surface = self.game.fontShadow.render(self.text, True, RED_BLOOD_SHADOW)
            shadow_rect = shadow_surface.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))
            shadow_surface2 = self.game.fontShadow.render(self.text, True, RED_BLOOD_SHADOW)
            shadow_rect2 = shadow_surface2.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))
            text_surface = self.game.font.render(self.text, True, RED_BLOOD)
            text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, 20))
        
            text_rect.x = 3 * MUTIPIE_SIZE 
            text_rect.y = 5 * MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1 * MUTIPIE_SIZE
            shadow_rect.y = text_rect.y 
            shadow_rect2.x = text_rect.x
            shadow_rect2.y = text_rect.y
        elif len(self.text) == 2:
            shadow_surface = self.game.font.render(self.text, True, RED_BLOOD_SHADOW)
            shadow_rect = shadow_surface.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))
            shadow_surface2 = self.game.font.render(self.text, True, RED_BLOOD_SHADOW)
            shadow_rect2 = shadow_surface2.get_rect(center=(self.image.get_width() // 2 + 2, 20 + 2))
            text_surface = self.game.font.render(self.text, True, RED_BLOOD)
            text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, 20))

            text_rect.x = 1 * MUTIPIE_SIZE
            text_rect.y = 5 * MUTIPIE_SIZE
            shadow_rect.x = text_rect.x + 1 * MUTIPIE_SIZE
            shadow_rect.y = text_rect.y 
            shadow_rect2.x = text_rect.x + 2 * MUTIPIE_SIZE
            shadow_rect2.y = text_rect.y 

        # Blit text onto the image
        self.image.blit(shadow_surface, shadow_rect)
        self.image.blit(shadow_surface2, shadow_rect2)
        self.image.blit(text_surface, text_rect)
