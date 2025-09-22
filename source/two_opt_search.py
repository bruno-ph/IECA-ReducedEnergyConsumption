from eval import EvalElecSingle

import numpy as np
def TwoOptSwap(route,v1,v2):
    new_route= np.array(route[0:v1])
    new_route= np.concatenate(new_route,route[v1+1:v2])
    new_route = np.concatenate(new_route,route[v2:])
    return new_route

def TwoOptSearch(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate):
    best_cost = EvalElecSingle(route,distances,speed, load_cap, all_coors,load_unit_cost,cons_rate)
    n=len(route)
    should_continue = False
    while (should_continue):
        should_continue=False
        for i in range (0,n):
            for j in range(1,n):
                new_route=TwoOptSwap(route,i,j)
                new_cost=EvalElecSingle(new_route)
                if (new_cost < best_cost + 0.000001): #potentially add check for time windows
                    best_cost=new_cost
                    route=new_route
                    should_continue=True
    return route
