import numpy as np
from eval import FirstBreakingPoint

def FindSearchZone(vehicle_route,original_vehicle_route, breaking_point, depots_count,rechargers_count):
    breaking_point_index = np.where(original_vehicle_route == breaking_point)[0]
    last_station_before_bp_index = np.where(original_vehicle_route[:breaking_point_index] < depots_count+rechargers_count)[-1]
    search_zone_start_node = original_vehicle_route[last_station_before_bp_index]
    search_zone_start_index = np.where(vehicle_route = search_zone_start_node)
    search_zone_end_index = np.where(vehicle_route == breaking_point)
    search_zone = vehicle_route[search_zone_start_index:search_zone_end_index]
    return search_zone

def FirstBreakingPoint(vehicle_route, distances, all_coors, initial_load_amm, unit_weight, fuel_cap, cons_rate,depots_count,rechargers_count):

    vehicle_battery = fuel_cap
    vehicle_load = initial_load_amm
    for i in range(0,len(vehicle_route)-1):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        vehicle_battery -= ((vehicle_weight + vehicle_load * unit_weight)*dist) * cons_rate
        if (vehicle_battery<0):
            return i+1
        if (vehicle_route[i+1]> depots_count+rechargers_count):
            load_at_last_station = vehicle_load
            next_node = all_coors[vehicle_route[i+1]]
            if (vehicle_load < next_node.demand):
                raise Exception(f"Negative Vehicle Load - Current Load{vehicle_load} - Demand: {all_coors[vehicle_route[i+1]].demand}")
            else:
                vehicle_load -= next_node.demand       
        else:
            vehicle_battery = fuel_cap
    return -1


def FindReachableStations():
    pass

def PickRandomNodeAndStation():
    pass

def LocalSearch(original_solution,depots_count,rechargers_count, load_cap):
    mask = (original_solution>=depots_count and original_solution<depots_count+rechargers_count)
    custom_solution=[route[mask[i]] for i,route in enumerate(original_solution)]
    for i in range (len(custom_solution)):
        load_at_last_station = load_cap
        custom_route = custom_solution[i]
        iterations = 0
        breaking_point_index= FirstBreakingPoint(custom_route)
        while (breaking_point_index!=-1):
            if (iterations>=len(custom_route)-1):
                return [[],1e15]
            search_zone_start = np.where(custom_route<depots_count+rechargers_count and custom_route>=depots_count)[-1]
            search_zone = custom_route[search_zone_start,breaking_point_index]
            reachable_stations=[] #matrix of reachable stations for each node in search zone
            for ni,node in enumerate(search_zone):
                rs = FindReachableStations(node) #should return an array of tuples {station number, cost to station} for that node
                if rs:
                    reachable_stations.append(rs)
                else:
                    search_zone.pop(ni) #delete from search zone if can't reach a station
            node_to_receive_station, station_to_be_added = PickRandomNodeAndStation()
            node_to_receive_station_index = np.where(custom_route == node_to_receive_station)[-1]
            custom_route.insert(station_to_be_added,node_to_receive_station_index) #watch out for off by one error
            breaking_point_index= FirstBreakingPoint(custom_route) #reset and iterate
            iterations+=1
        custom_solution[i]=custom_route
    #do local search





            

        


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