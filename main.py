import pygame
import sys
from config import *
from sprites import *
import random
import time
from Linked_List_system import LinkedList

class Game:
    def __init__(self) -> None:
        pygame.init
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("assets/Docter/Test.png")
        self.Map_image = Spritesheet("assets/Map/WALL.png")
        self.npc_linkedlist = LinkedList()  # สร้างคิวสำหรับ NPC
        self.npc_donate_move_Y = [int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 33)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 23)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 13))]

    def create_wall_map(self):
        self.map = Map(self)
        # TOP
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,MAP_SIZE_X*MUTIPIE_SIZE,40*MUTIPIE_SIZE)
        
        # Left
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,4*MUTIPIE_SIZE,MAP_SIZE_Y*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X+(36*MUTIPIE_SIZE),MAP_START_POSITION_Y+(124*MUTIPIE_SIZE),4*MUTIPIE_SIZE,36*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X+(4*MUTIPIE_SIZE),MAP_START_POSITION_Y+(124*MUTIPIE_SIZE),36*MUTIPIE_SIZE,36*MUTIPIE_SIZE)
        self.npc_donate_trigerbox = TrigerBox(self,MAP_START_POSITION_X+(4*MUTIPIE_SIZE),MAP_START_POSITION_Y+(109*MUTIPIE_SIZE),36*MUTIPIE_SIZE,16*MUTIPIE_SIZE)

        
        # Right
        Wall(self,MAP_START_POSITION_X+((MAP_SIZE_X*MUTIPIE_SIZE)-(4*MUTIPIE_SIZE)),MAP_START_POSITION_Y,4*MUTIPIE_SIZE,MAP_SIZE_Y*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X+((MAP_SIZE_X*MUTIPIE_SIZE)-(40*MUTIPIE_SIZE)),MAP_START_POSITION_Y+(124*MUTIPIE_SIZE),4*MUTIPIE_SIZE,36*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X+((MAP_SIZE_X*MUTIPIE_SIZE)-(40*MUTIPIE_SIZE)),MAP_START_POSITION_Y+(124*MUTIPIE_SIZE),37*MUTIPIE_SIZE,36*MUTIPIE_SIZE)
        self.npc_sick_trigerbox = TrigerBox(self,MAP_START_POSITION_X+((MAP_SIZE_X*MUTIPIE_SIZE)-(40*MUTIPIE_SIZE)),MAP_START_POSITION_Y+(109*MUTIPIE_SIZE),36*MUTIPIE_SIZE,16*MUTIPIE_SIZE)

        # Botton
        Wall(self,MAP_START_POSITION_X+(36*MUTIPIE_SIZE),MAP_START_POSITION_Y+((MAP_SIZE_Y*MUTIPIE_SIZE)-(4*MUTIPIE_SIZE)),128*MUTIPIE_SIZE,4*MUTIPIE_SIZE)

    def create_npc_queue_donate(self):
        self.npc_donate_move_X = [int(MAP_START_POSITION_X+(MUTIPIE_SIZE*13)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*20)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*13)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*17))]
        npc = NPC(self,self.npc_donate_move_X[3],SCREEN_HEIGHT)
        self.npc_linkedlist.append(npc)
        npc.target_pos = (self.npc_donate_move_X[self.npc_linkedlist.size()-1],self.npc_donate_move_Y[self.npc_linkedlist.size()-1])
        if self.npc_linkedlist.size() == 1:
            self.current_npc = self.npc_linkedlist.get_head_data()
        else:
            self.current_npc = self.current_npc.next

    def update_npc_donate(self):
        if not self.npc_linkedlist.isEmpty():
            if self.current_npc.data.facing == "Idel" and self.npc_linkedlist.size() != 3:
                self.create_npc_queue_donate()
                
    def move_npc_to_player_head(self):
        if not self.npc_linkedlist.isEmpty():
            npc_to_move = self.npc_linkedlist.pop_front()  
            npc_to_move.rect.x = self.player.rect.x  
            npc_to_move.rect.y = self.player.rect.y - (PLAYER_SIZE_Y * MUTIPIE_SIZE)  
            npc_to_move.target_pos = None  
            npc_to_move.facing = 'Idel'
    

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.playerhitbox = pygame.sprite.LayeredUpdates()
        self.trigger_donate_zone = pygame.sprite.LayeredUpdates()
        self.create_wall_map()
        self.player = Player(self)
        self.create_npc_queue_donate()

    def triger_box_check(self):
        keys = pygame.key.get_pressed()
        if self.npc_donate_trigerbox.check_Hit(self.playerhitbox):
            if keys[pygame.K_SPACE]:
                print("pick_Npc")
                time.sleep(0.2)
        elif self.npc_sick_trigerbox.check_Hit(self.playerhitbox):
            if keys[pygame.K_SPACE]:
                print("pick_sick_Npc")
                time.sleep(0.2)
            
        
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.update_npc_donate()
        self.triger_box_check()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.event()
            self.update()
            self.draw()
        self.running = False

    def gameover(self):
        pass

    def intro_screen(self):
        pass
    
def main():
    g = Game()
    g.intro_screen()
    g.new_game()
    while g.running:
        g.main()
        g.gameover()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()