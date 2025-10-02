import numpy as np
from random import sample, choice
from math import ceil
from binary_population import BinaryPopulation

def TournamentSelection(k,number_tourneys,fitness1,fitness2):
    chosen_solution = np.zeros(number_tourneys)
    size = len(fitness1)
    for ni in range(number_tourneys):
        selected = sample(range(size),k)
        sel_fitness = [fitness1[s] for s in selected]
        if (sel_fitness[min(sel_fitness)]>1):
            sel_fitness = [fitness2[s] for s in selected]
            winner = selected[np.where(sel_fitness == min(sel_fitness))[0]]
        else:
            winner = selected[np.where(sel_fitness == min(sel_fitness))[0]]
        chosen_solution[ni] = winner



def ChargingOptimization(charging_population,routing_ant_charging_scheme):
    cust_size= len(charging_population[0])
    pop_size = len(charging_population)
    offspring_size = len(charging_population)/2
    routing_ant_bool = np.tile(routing_ant_charging_scheme.astype(bool),(offspring_size,1)) 
    parent_population1 = [c.mask for c in charging_population[:offspring_size]].astype(bool)
    parent_population2 = [c.mask for c in charging_population[offspring_size+1:]].astype(bool)
    offspring = np.zeros((pop_size,cust_size))
    randomization_mask = np.random.choice([True,False],size= (offspring_size,cust_size))
    offspring = (parent_population1 & routing_ant_bool)
    offspring[randomization_mask]= parent_population2[randomization_mask]
    bitflip_mask = np.random.choice([True,False],size= (offspring_size,cust_size), p =(1/cust_size,1-(1/cust_size)))
    offspring= offspring ^ bitflip_mask
    offspring_pop = []
    for child_mask in offspring:
        offspring_pop.append(BinaryPopulation(child_mask, 1e15,1e15))
    return offspring