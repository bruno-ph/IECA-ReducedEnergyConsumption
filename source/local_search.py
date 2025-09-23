import numpy as np
from eval import IsRoutePossible

def FindSearchZone(vehicle_route):
    pass

def LocalSearch(best_solution,depots_count,rechargers_count):
    mask = (best_solution>=depots_count and best_solution<depots_count+rechargers_count)
    custom_solution=[route[mask[i]] for i,route in enumerate(best_solution)]
    for vehicle_route in custom_solution:
        iterations = 0
        while (not IsRoutePossible(vehicle_route)):
            if (iterations>=len(vehicle_route)-1):
                return [[],1e15]
            search_zone,remaining_charges,carrying_loads = FindSearchZone(vehicle_route)
            insertable_stations=[]
            insertable_stations_costs=[]
            for candidate_customer in search_zone:
                range_stations = []
                range_stations_cost=[]





            

        


# delete all charging stations in all routes
# while not all routes are feasible:
#     for each vehicle_route:
#         calculate if some node is infeasible eletrically
#         if infeasible: #limit iterations maybe
#             create a search zone:
#                 find first point where electricity is negative
#                 search zoneLk = all customers between the point before elec is negative and the last preceding station
#                 for node v in Lk:
#                     Jv_k=stations reacheable from v, with allocation and construction cost????
#                     remove already visited stations(in this route) from Jv_k (maybe)
#                     If v cant reach any station (empty JVK) its deleted from Lk
#                 Rank each node in Lk based on the total cost
#                 Randomly select one of the nodes in Lk based on the rank
#                 Rank selected node's stations based on cost
#                 Index that station
                    
                    
                    
# apply local search