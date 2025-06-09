import matplotlib.pyplot as plt
import numpy as np
import random

class Buyers:
    def __init__(self, demand_intercept, demand_slope):
        self.demand_intercept = demand_intercept #price when quantity is 0
        self.demand_slope = demand_slope    #how much the price decreases per quantity

    def demand_price(self,quantity):
        return self.demand_intercept - (self.demand_slope * quantity) 
        
    def demand_points(self):
        
        quantities = np.arange(0,151,5) #finds the price for a given quantity (points on a graph)
        return quantities , self.demand_price(quantities)


class Sellers:
    def __init__(self, supply_intercept, supply_slope):
        self.supply_intercept = supply_intercept #price when quantity is 0
        self.supply_slope = supply_slope    #how much the price increases per quantity
        
    def supply_price(self,quantity):
        return self.supply_intercept + (self.supply_slope * quantity)
    
    def supply_points(self):
        quantities = np.arange(0,151,5) #finds the price for a given quantity (points on a graph)
        return quantities , self.supply_price(quantities)
         

def find_equilibrium(Buyers, Sellers):
    quantity = (Buyers.demand_intercept - Sellers.supply_intercept) / (Buyers.demand_slope + Sellers.supply_slope) 
    price = Buyers.demand_price(quantity)   #uses equilibrium quantity to find equilibrium price
    return quantity,price

q1 = random.randint(40,120)
p1 = random.uniform(0.5,1.0)
print("q1: ",q1,"p1: ",p1)
q2 = random.randint(10,30)
p2 = random.uniform(0.1,0.5)
print("q2: ",q2,"p2: ",p2)
buyers = Buyers(q1,p1)
sellers = Sellers(q2,p2)

eq_qty, eq_price = find_equilibrium(buyers,sellers)
demand_qty, demand_price = buyers.demand_points()
supply_qty, supply_price = sellers.supply_points()
plt.plot(demand_qty,demand_price)
plt.plot(supply_qty,supply_price,':')
plt.plot(eq_qty,eq_price,'o')
plt.xlim(0,150)
plt.ylim(0,150)
plt.xlabel("Quantity")
plt.ylabel("Price")
plt.title("Supply and Demand")
plt.show()
