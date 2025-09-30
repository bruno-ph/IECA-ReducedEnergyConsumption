from eval import EvalElecSingle, RouteValid

import numpy as np
def TwoOptSwap(route,v1,v2):
    new_route = route[:v1+1]
    new_route = new_route + route[v2:v1:-1]
    new_route = new_route + route[v2+1:]
    return new_route


def TwoOptSearch(route,distances,speed, load_cap, demand,ready_time, service_time,due_time,load_unit_cost,cons_rate,fuel_cap, refuel_rate,depots_count,rechargers_count):
    best_cost = EvalElecSingle(route,distances,speed, load_cap, demand,load_unit_cost,cons_rate)
    n=len(route)
    should_continue = True
    route_valid = RouteValid(route, distances, speed, demand,ready_time, service_time,due_time, load_cap, load_unit_cost, fuel_cap, cons_rate, refuel_rate,depots_count,rechargers_count)
    while (should_continue):
        should_continue=False
        for i in range (1,n-1):
            for j in range(i+2,n-1):
                if (i<depots_count+rechargers_count or j<depots_count+rechargers_count):
                    continue
                new_route=TwoOptSwap(route,i,j)
                new_cost=EvalElecSingle(new_route,distances,speed,load_cap,demand,load_unit_cost,cons_rate)
                if (new_cost < best_cost - 0.000001):
                    new_route_valid=RouteValid(new_route,distances,speed,demand,ready_time, service_time,due_time,load_cap,load_unit_cost,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)
                    if (not(route_valid and not new_route_valid)): 
                        best_cost=new_cost
                        route=new_route
                        should_continue=True
                        route_valid= new_route_valid
    return route
