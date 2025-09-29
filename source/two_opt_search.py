from eval import EvalElecSingle, RouteValid

import numpy as np
def TwoOptSwap(route,v1,v2):
    new_route = route[:v1+1]
    new_route = new_route + route[v2:v1:-1]
    new_route = new_route + route[v2+1:]
    return new_route

def TwoOptSearch(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
    best_cost = EvalElecSingle(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate)
    n=len(route)
    should_continue = True
    route_valid = RouteValid(route, distances, speed, all_coors, load_cap, load_unit_cost, fuel_cap, cons_rate, refuel_rate,depots_count,rechargers_count)
    while (should_continue):
        should_continue=False
        for i in range (0,n):
            for j in range(i+2,n):
                new_route=TwoOptSwap(route,i,j)
                new_cost=EvalElecSingle(new_route,distances,speed,load_cap,all_coors,load_unit_cost,cons_rate)
                if (new_cost < best_cost - 0.000001):
                    new_route_valid=RouteValid(new_route,distances,speed,all_coors,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)
                    if (not(route_valid and not new_route_valid)): 
                        best_cost=new_cost
                        route=new_route
                        should_continue=True
                        route_valid= new_route_valid
    return route
