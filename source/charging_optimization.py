import numpy as np
from math import ceil
def ChargingOptimization(charging_population,routing_ant_charging_scheme):
    cust_size= len(charging_population[0])
    pop_size = len(charging_population)
    offspring_size = int(ceil(pop_size/2))
    routing_ant_bool = np.tile(routing_ant_charging_scheme.astype(bool),(offspring_size,1)) 
    parent_population1 = charging_population[0:offspring_size].astype(bool)
    parent_population2 = charging_population[int(pop_size/2):].astype(bool)
    offspring = np.zeros((pop_size,cust_size))
    randomization_mask = np.random.choice([True,False],size= (offspring_size,cust_size))
    offspring = (parent_population1 | routing_ant_bool)
    offspring[randomization_mask]= parent_population2[randomization_mask]
    bitflip_mask = np.random.choice([True,False],size= (offspring_size,cust_size), p =(1/cust_size,1-(1/cust_size)))
    offspring= offspring ^ bitflip_mask
    return offspring