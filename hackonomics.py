import matplotlib.pyplot as plt
import numpy as np
import random
from button import Button
from slider import Slider
from pygame_functions import *
from sys import exit
import time


Explanation_text = ["""Now, if there are more buyers than sellers (like a super popular toy everyone wants!), demand goes up.                 
Imagine the demand line shifting to the right. This means more people are willing to buy at every price.                
On the graph, the new demand line would cross the supply line at a higher price (P2) and quantity (Q2).                 
So, the price goes up because buyers are competing for the limited stuff sellers have, and more of the product gets sold!""",
                    "2",
                    "3"]


seller = Slider(1000,500,200)
buyer = Slider(1000,400,200)
seller.set_knob_color((255,255,0))
buyer.set_knob_color((0,255,0))
menu = True
widths = [-20,90,200,310,420,530,640,750,860,970]
stall_rect = [0] * 10
stall_active = [0] * 10

pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("supply and demand simulation")
clock = pygame.time.Clock()

black_vertical_line = pygame.Surface((3,1080))
black_vertical_line.fill("black")

black_horizontal_line = pygame.Surface((700,3))
black_horizontal_line.fill("black")

sky_surface = pygame.Surface((1420,800))
sky_surface.fill("sky blue")

cloud_surface = pygame.image.load("images/cloud.png")
cloud_surface_scaled = pygame.transform.scale(cloud_surface,(250,100))


moreBuyers = pygame.image.load("images/bigger.png").convert()
moreBuyers_scaled = pygame.transform.scale(moreBuyers,(600,500))


sameBuyers = pygame.image.load("images/same.png").convert()
sameBuyers_scaled = pygame.transform.scale(sameBuyers,(600,500))

lessBuyers = pygame.image.load("images/smaller.png").convert()
lessBuyers_scaled = pygame.transform.scale(lessBuyers,(600,500))



ground_surface = pygame.image.load("images/ground.png").convert()
ground_surface_scaled = pygame.transform.scale(ground_surface,(1420,280))

stall_surface = pygame.image.load("images/stall.png")
stall_surface_scaled = pygame.transform.scale(stall_surface,(150,150))

right_surface = pygame.Surface((700,1080))
right_surface.fill("white")

person_surface_back = pygame.image.load("images/mario_back.png").convert_alpha()
person_surface_scaled_back = pygame.transform.scale(person_surface_back,(80,100))
person_rect_back = person_surface_scaled_back.get_rect(bottomleft = (1120,815))

person_surface_right = pygame.image.load("images/mario.png").convert_alpha()
person_surface_scaled_right = pygame.transform.scale(person_surface_right,(80,100))
person_rect_right = person_surface_scaled_right.get_rect(bottomleft = (1120,815))

person_surface_scaled_left = pygame.transform.flip(person_surface_scaled_right,True,False)
person_rect_left = person_surface_scaled_left.get_rect(bottomleft = (1120,815))


bg = pygame.image.load("images/Background.png")
bg_scaled = pygame.transform.scale(bg,(1920,1080))

def get_font(size): 
    return pygame.font.Font("font.ttf", size)

title_font = get_font(100)
button_font = get_font(50)
bs_font = get_font(40)

explanation_font = pygame.font.SysFont("Comic sans", 21, bold=True, italic=False)


def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width > 1860:
                x= pos[0]
                y+= word_height
            surface.blit(word_surface,(x,y))
            x+= word_width +space
        x = pos[0]
        y+= word_height



for i in range(len(stall_rect)):
    stall_rect[i] = stall_surface_scaled.get_rect(bottomleft = (widths[i],820))

class Buyer:
    def __init__(self, stall_rects, start_x, start_y, speed=8):
        self.stall_rects = stall_rects
        self.stall_order = list(range(len(stall_rects)))
        random.shuffle(self.stall_order)  # random order of stalls
        self.current_index = 0
        self.returning = False
        self.paused = False
        self.pause_start = 0
        self.pause_duration = random.randint(1000, 2500)  #pause duration
        self.rect = person_surface_scaled_back.get_rect(bottomleft=(start_x, start_y))
        self.speed = speed + random.randint(-1, 1)  # adds slight variation in speeds
        self.start_delay = pygame.time.get_ticks() + random.randint(0, 1500)  # offset start
        self.started = False
        self.done = False
        self.loops_completed = 0
        self.max_loops = 2

    def get_direction(self,target_x):
        if target_x == None:
            return -1
        if self.rect.x > target_x:
            return -1
        elif self.rect.x == target_x:
            return 0
        else:
            return  1
                        
    def update(self):
        now = pygame.time.get_ticks()

        # Wait for start delay
        if not self.started:
            if now >= self.start_delay:
                self.started = True
            else:
                return

        if not self.returning:
            if self.current_index < len(self.stall_order):
                stall_idx = self.stall_order[self.current_index]
                target_x = self.stall_rects[stall_idx].x + 35
                

                if not self.paused:
                    if abs(self.rect.x - target_x) > self.speed:
                        # Move toward the target
                        direction = self.get_direction(target_x)
                        self.rect.x += direction * self.speed
                    else:
                        self.rect.x = target_x
                        self.paused = True
                        self.pause_start = now
                else:
                    if now - self.pause_start >= self.pause_duration:
                        self.paused = False
                        self.current_index += 1
            else:
                self.returning = True
                target_x = 1220

        else:
            target_x = 1220
            if self.rect.x < target_x:
                self.rect.x += self.speed
            else:
                self.loops_completed += 1
                if self.loops_completed >= self.max_loops:
                    self.done = True
                else:
                    self.stall_order = list(range(len(self.stall_rects)))
                    random.shuffle(self.stall_order)
                    self.current_index = 0
                    self.returning = False
                    self.paused = False
                    self.pause_duration = random.randint(1000, 2500)

        return target_x
    def draw(self, surface,target_x):
        direction = self.get_direction(target_x)
        if direction == 0:
            surface.blit(person_surface_scaled_back, self.rect)

        elif direction == -1:
            surface.blit(person_surface_scaled_left,self.rect)
        
        elif direction == 1:
            surface.blit(person_surface_scaled_right,self.rect)

def simulation(num_Of_Sellers, num_Of_Buyers):

    seagull_start_x = 0
    seagull_surface = pygame.image.load("images/seagull.png")
    seagull_surface_scaled_right = pygame.transform.scale(seagull_surface,(75,75))
    seagull_rect = seagull_surface_scaled_right.get_rect(bottomleft = (seagull_start_x, 500))
    seagull_surface_scaled_left = pygame.transform.flip(seagull_surface_scaled_right, True, False)


    global menu
    buyers = [Buyer(stall_rect[:num_Of_Sellers], 1120, 815) for _ in range(num_Of_Buyers)]
    simulation_done = False
    seagull_returning = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()


        screen.fill("black")
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface_scaled, (0, 800))

        if seagull_returning is True:
            seagull_rect.x += 5
            screen.blit(seagull_surface_scaled_right,(seagull_rect.x,400))
            if seagull_rect.x >= 1220:
                seagull_returning = False
        else:
            seagull_rect.x -= 5
            screen.blit(seagull_surface_scaled_left,(seagull_rect.x,400))
            if seagull_rect.x <= -50:
                seagull_returning = True

        screen.blit(cloud_surface_scaled, (100,300))
        screen.blit(cloud_surface_scaled, (900,200))
        screen.blit(cloud_surface_scaled, (500,100))
        screen.blit(cloud_surface_scaled, (650,400))

        
        
        menu_button = Button(
            image= pygame.image.load("images/quit.png"), pos=(135, 50), text_input="Menu",
            font=button_font, base_color="#fcf935", hovering_color="white"
        )
        for button in [menu_button]:
            button.changeColor(mouse)
            button.update(screen)

        for i in range(num_Of_Sellers):
            screen.blit(stall_surface_scaled, stall_rect[i])

        if not simulation_done:
            all_done = True
            active_buyers = []
    
            for buyer in buyers:
                if not buyer.done:
                    target_x = buyer.update()
                    buyer.draw(screen,target_x)
                    active_buyers.append(buyer)
                    all_done = False  # checks if any buyers still active
    
            buyers = active_buyers  # Keep only active buyers and rest invisible
    
            if all_done:
                simulation_done = True

        
            
            
        screen.blit(right_surface, (1220, 0))
        screen.blit(black_vertical_line, (1220, 0))
        screen.blit(black_horizontal_line, (1220, 540))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mouse):
                    menu = True
                    main_menu()
        if num_Of_Buyers > num_Of_Sellers:
            screen.blit(moreBuyers_scaled,(1280,0))
            display_text(screen, Explanation_text[0], (1280,580), explanation_font, "black")
        elif num_Of_Buyers == num_Of_Sellers:
            screen.blit(sameBuyers_scaled,(1320,0))
        
        elif num_Of_Buyers < num_Of_Sellers:
            screen.blit(lessBuyers_scaled,(1320,0))

        pygame.display.update()
        clock.tick(30)

def main_menu():
    pygame.display.set_caption("menu")
    global menu
    while menu:
        screen.fill("black")
        screen.blit(bg_scaled,(0,0))

        mouse = pygame.mouse.get_pos()

        buyer_text = bs_font.render("Buyers",True, "Green")
        buyer_rect = buyer_text.get_rect(center=(800,400))
        screen.blit(buyer_text, buyer_rect)

        seller_text = bs_font.render("Sellers",True, "Yellow")
        seller_rect = seller_text.get_rect(center=(800,500))
        screen.blit(seller_text, seller_rect)

        menu_text = title_font.render("Main Menu",True, "White")
        menu_rect = menu_text.get_rect(center=(960,125))

        start_button = Button(image=pygame.image.load("images/start.png"),pos=(960,750)
                             ,text_input="START",font = button_font,base_color = "Green", hovering_color = "white")

        quit_button = Button(image=pygame.image.load("images/quit.png"),pos=(960,900)
                             ,text_input="QUIT",font = button_font,base_color = "red", hovering_color = "white")
        
        screen.blit(menu_text, menu_rect)
        for button in [start_button,quit_button]:
            button.changeColor(mouse)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            buyer.handle_event(event)
            seller.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse):
                    menu = False
                    simulation(seller.get_value(),buyer.get_value())
                if quit_button.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()
        buyer.draw(screen)
        seller.draw(screen)
        pygame.display.update()
        clock.tick(30)

main_menu()


         



#q1 = random.randint(60,80)
#m1 = random.uniform(0.5,1.0)
#print("q1: ",q1,"p1: ",m1)
#q2 = 0
#m2 = random.uniform(0.5,1.0)
#print("q2: ",q2,"p2: ",m2)
#buyers = Buyers(q1,m1)
#sellers = Sellers(q2,m2)

#eq_qty, eq_price = find_equilibrium(buyers,sellers)
#demand_qty, demand_price = buyers.demand_points()
#supply_qty, supply_price = sellers.supply_points()
#plt.plot(demand_qty,demand_price)
#plt.plot(demand_qty+20,demand_price+20) #shifts it to right
#plt.plot(supply_qty,supply_price)
#plt.xlim(0,100)
#plt.ylim(0,100)
#plt.xlabel("Quantity")
#plt.ylabel("Price")
#plt.title("Supply and Demand")
#plt.show()
