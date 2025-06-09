class Buyers:
    def __init__(self, demand_intercept, demand_slope):
        self.demand_intercept = demand_intercept #price when quantity is 0
        self.demand_slope = demand_slope    #how much the price decreases per quantity

    def demand_price(self,quantity):
        return self.demand_intercept - (self.demand_slope * quantity) 
        
    def demand_points(self):
        
        tuple = [(qty,self.demand_price(qty))for qty in range(0,101,5)] #finds the price for a given quantity (points on a graph)
        return tuple


class Sellers:
    def __init__(self, supply_intercept, supply_slope):
        self.supply_intercept = supply_intercept #price when quantity is 0
        self.supply_slope = supply_slope    #how much the price increases per quantity
        
    def supply_price(self,quantity):
        return self.supply_intercept + (self.supply_slope * quantity)
    
    def supply_points(self):
        tuple = [(qty,self.supply_price(qty))for qty in range(0,101,5)]
        return tuple
         

def find_equilibrium(Buyers, Sellers):
    quantity = (Buyers.demand_intercept - Sellers.supply_intercept) / (Buyers.demand_slope + Sellers.supply_slope) 
    price = Buyers.demand_price(quantity)   #uses equilibrium quantity to find equilibrium price
    return quantity,price
