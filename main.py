import pygame
import sys
from config import *
from sprites import *
import random
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
        self.npc_donate_move = [int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 33)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 23)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 13))]

    def create_wall_map(self):
        self.map = Map(self)
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,MAP_SIZE_X*MUTIPIE_SIZE,40*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,MAP_SIZE_X*MUTIPIE_SIZE,40*MUTIPIE_SIZE)

    def create_npc_queue_donate(self):
        self.npc_donate_move_X = int(MAP_START_POSITION_X+(MUTIPIE_SIZE*17))
        npc = NPC(self,self.npc_donate_move_X,SCREEN_HEIGHT)
        self.npc_linkedlist.append(npc)
        npc.target_pos = (self.npc_donate_move_X, self.npc_donate_move[0])
        print(MAP_START_POSITION_X+(MUTIPIE_SIZE*3))
        self.npc_linkedlist.display()
        self.current_npc = self.npc_linkedlist.get_head_data()

    def update_npc_donate(self):
        if not self.npc_linkedlist.isEmpty():
            if self.current_npc.data.facing == "Idel" and self.npc_linkedlist.size() !=3:
                npc = NPC(self,self.npc_donate_move_X,SCREEN_HEIGHT)
                self.npc_linkedlist.append(npc)
                npc.target_pos = (self.npc_donate_move_X,self.npc_donate_move[self.npc_linkedlist.size()-1])
                self.npc_linkedlist.display()
                self.current_npc = self.current_npc.next


                
        pass
    

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        
        self.create_wall_map()
        self.player = Player(self)
        self.create_npc_queue_donate()
        
        
    

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.update_npc_donate()  # อัปเดตการเคลื่อนที่ของ NPC ในคิว

        

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
