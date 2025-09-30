import numpy as np
from random import randint, uniform, choices
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

def Split(original_route,demand, ready_time,service_time,due_time,distances,cargo_size,cost_limit, speed, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
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
        elapsed_time = 0.0
        battery = fuel_cap #assumes best case with no load, just to filter out worst cases
        # delivered_units_per_station=[]
        while (j<n and cost<=cost_limit and load<=cargo_size):
            load+=demand[original_route[j]]
            elapsed_time+=service_time[original_route[j]]
            if (i==j):
                cost = distances[first_node][original_route[j]]*2
                elapsed_time += distances[first_node][original_route[j]]/speed
                battery -=  distances[first_node][original_route[j]] * cons_rate
            else:
                cost = cost - distances[first_node][original_route[j-1]] + distances[original_route[j-1]][original_route[j]] + distances[first_node][original_route[j]]
                elapsed_time+= distances[original_route[j-1]][original_route[j]]/speed
                battery -=  distances[original_route[j-1]][original_route[j]] * cons_rate
            if (j>=depots_count and j<depots_count+rechargers_count):
                elapsed_time+= (fuel_cap-battery)*refuel_rate

            if (load<=cargo_size and cost<=cost_limit):
                if (v[i-1]+cost < v[j] and elapsed_time<=due_time[original_route[j]]+service_time[original_route[j]]):
                    v[j]=v[i-1]+cost
                    p[j]=i-1
                j+=1

    trips = []
    j=n-1
    i = j
    while (i>=1):
        trip=[first_node]
        i = p[j]
        for k in range (i+1,j+1):
            trip.append(original_route[k])
        trip.append(first_node)
        #trip = TwoOptSearch(trip,distances,speed, cargo_size, demand,ready_time, service_time,due_time, load_unit_cost,cons_rate, fuel_cap, refuel_rate,depots_count,rechargers_count )
        trips.append(trip)
        j=i
    return trips
    #print ("Trips:" ,trips)
    

    

def RoutingOptimization(vertex_count, depots_count,customers_count,rechargers_count, pheromone_matrix, population_size, alpha, beta, distances, demand,ready_time, service_time,due_time, load_cap, speed,load_unit_cost,cons_rate,fuel_cap,refuel_rate):
    best_ant_route = []
    best_ant_cost= 1e15
    # best_ant_viable = False
    for k in range(population_size):
        was_visited= np.zeros(vertex_count)
        route = []
        current = randint(0,vertex_count-1)
        route.append(current)
        was_visited[current]=1
        #remaining_positions =np.where(was_visited==0) #[0]here too
        while (len(np.where(was_visited[depots_count+rechargers_count:]==0)[0])>0 or was_visited[0]==0):
            possible_next = np.where(was_visited==0)[0]
            probabilities = [pow(pheromone_matrix[current][int(pn)], alpha) / max(pow(distances[current][int(pn)], beta),1) for pn in possible_next]
            next = choices(possible_next,weights=probabilities)[0]
            if (next==current):
                if (current>=vertex_count):
                    next-=1
                else:
                    next+=1
            current=next
            #current= RouletteWheelSelection(np.delete(remaining_positions,np.argwhere(remaining_positions==current)),current, distances, alpha, beta, pheromone_matrix)
            route.append(current)
            was_visited[current]=1
            if (current>depots_count+rechargers_count):
                was_visited[depots_count:depots_count+rechargers_count]=0
        if (route[0]>=depots_count):
            index0 = route.index(0)
            route = route[index0:] + route[:index0]
        
        
        
        split_route= Split(route,demand,ready_time, service_time,due_time,distances,load_cap,1e15, speed, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count)
        split_route_cost = EvalElecMulti(split_route,distances, speed, load_cap, demand,load_unit_cost, cons_rate)
        if (split_route_cost<best_ant_cost):
                best_ant_cost = split_route_cost
                best_ant_route = split_route
        # if (best_ant_viable):
        #     if (split_route_cost<best_ant_cost and IsViable(split_route,distances,speed,all_coors,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)):
        #         best_ant_cost = split_route_cost
        #         best_ant_route = split_route
        # else:
        #     if (split_route_cost<best_ant_cost):
        #         best_ant_cost = split_route_cost
        #         best_ant_route = split_route
        #         best_ant_viable = IsViable(split_route,distances,speed,all_coors,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)
    best_ant_charging_scheme  = GetAntChargingScheme(best_ant_route,customers_count,depots_count,rechargers_count)
    return (best_ant_route,best_ant_cost,best_ant_charging_scheme)


            



