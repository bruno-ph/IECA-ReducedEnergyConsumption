import numpy as np
class BinaryPopulation:
    def __init__(self,mask,cost,cons):
        self.mask = mask
        self.cost = cost
        self.cons = cons

def CalculateCost(mask,distances,depots_count,rechargers_count,load_cap,cons_rate,unit_weight):
    cost = 0
    for bi,bit in enumerate(mask):
        if bit:
            dist= min(distances[depots_count+bi][depots_count:depots_count+rechargers_count])
            cost +=((1.0 + load_cap * unit_weight)*dist) * cons_rate
    return cost