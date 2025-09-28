from eval import EvalElecSingle, RouteValid

import numpy as np
def TwoOptSwap(route,v1,v2):
    new_route= np.array(route[0:v1])
    new_route= np.concatenate(new_route,route[v1+1:v2])
    new_route = np.concatenate(new_route,route[v2:])
    return new_route

def TwoOptSearch(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
    best_cost = EvalElecSingle(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate)
    n=len(route)
    should_continue = False
    while (should_continue):
        should_continue=False
        for i in range (0,n):
            for j in range(1,n):
                new_route=TwoOptSwap(route,i,j)
                new_cost=EvalElecSingle(new_route)
                if (new_cost < best_cost + 0.000001):
                    route_valid = RouteValid(route, distances, speed, all_coors, load_cap, load_unit_cost, fuel_cap, cons_rate, refuel_rate,depots_count,rechargers_count)
                    new_route_valid=RouteValid(new_route)
                    if (not(route_valid and not new_route_valid)): 
                        best_cost=new_cost
                        route=new_route
                        should_continue=True
                        route_valid= new_route_valid
    return route
