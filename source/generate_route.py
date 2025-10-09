import numpy as np
from eval import *

#Combines Routing Ant and Charging Scheme into a set of vehicle routes
def GenerateRoute(combined_route,charging_scheme,depots_count,rechargers_count,distances):
    cust_offset =  depots_count + rechargers_count
    new_combined_route = []
    for old_vehicle_route in combined_route:
        new_vehicle_route = []
        for i,node in enumerate(old_vehicle_route):
            if (node<depots_count):
                new_vehicle_route.append(node)
            elif (node>=cust_offset):
                new_vehicle_route.append(node)
                if(charging_scheme[node-cust_offset]):
                    next = old_vehicle_route[i+1]
                    station_to_add = np.argmin([distances[node][st]+distances[st][next] for st in range(depots_count,depots_count+rechargers_count)])+depots_count
                    new_vehicle_route.append(station_to_add)
        if (len(new_vehicle_route)>2):
            new_combined_route.append(new_vehicle_route)
    return new_combined_route