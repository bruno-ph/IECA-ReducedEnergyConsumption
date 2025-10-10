import numpy as np
from random import randint, choices
from math import pow
from eval import EvalElecMulti

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



def Split(original_route,demand, ready_time,service_time,due_time,distances,cargo_size,cost_limit, speed, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
    np.fill_diagonal(distances,0)
    n = len(original_route)
    first_node = original_route[0]
    load = 0
    elapsed_time = 0.0
    battery = fuel_cap #assumes best case with no load, just to filter out worst cases
    trip = [first_node]
    trips=[]
    inserted_cust = 0
    for i in range(1,n): #take each note as route start
        node = original_route[i]
        load+=demand[node]
        elapsed_time+=distances[original_route[i-1]][node]/speed
        battery -=  distances[original_route[i-1]][node] * cons_rate
        if (battery<0 or (elapsed_time>due_time[node] and node>=depots_count+rechargers_count) or load>cargo_size or (node==first_node)):
            if (inserted_cust > 0):
                trip.append(first_node)
                trips.append(trip)
            load = demand[node]
            elapsed_time =distances[first_node][node]/speed
            battery = fuel_cap - distances[first_node][node] * cons_rate
            inserted_cust = 0
            if (node!=first_node):
                trip = [first_node]
            else:
                trip = []
        trip.append(node)
        elapsed_time += service_time[node]
        if (node>=depots_count+rechargers_count):
            elapsed_time = max(elapsed_time,due_time[node] + service_time[node])
            inserted_cust+=1
        elif (depots_count<=node and node<depots_count+rechargers_count):
            elapsed_time+= (fuel_cap-battery)*refuel_rate
    if trip:
        if (inserted_cust>0):
            trip.append(first_node)
            trips.append(trip)
    return trips
    

    

def RoutingOptimization(vertex_count, depots_count,customers_count,rechargers_count, pheromone_matrix, population_size, alpha, beta, distances, demand,ready_time, service_time,due_time, load_cap, speed,load_unit_cost,cons_rate,fuel_cap,refuel_rate):
    best_ant_route = []
    best_ant_cost= 1e15
    for k in range(population_size):
        was_visited= np.zeros(vertex_count)
        route = []
        current = randint(0,vertex_count-1)
        route.append(current)
        was_visited[current]=1
        should_continue = True
        while (should_continue):
            should_continue = (len(np.where(was_visited[depots_count+rechargers_count:]==0)[0])>0 or was_visited[0]==0)
            possible_next = np.where(was_visited==0)[0]
            if (len(possible_next)==0):
                break
            probabilities = [pow(pheromone_matrix[current][int(pn)], alpha) / max(pow(distances[current][int(pn)], beta),1) for pn in possible_next]
            next = choices(possible_next,weights=probabilities)[0]
            if (next==current):
                if (current>=vertex_count):
                    next-=1
                else:
                    next+=1
            current=next
            route.append(current)
            was_visited[current]=1
            if (current>depots_count+rechargers_count):
                was_visited[:depots_count+rechargers_count]=0
        if (route[0]>=depots_count):
            index0 = route.index(0)
            route = route[index0:] + route[:index0]
        
        split_route= Split(route,demand,ready_time, service_time,due_time,distances,load_cap,1e15, speed, load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count)
        split_route_cost = EvalElecMulti(split_route,distances, speed, load_cap, demand,load_unit_cost, cons_rate)
        if (split_route_cost<best_ant_cost):
                best_ant_cost = split_route_cost
                best_ant_route = split_route
    best_ant_charging_scheme  = GetAntChargingScheme(best_ant_route,customers_count,depots_count,rechargers_count)
    return (best_ant_route,best_ant_cost,best_ant_charging_scheme)


            



