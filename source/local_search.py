import numpy as np
from eval import EvalElecMulti, IsViable
from random import uniform
def FindSearchZone(vehicle_route,original_vehicle_route, breaking_point, depots_count,rechargers_count):
    breaking_point_index = np.where(original_vehicle_route == breaking_point)[0]
    last_station_before_bp_index = np.where(original_vehicle_route[:breaking_point_index] < depots_count+rechargers_count)[-1]
    search_zone_start_node = original_vehicle_route[last_station_before_bp_index]
    search_zone_start_index = np.where(vehicle_route = search_zone_start_node)
    search_zone_end_index = np.where(vehicle_route == breaking_point)
    search_zone = vehicle_route[search_zone_start_index:search_zone_end_index]
    return search_zone

def FirstBreakingPoint(vehicle_route, distances, all_coors, initial_load_amm, unit_weight, fuel_cap, cons_rate,depots_count,rechargers_count, vehicle_weight):

    vehicle_battery = fuel_cap
    vehicle_load = initial_load_amm
    for i in range(0,len(vehicle_route)-1):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        vehicle_battery -= ((vehicle_weight + vehicle_load * unit_weight)*dist) * cons_rate
        if (vehicle_battery<0):
            return i+1
        if (vehicle_route[i+1]> depots_count+rechargers_count):
            next_node = all_coors[vehicle_route[i+1]]
            if (vehicle_load < next_node.demand):
                raise Exception(f"Negative Vehicle Load - Current Load{vehicle_load} - Demand: {all_coors[vehicle_route[i+1]].demand}")
            else:
                vehicle_load -= next_node.demand       
        else:
            vehicle_battery = fuel_cap
    return -1


def FindReachableStations(current_node, next_node ,depots_count,rechargers_count, distances, vehicle_weight, vehicle_load,unit_weight, cons_rate, vehicle_battery):
    rs = []
    for station in range(depots_count,depots_count+rechargers_count):
        dist1 = distances[current_node][station]
        
        station_cost = (((vehicle_weight + vehicle_load * unit_weight)*dist1) * cons_rate)
        if (vehicle_battery-station_cost>0):
            dist2= distances[station][next_node]
            station_return_cost = (((vehicle_weight + vehicle_load * unit_weight)*dist2) * cons_rate)
            rs.append(station, station_cost + station_return_cost)
    return rs

def PickRandomNodeAndStation(search_zone,rs):
    chances =[]
    chances_sum = 0.0
    for i, node_reachable_stations in enumerate(rs):
        for station in node_reachable_stations:
            cost_inverted = 1/station[1]
            chances_sum+= cost_inverted
            chances.append((station[0],search_zone[i],chances_sum)) #station, origin, station_cost
            
    random_value = uniform(0.0, chances_sum)
    for chance in chances:
        if (random_value<=chance[2]):
            return [chance[1],chances[0]]
    raise Exception


def LocalSearch(original_solution,original_solution_cost, depots_count,rechargers_count,all_coors,speed, load_cap, distances, vehicle_weight, vehicle_load, unit_weight, cons_rate, fuel_cap,refuel_rate,max_iter):
    custom_solution = []
    station_count =0 
    for io in original_solution:
        ci =[]
        for jo in io:
            if (jo>=depots_count and jo<depots_count+rechargers_count):
                ci.append(jo)
                station_count+=1
        custom_solution.append(ci)
    #mask = (original_solution>=depots_count and original_solution<depots_count+rechargers_count)
    if (station_count==0):
        return (original_solution,original_solution_cost)
    return_solution =original_solution
    improvement = 1
    best_cost = original_solution_cost
    ls_iterations = 0
    while (improvement>0.00001 and ls_iterations<max_iter):
        for i in range (len(custom_solution)):
            custom_route = custom_solution[i]
            iterations = 0
            breaking_point_index= FirstBreakingPoint(custom_route)
            while (breaking_point_index!=-1):
                if (iterations>=len(custom_route)-2):
                    raise Exception
                search_zone_start = np.where(custom_route<depots_count+rechargers_count and custom_route>=depots_count)[-1]
                search_zone = custom_route[search_zone_start,breaking_point_index]
                reachable_stations=[] #matrix of reachable stations for each node in search zone
                for ni,node in enumerate(search_zone):
                    rs = FindReachableStations(node,search_zone[ni+1],depots_count,rechargers_count,distances, vehicle_weight, vehicle_load, unit_weight, cons_rate, fuel_cap) #should return an array of tuples {station number, cost to station} for that node
                    if rs:
                        reachable_stations.append(rs)
                    else:
                        search_zone.pop(ni) #delete from search zone if can't reach a station
                node_to_receive_station, station_to_be_added = PickRandomNodeAndStation(search_zone,rs)
                node_to_receive_station_index = np.where(custom_route == node_to_receive_station)[-1]
                custom_route.insert(station_to_be_added,node_to_receive_station_index) #watch out for off by one error
                breaking_point_index= FirstBreakingPoint(custom_route, distances, all_coors, load_cap, unit_weight, fuel_cap, cons_rate, depots_count, rechargers_count, vehicle_weight) #reset and iterate
                iterations+=1
            custom_solution[i]=custom_route
        route_station_indexes = []
        for r_i,route in enumerate(custom_solution):
            for s_i,node in enumerate(len(route)):
                if (node>=depots_count and node<depots_count+rechargers_count):
                    route_station_indexes.append((r_i,s_i))
        tmp_cost = EvalElecMulti(custom_solution,distances,speed,load_cap,all_coors,unit_weight,cons_rate)
        #exchange
        for i in route_station_indexes:
            for j in range(i,len(route_station_indexes)):
                route1 = route_station_indexes[i][0]
                station1=route_station_indexes[i][1]
                route2 = route_station_indexes[j][0]
                station2=route_station_indexes[j][1]
                tmp=custom_solution[route1][station1]
                custom_solution[route1][station1] = custom_solution[route2][station2]
                custom_solution[route2][station2] = tmp
                tmp_cost_exchange = EvalElecMulti(custom_solution,distances,speed,load_cap,all_coors,unit_weight,cons_rate)
                if (tmp_cost<tmp_cost_exchange or not IsViable(custom_solution,distances,speed,all_coors,load_cap,unit_weight,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)):
                    tmp=custom_solution[route1][station1]
                    custom_solution[route1][station1] = custom_solution[route2][station2]
                    custom_solution[route2][station2] = tmp
                else:
                    tmp_cost= tmp_cost_exchange
        #move
        for i in route_station_indexes:
            for j in range(depots_count,depots_count+rechargers_count):
                if (i==j):
                    continue
                route1 = route_station_indexes[i][0]
                station1=route_station_indexes[i][1]
                tmp=custom_solution[route1][station1]
                custom_solution[route1][station1] = j
                tmp_cost_exchange = EvalElecMulti(custom_solution,distances,speed,load_cap,all_coors,unit_weight,cons_rate)
                if (tmp_cost<tmp_cost_exchange or not IsViable(custom_solution,distances,speed,all_coors,load_cap,unit_weight,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)):
                    tmp=custom_solution[route1][station1]
                    custom_solution[route1][station1] = tmp
                else:
                    tmp_cost= tmp_cost_exchange
        improvement = -tmp_cost-best_cost
        if (tmp_cost<best_cost and IsViable(custom_solution,distances,speed,all_coors,load_cap,unit_weight,fuel_cap,cons_rate,refuel_rate,depots_count,rechargers_count)):
            return_solution= custom_solution
            best_cost=tmp_cost
        ls_iterations+=1
    return (return_solution,best_cost)

        #check if is improved
    

    






            

        


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