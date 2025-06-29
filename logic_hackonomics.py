from pygame_functions import *
import random

class Buyer:
    def __init__(self,maximum_price,local_price):
        self.maximum_price = maximum_price
        self.local_price = local_price
        self.traded = False

class Seller:
    def __init__(self,minimum_price,local_price):
        self.minimum_price = minimum_price
        self.local_price = local_price
        self.traded = False

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
            buyer_array.append(Buyer(price,price))
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
    #these are the copies of the respective arrays so original isn't overwritten
    cbuyer_array = buyer_array
    cseller_array = seller_array

    for i in range(num_of_iterations):
        pos = random.randint(0,max)
        buyer_seller_dict[cbuyer_array[pos]] = cseller_array[pos]
        cbuyer_array.pop(pos)
        cseller_array.pop(pos)
        max = max - 1
        random.shuffle(cbuyer_array)
        random.shuffle(cseller_array)

    
    return buyer_seller_dict



#this disects the dictionary back into the prices of the buyers and sellers in numbers
def transaction(some_dictionary,increment):
    global local_buyer_prices 
    global local_seller_prices
    local_buyer_prices = []
    local_seller_prices = []
    trade_prices = []
    number_of_trades_today = 0

    for buyer, seller in some_dictionary.items():

        if buyer.local_price >= seller.local_price: #condition for a trade occuring
            trade_price = int((buyer.local_price + seller.local_price) / 2) #transact in the middle
            number_of_trades_today += 1
            buyer.local_price = min(buyer.maximum_price, buyer.local_price - increment)
            seller.local_price = max(seller.minimum_price, seller.local_price + increment)
        else:
            trade_price = 0
            buyer.local_price = min(buyer.maximum_price, buyer.local_price + increment)
            seller.local_price = max(seller.minimum_price, seller.local_price - increment)
        
        trade_prices.append(trade_price)
        local_buyer_prices.append(buyer.local_price)
        local_seller_prices.append(seller.local_price)
        
    print("Number of trades:",number_of_trades_today)
    
    if number_of_trades_today != 0:
        new_equilibrium = int((sum(trade_prices) / number_of_trades_today))
    else:
        new_equilibrium = 0
    print(*trade_prices)
    print(new_equilibrium)
    new_equilibrium_prices.append(new_equilibrium)

num_of_buyers = int(input("How many buyers are there: "))
num_of_sellers = int(input("How many sellers are there: "))

if (num_of_buyers or num_of_sellers) > 10 or (num_of_buyers or num_of_sellers) <= 0:
    print("Error")
type_of_product = int(input("Would you like to buy \n 1) iPads \n 2) Cars \n 3) Toys \n 4) Jackets "))
lower_price = product_category(type_of_product)[0]
upper_price = product_category(type_of_product)[1]
incremental_price = product_category(type_of_product)[2]

#the arrays containing the random maximum/minimum prices: THIS WORKS
equilibrium_price = price_equilibrium(lower_price,upper_price)


max_prices_buyers = price_setter(1,num_of_buyers,lower_price,upper_price,equilibrium_price)
min_prices_sellers = price_setter(2,num_of_sellers,lower_price,upper_price,equilibrium_price)
print(*max_prices_buyers)
print(*min_prices_sellers)
print(equilibrium_price)

days_of_trade = 0
new_equilibrium_prices = []

#initial arrays of buyer and seller objects with maximum and minimum prices assigned

local_buyer_prices = []
local_seller_prices = []
while days_of_trade < 20:
    buyer_objects = price_to_agent(1,max_prices_buyers,local_buyer_prices)
    seller_objects = price_to_agent(2,min_prices_sellers,local_seller_prices)
    buyer_seller_dictionary = agent_to_agent(buyer_objects,seller_objects)
    days_of_trade += 1
    print()
    print(f"Day {days_of_trade}")
    print()
    transaction(buyer_seller_dictionary,incremental_price)

while 0 in new_equilibrium_prices: 
    new_equilibrium_prices.remove(0)

print(*new_equilibrium_prices)

########################### The following simulates an accurate equilibrium #################################################
eq_scaled_agents = accurate_equilibrium(num_of_buyers,num_of_sellers)

max_prices_buyers = price_setter(1,num_of_buyers,lower_price,upper_price,equilibrium_price)
min_prices_sellers = price_setter(2,num_of_sellers,lower_price,upper_price,equilibrium_price)

days_of_trade = 0
new_equilibrium_prices = []

local_buyer_prices = []
local_seller_prices = []
while days_of_trade < 20:
    buyer_objects = price_to_agent(1,max_prices_buyers,local_buyer_prices)
    seller_objects = price_to_agent(2,min_prices_sellers,local_seller_prices)
    buyer_seller_dictionary = agent_to_agent(buyer_objects,seller_objects)
    days_of_trade += 1
    transaction(buyer_seller_dictionary,incremental_price)

while 0 in new_equilibrium_prices: 
    new_equilibrium_prices.remove(0)

new_equilibrium = new_equilibrium_prices[-1]
print(f"Accurate equilibrium: {new_equilibrium}")


