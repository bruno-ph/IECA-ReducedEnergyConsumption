import numpy as np
from random import randint, uniform
from math import pow
from two_opt_search import TwoOptSearch
from eval import EvalElecMulti, IsViable

def GetAntChargingScheme(best_ant_route,customers_count,depots_count,recharges_count):
    charge_mask = np.zeros(customers_count)
    min_customer = depots_count+recharges_count
    for route in best_ant_route:
        last_customer = -1
        for coordinate in route:
            if (coordinate>=min_customer):
                last_customer=coordinate
            elif (coordinate>=depots_count and last_customer!=-1):
                charge_mask[last_customer-min_customer]=1
    return charge_mask



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

def Split(original_route,vertices,distances,cargo_size,cost_limit, speed, all_coors, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
    np.fill_diagonal(distances,0)
    n = len(original_route)
    p = np.full(n,original_route[0]) #Predecessor Node
    #print("P is",p)
    v= np.full(n,1e15) #Minimum cost in some route
    v[0] = 0
    first_node = original_route[0]
    for i in range(1,n):
        load = 0
        cost = 0
        j=i
        while (j<n and cost<=cost_limit and load<=cargo_size):
            load+=vertices[original_route[j]].demand
            if (i==j):
                cost = distances[first_node][original_route[j]]*2
            else:
                cost = cost - distances[first_node][original_route[j-1]] + distances[original_route[j-1]][original_route[j]] + distances[first_node][original_route[j]]
            if (load<=cargo_size and cost<=cost_limit):
                if (v[i-1]+cost < v[j]):
                    v[j]=v[i-1]+cost
                    p[j]=i-1
                j+=1

    trips = []
    j=n-1
    while (i>=1):
        trip=[first_node]
        i = p[j]
        for k in range (i+1,j+1):
            trip.append(original_route[k])
        trip = TwoOptSearch(trip,distances,speed, cargo_size, all_coors, load_unit_cost,cons_rate, fuel_cap, refuel_rate,depots_count,rechargers_count )
        trips.append(trip)
        j=i
    return trips
    #print ("Trips:" ,trips)
    

    

def RoutingOptimization(vertex_count, depots_count,customers_count,rechargers_count, pheromone_matrix, population_size, alpha, beta, distances, all_coors, load_cap, speed,load_unit_cost,cons_rate,fuel_cap,refuel_rate):
    best_ant_route = []
    best_ant_cost= 1e15
    best_ant_viable = False
    for k in range(population_size):
        remaining_uses= np.ones(vertex_count)
        remaining_uses[depots_count:rechargers_count] = 2  * customers_count
        route = []
        possible_next=np.where(remaining_uses>0)[0]
        current = possible_next[randint(0, len(possible_next)-1)]
        route.append(current)
        remaining_uses[current]-=1
        remaining_positions =np.where(remaining_uses>0)[0]
        while (len(remaining_positions)>0):

            current= RouletteWheelSelection(np.delete(remaining_positions,np.argwhere(remaining_positions==current)),current, distances, alpha, beta, pheromone_matrix)
            route.append(current)
            remaining_uses[current]-=1
            if len(remaining_positions<=depots_count+rechargers_count) and max(remaining_positions)<(depots_count+rechargers_count):
                break
            remaining_positions =np.where(remaining_uses>0)[0]
        if (route[0]>=depots_count):
            route.insert(0,0)
        
        #print ("Route = ",route)
        split_route= Split(route,all_coors,distances,load_cap,1e15, speed, all_coors, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count)
        split_route_cost = EvalElecMulti(split_route,distances, speed, load_cap, all_coors,load_unit_cost, cons_rate)
        if (best_ant_viable):
            if (split_route_cost<best_ant_cost and IsViable(split_route,distances,speed,all_coors,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)):
                best_ant_cost = split_route_cost
                best_ant_route = split_route
        else:
            if (split_route_cost<best_ant_cost):
                best_ant_cost = split_route_cost
                best_ant_route = split_route
                best_ant_viable = IsViable(split_route,distances,speed,all_coors,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)
    #get best ant charging scheme
    best_ant_charging_scheme  = GetAntChargingScheme(best_ant_route,customers_count,depots_count,rechargers_count)
    return (best_ant_route,best_ant_cost,best_ant_charging_scheme)
        #print(routes)


            



