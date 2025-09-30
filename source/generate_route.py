import numpy as np
from eval import *
def GenerateRoute(combined_route, charging_scheme,depots_count,rechargers_count):
    cust_offset =  depots_count + rechargers_count
    new_route = []
    for old_vehicle_route in combined_route:
        new_vehicle_route = [old_vehicle_route[0]]
        for i,node in enumerate(old_vehicle_route):

            if (node>=cust_offset):
                new_vehicle_route.append(node)
                if (charging_scheme[node-cust_offset]):
                        if (i==len(old_vehicle_route)-1):
                            j=i-1
                            while (j>0):
                                if (old_vehicle_route[j]<cust_offset):
                                    new_vehicle_route.append(old_vehicle_route[j])
                                    break
                                j-=1
                        elif (old_vehicle_route[i+1]<cust_offset):
                            new_vehicle_route.append(old_vehicle_route[i+1])
                        else: #elif (old_vehicle_route[i+1]>=cust_offset):
                            j=i-1
                            while (j>0):
                                if (old_vehicle_route[j]<cust_offset):
                                    new_vehicle_route.append(old_vehicle_route[j])
                                    break
                                j-=1
        new_vehicle_route.append(old_vehicle_route[-1])
        new_route.append(new_vehicle_route)
    return new_route
        
                
                        

