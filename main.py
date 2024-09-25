import pygame
import sys
from config import *
from sprites import *
import random

class Game:
    def __init__(self) -> None:
        pygame.init
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("assets/Docter/Test.png")
        self.Map_image = Spritesheet("assets/Map/WALL.png")

    def create_wall_map(self):
        self.map = Map(self)
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,MAP_SIZE_X*MUTIPIE_SIZE,40*MUTIPIE_SIZE)
        Wall(self,MAP_START_POSITION_X,MAP_START_POSITION_Y,MAP_SIZE_X*MUTIPIE_SIZE,40*MUTIPIE_SIZE)

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        
        self.create_wall_map()
        self.player = Player(self)
        
        
    

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        

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
