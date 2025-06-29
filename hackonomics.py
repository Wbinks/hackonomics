import math
import numpy as np
import random
from button import Button
from slider import Slider
from pygame_functions import *
from sys import exit
import time

greater_text = ["""In this simulation, there are more buyers than sellers in the market. This causes demand to shift to the right (from D1 to D2) as the demographic for the product increases. However, at P1, this causes a disequilibrium in the market.""",
                    """Activity: Copy the graph and trace from the dotted line P1 to the new demand curve. Then trace down and find the new quantity demanded (label Q3).""",
                    """The diagram shows excess demand, where quantity demanded (Q3) exceeds quantity supplied (Q1), pushing the price up from P1 to P2. This higher price encourages producers to increase supply (Q1 -> Q2) and discourages some consumers (Q3 -> Q2), leading to a new equilibrium at P2Q2 where resources are allocated more efficiently.""",
                    ]
smaller_text = ["In this simulation, there are more sellers than buyers in the market. This causes supply to shift to the right (from S1 to S2) as there are more producers making products. However, at P1, this causes a disequilibrium in the market.",
                "Activity: Copy the graph and trace from the dotted line P1 to the new supply curve. Then trace down and find the new quantity supplied (label Q3).",
                "Supply (Q3) is higher than demand (Q1), causing prices to fall from P1 to P2 as sellers clear excess stock. Lower prices make producers reduce supply (Q3 -> Q2) and encourage more buyers (Q1 -> Q2), leading to a new market equilibrium at price P2 and quantity Q2."]

same_text = ["In this simulation, there are the same amount of sellers and buyers in the market. This means that the price remains constant at P1, not changing. (it may change slightly in this simulation as this is a rough equilibrium calculator)"]
product = Slider(860,450,200,1,4)
seller_slider = Slider(1110,725,200,1,10)
buyer_slider = Slider(610,725,200,1,10)
product.set_knob_color((173, 216, 230))
seller_slider.set_knob_color((255,255,0))
buyer_slider.set_knob_color((128, 0, 128))
menu = True
widths = [-20,90,200,310,420,530,640,750,860,970]
stall_rect = [0] * 10
stall_active = [0] * 10
number_of_trades_today = 0
new_equilibrium_prices = []
local_buyer_prices = []
local_seller_prices = []
trades_completed = 0

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

trades_font = get_font(15)
product_font = get_font(30)
title_font = get_font(100)
button_font = get_font(50)
bs_font = get_font(40)
explanation_font = pygame.font.SysFont("Comic sans", 25, bold=True, italic=False)

class Seller:
    def __init__(self,minimum_price,local_price):
        self.minimum_price = minimum_price
        self.local_price = local_price
        self.traded = False

for i in range(len(stall_rect)):
    stall_rect[i] = stall_surface_scaled.get_rect(bottomleft = (widths[i],820))

class Buyer:
    def __init__(self, stall_rects, start_x, start_y, speed, maximum_price,local_price, stall_seller_map):
        self.traded = False
        self.trade_attempted_stalls = set()
        self.stall_seller_map = stall_seller_map
        self.transaction_done = False
        self.maximum_price = maximum_price
        self.local_price = local_price
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
        self.max_loops = 10

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
                        self.transaction_done = False
                           
                else:
                    if not self.transaction_done:
                        stall_idx = self.stall_order[self.current_index]
                        seller = self.stall_seller_map.get(stall_idx)
    
                        if seller :
                            transaction({self: seller}, 5, True, market_pressure)  
                            print(f"Trade occurred at stall {stall_idx}")

                            self.transaction_done = True  

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

def product_category(option):
    #This array holds the lower/upper bounds of the price and the incrementations. 
    price_increment_bound_array = [[100,1000,50],[10000,20000,100],[10,100,5],[20,200,10]]
    if option == 1:
        return price_increment_bound_array[0]
    elif option == 2:
        return price_increment_bound_array[1]
    elif option == 3:
        return price_increment_bound_array[2]
    elif option == 4:
        return price_increment_bound_array[3]
    else:
        return "Error"
 
#This gives an initial equilibrium price by taking the median of 100 buyers and 100 sellers. 
def price_equilibrium(lower_bound,upper_bound):
    tseller_array = []
    tbuyer_array = []
    for i in range(100):
        tseller_array.append(random.randint(lower_bound,upper_bound))
        tbuyer_array.append(random.randint(lower_bound,upper_bound))
    tseller_array.sort()
    tbuyer_array.sort()
    median = int((tseller_array[50] + tseller_array[50]) / 2)
    return median

#This simulates how it'd actually be like with many buyers and many sellers
def accurate_equilibrium(num_of_buyers,num_of_sellers):
    if num_of_buyers == num_of_sellers:
        eq_num_of_buyers = 1000
        eq_num_of_sellers = 1000
    elif num_of_buyers > num_of_sellers:
        eq_num_of_buyers = int((1000 / num_of_sellers) * num_of_buyers)
        eq_num_of_sellers = 1000
    else:
        eq_num_of_sellers = int((1000 / num_of_buyers) * num_of_sellers)
        eq_num_of_buyers = 1000

    return [eq_num_of_buyers,eq_num_of_sellers]

#This assigns random prices between an upper and lower bound for buyers/sellers
#max_prices_buyers holds the maximum prices of the buyers
#min_prices_sellers holds the minimum prices for the sellers
def price_setter(type_of_agent,agents,lower_bound,upper_bound,equilibrium): 
    agents_array = []
    for i in range(agents):
        if type_of_agent == 1:
            agents_array.append(random.randint(equilibrium,upper_bound)) #assigns a random price between upper lower bounds
        elif type_of_agent == 2:
            agents_array.append(random.randint(lower_bound,equilibrium))
    
    return agents_array

#This allocates the prices from the price setter functions to respective objects 
#buyer_objects hold the array of objects with maximum prices
#seller_objects hold the array of objects with minimum prices
def price_to_agent(type_of_agent,price_array,local_price_array):
    buyer_array = []
    seller_array = []
    for price in price_array:
        if type_of_agent == 1:
            buyer_array.append(Buyer(stall_rect[:len(price_array)], 1120, 815, 8, price, price, stall_seller_map=None))
        elif type_of_agent == 2: #This is for a seller
            seller_array.append(Seller(price,price))

    counter = 0
    for price in local_price_array:
        if type_of_agent == 1:
            buyer_array[counter].local_price = price
        elif type_of_agent == 2:
            seller_array[counter].local_price = price
        counter += 1

    if type_of_agent == 1:
        return buyer_array
    elif type_of_agent == 2:
        return seller_array

#randomly allocates a buyer object to a seller object within a dictionary
def agent_to_agent(buyer_array,seller_array): 
    buyer_seller_dict = {}
    num_of_iterations = min(len(buyer_array),len(seller_array))
    max = num_of_iterations - 1
    
    cbuyer_array = buyer_array
    cseller_array = seller_array

    for i in range(num_of_iterations):
        random.shuffle(cbuyer_array)
        random.shuffle(cseller_array)
        pos = random.randint(0,max)
        buyer_seller_dict[cbuyer_array[pos]] = cseller_array[pos]
        cbuyer_array.pop(pos)
        cseller_array.pop(pos)
        max = max - 1  
    return buyer_seller_dict

#this disects the dictionary back into the prices of the buyers and sellers in numbers
def transaction(some_dictionary,increment, accurate_equilibrium, market_pressure):
    global local_buyer_prices 
    global local_seller_prices
    global number_of_trades_today
    global new_equilibrium_prices
    global trades_completed

    for buyer, seller in some_dictionary.items():
        trade_price = 0
        if buyer.local_price >= seller.local_price:
            trade_price = int((buyer.local_price + seller.local_price) / 2)
            number_of_trades_today += 1
            trades_completed += 1

            if market_pressure == "demand":
                # Demand > Supply
                buyer.local_price = max(seller.local_price, buyer.local_price - increment )
                seller.local_price = min(buyer.local_price, seller.local_price + increment )
            elif market_pressure == "supply":
                # Supply > Demand
                buyer.local_price = max(seller.local_price, buyer.local_price - increment * 2)
                seller.local_price = max(seller.minimum_price, seller.local_price - increment * 2)
            else:
                # Balanced market
                buyer.local_price = max(seller.local_price, buyer.local_price - increment // 2)
                seller.local_price = min(seller.minimum_price + increment, seller.local_price + increment // 2)
        else:
            # Trade failed
            if market_pressure == "demand":
                buyer.local_price = min(buyer.maximum_price, buyer.local_price + increment)
                seller.local_price = max(seller.minimum_price, seller.local_price - increment)
            elif market_pressure == "supply":
                buyer.local_price = max(seller.local_price, buyer.local_price - increment * 2)
                seller.local_price = max(seller.minimum_price, seller.local_price - increment * 2)
            else:
                buyer.local_price = buyer.local_price  
                seller.local_price = seller.local_price 

        trade_prices.append(trade_price)
        local_buyer_prices.append(buyer.local_price)
        local_seller_prices.append(seller.local_price)
    
    if number_of_trades_today != 0:
        print(trade_prices)
        new_equilibrium = int((sum(trade_prices) / number_of_trades_today))
        
    else:
        new_equilibrium = 0
    
    new_equilibrium_prices.append(new_equilibrium)

    if not accurate_equilibrium:
        print("Number of trades:",number_of_trades_today)
        print(*trade_prices)
        print(new_equilibrium)

    new_equilibrium_prices.append(new_equilibrium)

typing_index = 0
typing_speed = 1
def display_text(surface, text, pos, font, color, chars_shown):
    x, y = pos
    visible_text = text[:chars_shown]  # Show only part of text
    lines = []
    current_line = ""
    
    for word in visible_text.split(' '):
        test_line = current_line + word + ' '
        if font.size(test_line)[0] + x > 1860:
            lines.append(current_line)
            current_line = word + ' '
        else:
            current_line = test_line
    lines.append(current_line)

    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += font.get_height()

def sim_display(now):
    global typing_index
    if typing_index < len(greater_text[now]):
        typing_index += typing_speed
    if greater:
        screen.blit(moreBuyers_scaled,(1280,0))
        display_text(screen, greater_text[now], (1280,600), explanation_font, "black",typing_index)
    elif same:
        screen.blit(sameBuyers_scaled,(1280,0))
        display_text(screen, same_text[now], (1280,600), explanation_font, "black",typing_index)
    elif smaller:
        screen.blit(lessBuyers_scaled,(1280,0))
        display_text(screen, smaller_text[now], (1280,600), explanation_font, "black",typing_index)

def simulation(num_Of_Sellers, num_Of_Buyers,type_of_product):
    global menu
    global greater
    global same
    global smaller
    global number_of_trades_today
    global trades_completed
    global min_prices_sellers
    global max_prices_buyers
    global lower_price
    global upper_price
    global incremental_price
    global stall_seller_map
    global trade_prices
    global new_equilibrium_prices
    global local_buyer_prices
    global local_seller_prices
    global typing_index
    global initial_equilibrium_price
    global market_pressure
    lower_price = product_category(type_of_product)[0]
    upper_price = product_category(type_of_product)[1]
    incremental_price = product_category(type_of_product)[2]
    equilibrium_price = price_equilibrium(lower_price,upper_price)
    initial_equilibrium_price = equilibrium_price
    typing_index = 0
    trade_prices = []
    number_of_trades_today = 0
    local_buyer_prices = []
    local_seller_prices = []
    simulation_done = False
    trades_completed = 0
    greater = False
    same = False
    smaller = False
    finish = False
    now = 0
    seagull_start_x = 0
    seagull_surface = pygame.image.load("images/seagull.png")
    seagull_surface_scaled_right = pygame.transform.scale(seagull_surface,(75,75))
    seagull_rect = seagull_surface_scaled_right.get_rect(bottomleft = (seagull_start_x, 500))
    seagull_surface_scaled_left = pygame.transform.flip(seagull_surface_scaled_right, True, False)
    seagull_returning = True
    if num_Of_Buyers > num_Of_Sellers:
        greater = True
        market_pressure = "demand"
    elif num_Of_Buyers == num_Of_Sellers:
        same = True
        market_pressure = "equal"
    elif num_Of_Buyers < num_Of_Sellers:
        smaller = True
        market_pressure = "supply"

    new_equilibrium_prices = [0]

    eq_scaled_agents = accurate_equilibrium(num_Of_Buyers,num_Of_Sellers)
    if num_Of_Buyers > num_Of_Sellers:
        buyer_bias = int(equilibrium_price * 0.1)  # increase buyer price floor
        new_lower = min(equilibrium_price + buyer_bias, upper_price)
        max_prices_buyers = [random.randint(new_lower, upper_price) for _ in range(eq_scaled_agents[0])]
    else:
        max_prices_buyers = price_setter(1, eq_scaled_agents[0], lower_price, upper_price, equilibrium_price)
    min_prices_sellers = price_setter(2,eq_scaled_agents[1],lower_price,upper_price,equilibrium_price)
    
    local_buyer_prices = []
    local_seller_prices = []

    sellers = price_to_agent(2, min_prices_sellers, local_seller_prices)
    stall_seller_map = {i: sellers[i] for i in range(num_Of_Sellers)}

    buyers = []
    for i in range(num_Of_Buyers):
        buyers.append(Buyer(stall_rect[:num_Of_Sellers], 1120, 815, 10, max_prices_buyers[i], max_prices_buyers[i],stall_seller_map))
    
    while True:
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
        screen.blit(cloud_surface_scaled, (500,400))
        

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
        
        trades_completed_text = trades_font.render(("Trades Completed: " + str(trades_completed)),True, "brown")
        trades_completed_text_rect = trades_completed_text.get_rect(bottomright=(1150,50))
        
        eq_price_text = trades_font.render("Current Equilibrium Price: "+ str(new_equilibrium_prices[-1]),True,"brown")
        eq_price_text_rect = eq_price_text.get_rect(bottomright = (1150,100))

        price_change = new_equilibrium_prices[-1] - initial_equilibrium_price
        price_change_text = trades_font.render("Price Change: " + str(price_change), True, "brown")
        price_change_rect = price_change_text.get_rect(bottomright=(1150, 150))

        screen.blit(price_change_text, price_change_rect)

        screen.blit(trades_completed_text,trades_completed_text_rect)
        screen.blit(eq_price_text,eq_price_text_rect)

        menu_button = Button(
            image= pygame.image.load("images/quit.png"), pos=(135, 50), text_input="Menu",
            font=button_font, base_color="#fcf935", hovering_color="white"
        )
        for button in [menu_button]:
            button.changeColor(mouse)
            button.update(screen)
        
        if now == len(greater_text)-1 or same==True: 
            finish = True
            finish_button = Button(
                image= None, pos=(1570, 950), text_input="Finish",
                font=button_font, base_color="dark red", hovering_color= "red"
            )
            for button in [finish_button]:
                button.changeColor(mouse)
                button.update(screen)

        elif now != len(greater_text)-1:
            next_button = Button(
                image= None, pos=(1570, 950), text_input="next",
                font=button_font, base_color="Dark blue", hovering_color= "blue"
            )
            for button in [next_button]:
                button.changeColor(mouse)
                button.update(screen)
            
        sim_display(now)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mouse):
                    menu = True
                    main_menu()
                if finish == True:
                    if finish_button.checkForInput(mouse):
                        typing_index = 0
                        menu = True
                        main_menu()
                else: 
                    if next_button.checkForInput(mouse):
                        typing_index = 0
                        now+=1
        pygame.display.update()
        clock.tick(30)

def main_menu():
    pygame.display.set_caption("menu")
    global num_Of_Buyers
    global num_Of_Sellers
    global menu
    
    while menu:
        screen.fill("black")
        screen.blit(bg_scaled,(0,0))

        mouse = pygame.mouse.get_pos()

        buyer_text = bs_font.render("Buyers",True, (128, 0, 128))
        buyer_rect = buyer_text.get_rect(center=(710,600))
        screen.blit(buyer_text, buyer_rect)

        seller_text = bs_font.render("Sellers",True, "Yellow")
        seller_rect = seller_text.get_rect(center=(1210,600))
        screen.blit(seller_text, seller_rect)

        menu_text = title_font.render("Main Menu",True, "White")
        menu_rect = menu_text.get_rect(center=(960,125))

        product_text = product_font.render("1) iPads 2) Cars 3) Toys 4) Jackets",True, "light blue")
        product_rect = product_text.get_rect(center=(960,300))


        start_button = Button(image=pygame.image.load("images/start.png"),pos=(710,900)
                             ,text_input="START",font = button_font,base_color = "Green", hovering_color = "white")

        quit_button = Button(image=pygame.image.load("images/quit.png"),pos=(1210,900)
                             ,text_input="QUIT",font = button_font,base_color = "red", hovering_color = "white")
        
        screen.blit(product_text,product_rect)
        screen.blit(menu_text, menu_rect)
        
        for button in [start_button,quit_button]:
            button.changeColor(mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            buyer_slider.handle_event(event)
            seller_slider.handle_event(event)
            product.handle_event(event)
            type_of_product = product.get_value()
            num_Of_Buyers = buyer_slider.get_value()
            num_Of_Sellers = seller_slider.get_value()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse):
                    menu = False
                    simulation(num_Of_Sellers,num_Of_Buyers,type_of_product)
                if quit_button.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        buyer_slider.draw(screen)
        seller_slider.draw(screen)
        product.draw(screen)
        pygame.display.update()
        clock.tick(30)

main_menu()

