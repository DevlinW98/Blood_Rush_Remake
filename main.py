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
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("assets/Docter/Test.png")
        self.Map_image = Spritesheet("assets/Map/WALL.png")
        self.Bed_image = Spritesheet("assets/Bed/Bed.png")
        self.blood_storage_image = Spritesheet("assets/Blood storage cabinet/Blood storage cabinet.png")
        self.blood_bag_image = Spritesheet("assets/Blood_pack/Pixilart Sprite Sheet.png")
        self.iv_stand_image = Spritesheet("assets/IV_STAND/IV_STAND.png")
        self.NPC_imge = [
            Spritesheet("assets/NPC/NPC1.png"),
            Spritesheet("assets/NPC/NPC2.png")
        ]

        self.font = pygame.font.Font('assets/Font/PressStart2P-vaV7.ttf', 26)
        self.fontShadow = pygame.font.Font('assets/Font/PressStart2P-vaV7.ttf', 32)
        self.font.set_bold(True)
        self.fontShadow.set_bold(True)
        self.npc_Donate_linkedlist = LinkedList()  # สร้างคิวสำหรับ NPC
        self.npc_donate_move_Y = [int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 55)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 40)),int(SCREEN_HEIGHT - (MUTIPIE_SIZE * 25))]
        self.npc_donate_move_X = [int(MAP_START_POSITION_X+(MUTIPIE_SIZE*5)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*0)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*5)),int(MAP_START_POSITION_X+(MUTIPIE_SIZE*17))]
        self.blood_groups = ["A","B","AB","O"]
        self.last_action_time = 0
    
            

    def create_npc_queue_donate(self):
        random_img = random.choice(self.NPC_imge)
        random_blood = random.choice(self.blood_groups)
        npc = NPC(self,self.npc_donate_move_X[3],SCREEN_HEIGHT,random_img,"Donate",random_blood)
        npc.add_text(Text_Follow(self,npc.rect.x,npc.rect.y,npc.blood_groups))
        self.npc_Donate_linkedlist.append(npc)
        npc.target_pos = (self.npc_donate_move_X[self.npc_Donate_linkedlist.size()-1],self.npc_donate_move_Y[self.npc_Donate_linkedlist.size()-1])
        if self.npc_Donate_linkedlist.size() == 1:
            self.current_npc = self.npc_Donate_linkedlist.get_head_data()
        else:
            self.current_npc = self.current_npc.next

    def update_npc_donate(self,command = ""):
        if not self.npc_Donate_linkedlist.isEmpty():
            if command == "Update_Move":
                move = self.npc_Donate_linkedlist.get_head_data()
                for i in range(self.npc_Donate_linkedlist.size()):
                    move.data.target_pos = (self.npc_donate_move_X[i] , self.npc_donate_move_Y[i])
                    move = move.next
            elif self.current_npc.data.facing == "Idle" and self.npc_Donate_linkedlist.size() != 3:
                self.create_npc_queue_donate()
        if self.npc_Donate_linkedlist.isEmpty():
            self.create_npc_queue_donate()
        
        

                
    def move_npc_to_player_head(self):
        if not self.npc_Donate_linkedlist.isEmpty():
            npc_to_move = self.npc_Donate_linkedlist.pop_front()  
            npc_to_move.rect.x = self.player.rect.x  
            npc_to_move.rect.y = self.player.rect.y - (PLAYER_SIZE_Y * MUTIPIE_SIZE)  
            npc_to_move.target_pos = None  
            npc_to_move.facing = 'Idle'
    

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.blood_storage_Layer = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.playerhitbox = pygame.sprite.LayeredUpdates()
        self.trigger_donate_zone = pygame.sprite.LayeredUpdates()
        self.create_wall_map()
        
        self.player = Player(self)
        self.create_blood_storage()

        
        
        self.create_npc_queue_donate()

    def triger_box_check(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        self.triger_box_blood_storage
        if self.npc_donate_trigerbox.check_Hit(self.playerhitbox) and self.player.iscarry is False:
            if keys[pygame.K_SPACE]:
                self.player.objcarry = self.npc_Donate_linkedlist.pop_front()
                self.player.iscarry = True
                self.player.objcarry.target_pos = None
                self.player.objcarry.rect.x = self.player.rect.x
                self.player.objcarry.rect.y = self.player.rect.y
                self.player.objcarry.facing = "Idle"
                self.update_npc_donate("Update_Move")
                
        elif self.npc_sick_trigerbox.check_Hit(self.playerhitbox) and self.player.iscarry is False:
            if keys[pygame.K_SPACE]:
                print("pick_sick_Npc")
                time.sleep(0.2)
        for i in range(int(len(self.blood_storage))):
            if self.blood_storage[i][1].check_Hit(self.playerhitbox):
                if keys[pygame.K_SPACE]:

                    # เพิ่มเงื่อนไขตรวจจับเวลาการกดปุ่มล่าสุด
                    if current_time - self.last_action_time > 200:  # 200ms delay
                        if self.player.iscarry is False:
                            if self.blood_storage[i][0].bloodgroups == "":
                                self.player.objcarry = Blood_Bag(self, self.player.rect.x, self.player.rect.y)
                                self.player.iscarry = True
                            else:
                                self.player.objcarry = self.blood_storage[i][0].Pop_Storage()
                                if self.player.objcarry is not None:
                                    self.player.iscarry = True

                        elif self.player.iscarry is True and self.player.objcarry.type() == "Blood_Bag":
                            if self.blood_storage[i][0].bloodgroups == "" and self.player.objcarry.bloodgroups == "":
                                self.player.objcarry.kill()
                                self.player.objcarry = None
                                self.player.iscarry = False
                            else:
                                if self.blood_storage[i][0].Push_Storage(self.player.objcarry):
                                    self.player.objcarry = None
                                    self.player.iscarry = False

                        # อัปเดตเวลาการกดปุ่มครั้งล่าสุด
                        self.last_action_time = current_time
        
        for i in range(int(len(self.bed))):
            if self.bed[i][1].check_Hit(self.playerhitbox):
                if keys[pygame.K_SPACE]:
                    if self.player.iscarry is True and self.player.objcarry.type() == "NPC" and self.bed[i][0].on_bed == None:
                        self.bed[i][0].add_to_bed(self.player.popobjcarry())
                        
                    elif self.player.iscarry is True and self.bed[i][0].on_bed != None and self.player.objcarry.type() == "Blood_Bag":
                        if self.bed[i][0].blood_bag == None:
                            if self.player.objcarry.status == "Empty" and self.bed[i][0].on_bed.typeofnpc == "Donate":
                                self.bed[i][0].add_blood_bag(self.player.popobjcarry())
                                self.bed[i][0].drawing_blood()
                    elif self.player.iscarry is False and self.bed[i][0].status == "Success":
                        self.player.objcarry = self.bed[i][0].blood_bag
                        self.player.iscarry = True
                        self.bed[i][0].status = ""
                        self.bed[i][0].blood_bag = None
                        self.bed[i][0].on_bed.kill()
                        self.bed[i][0].on_bed = None
                        
        
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

    # ======================================= Create Map =========================================================
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
        
        x_bed = MAP_START_POSITION_X+(32*MUTIPIE_SIZE)
        y_bed = MAP_START_POSITION_Y+(30*MUTIPIE_SIZE)
        self.bed = []
        for i in range(3):
            self.bed.append([])
            self.bed[i].append(Bed(self,x_bed,y_bed)) 
            Down_Bed(self,x_bed,y_bed)
            Iv_Stand(self,x_bed+(12*MUTIPIE_SIZE),y_bed-(19*MUTIPIE_SIZE))
            Wall(self,x_bed,y_bed,20*MUTIPIE_SIZE,41*MUTIPIE_SIZE)
            self.bed[i].append(TrigerBox(self,x_bed-(8*MUTIPIE_SIZE),y_bed+(10*MUTIPIE_SIZE),36*MUTIPIE_SIZE,30*MUTIPIE_SIZE)) 
            x_bed += 58*MUTIPIE_SIZE
            

    def create_blood_storage(self):
        
        self.blood_storage = []
        self.triger_box_blood_storage = []
        x = MAP_START_POSITION_X+(44*MUTIPIE_SIZE)
        y = MAP_START_POSITION_Y+(130*MUTIPIE_SIZE)
        for i in range(len(self.blood_groups)):
            self.blood_storage.append([])
            self.blood_storage[i].append(BloodStorage(self,x,y,self.blood_groups[i]))
            self.blood_storage[i].append(TrigerBox(self,x+(8*MUTIPIE_SIZE),y,4*MUTIPIE_SIZE,13*MUTIPIE_SIZE))
            self.blood_storage[i][0].Push_Storage(Blood_Bag(self,-20*MUTIPIE_SIZE,-20*MUTIPIE_SIZE,"Full",self.blood_groups[i]))
            self.blood_storage[i][0].Push_Storage(Blood_Bag(self,-20*MUTIPIE_SIZE,-20*MUTIPIE_SIZE,"Full",self.blood_groups[i]))
            Wall(self,x,MAP_START_POSITION_Y+(143*MUTIPIE_SIZE),20*MUTIPIE_SIZE,13*MUTIPIE_SIZE)
            x += 23*MUTIPIE_SIZE
        self.blood_storage.append([])
        self.blood_storage[len(self.blood_groups)].append(BloodStorage(self,x,y,""))
        self.blood_storage[len(self.blood_groups)].append(TrigerBox(self,x+(8*MUTIPIE_SIZE),y,4*MUTIPIE_SIZE,13*MUTIPIE_SIZE))
        Wall(self,x,MAP_START_POSITION_Y+(143*MUTIPIE_SIZE),20*MUTIPIE_SIZE,13*MUTIPIE_SIZE)
        Blood_Bag(self,x+(3*MUTIPIE_SIZE),y+(8*MUTIPIE_SIZE))
    
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