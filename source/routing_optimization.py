import numpy as np
from random import randint, uniform
from math import pow
def RouletteWheelSelection(nodes,origin, distances, alpha, beta, pheromone_matrix):
    f = lambda x: max((min(pow(pheromone_matrix[origin][x], alpha) / max(pow(distances[origin][x], beta),1e-8),1e15)),1e-8)
    chances = list(map(f,nodes))

    #print(chances)
    sum_chances = sum(chances)
    curr_sum=0.0
    random_value= uniform(0.0,sum_chances)
    for i, chance in enumerate(chances):
        cumm_chance = chance+curr_sum
        if random_value<=cumm_chance:
            return nodes[i]
        curr_sum+=chance
    raise Exception







def RoutingOptimization(vertex_count, depots_count,customers_count,recharges_count, pheromone_matrix, population_size, alpha, beta, distances):
    routes = []
    for k in range(population_size):
        remaining_uses= np.ones(vertex_count)
        remaining_uses[depots_count:recharges_count] = 2  * customers_count
        route = []
        possible_next=np.where(remaining_uses>0)[0]
        current = possible_next[randint(0, len(possible_next)-1)]
        route.append(current)
        remaining_uses[current]-=1
        remaining_positions =np.where(remaining_uses>0)[0]
        while (len(remaining_positions)>0):

            current= RouletteWheelSelection(np.delete(remaining_positions,np.argwhere(remaining_positions==current)),current, distances, alpha, beta, pheromone_matrix)
            #IMPORTANT, CHECK IF ROULETE RETURNS INDEX IN REMAINING_POS OR OVERALL NUMBER (CURRENT SHOULD BE OVERALL NUMBER)
            route.append(current)
            remaining_uses[current]-=1
            if len(remaining_positions<=depots_count+recharges_count) and max(remaining_positions)<=(depots_count+recharges_count):
                break
            remaining_positions =np.where(remaining_uses>0)[0]
        if (route[0]>=depots_count):
            route.randint(0,depots_count-1)
        
        print ("Route = ",route)
        split_route= Split(route)
        routes.append(route)


            



