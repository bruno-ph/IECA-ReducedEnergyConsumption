import numpy as np
def InitializeElitePopulation(depots_count,rechargers_count,customers_count,distances,fuel_cap,load_cap,refuel_rate, vel, unit_weight,cons_rate,all_coors):
    routes = []
    ranked_customers = sorted([(all_coors[x].due_time,x) for x in range(depots_count+rechargers_count,depots_count+rechargers_count+customers_count)])
    #find nearest recharging station for all nodes
    
    nearest_stations = [depots_count+np.argmin([distances[x][rs] for rs in range(depots_count,rechargers_count+1)]) for x in range (0,len(distances))]

    total_cost =0.0
    while (ranked_customers):
        route = [0]
        load = min(load_cap,sum(all_coors[x[1]].demand for x in ranked_customers))
        battery = fuel_cap
        elapsed_time = 0.0
        cost = 0.0
        objective_rank_index = 0
        while (objective_rank_index<len(ranked_customers) and ranked_customers): #
            current_pos = route[-1]
            objective = ranked_customers[objective_rank_index][1]

            objective_demand = all_coors[objective].demand
            dist = distances[current_pos][objective]
            required_battery = (((1.0 + load * unit_weight)*dist) * cons_rate)  
            return_battery = (((1.0 + (load-objective_demand) * unit_weight)*distances[objective][nearest_stations[objective]]) * cons_rate)
            potential_elapsed_time = elapsed_time + dist/vel
            objective_ready_time = all_coors[objective].ready_time
            objective_due_time = ranked_customers[objective_rank_index][0]
            if (required_battery+return_battery<=battery and potential_elapsed_time<objective_due_time):
                route.append(objective)
                battery -= required_battery
                cost +=required_battery
                load -= objective_demand
                elapsed_time = max(objective_ready_time,potential_elapsed_time) + all_coors[objective].service_time
                objective_rank_index+=1
            elif (potential_elapsed_time<objective_due_time):
                route.append(nearest_stations[current_pos])
                dist = distances[current_pos][route[-1]]
                current_pos = route[-1]
                battery_to_station = (((1.0 + load * unit_weight)*dist) * cons_rate)  
                elapsed_time += dist/vel + (fuel_cap -(battery-battery_to_station))*refuel_rate
                battery = fuel_cap
                cost +=battery_to_station
                required_battery = (((1.0 + load * unit_weight)*distances[current_pos][objective]) * cons_rate)  
                #sort stations based on proximity to objective
                candidate_stations = sorted([(distances[st][objective],st) for st in range(depots_count,depots_count+rechargers_count)])
                while (required_battery+return_battery>battery and elapsed_time<objective_due_time and candidate_stations):
                    #find first station reacheable
                    next_station = next(((station for station in candidate_stations if  (((1.0 + load * unit_weight)*distances[current_pos][station[1]]) * cons_rate)<=battery  )),None)
                    candidate_stations= candidate_stations[:(candidate_stations.index(next_station))]
                    #do all the step updates
                    route.append(next_station[1])
                    dist = distances[current_pos][route[-1]]
                    current_pos = route[-1]
                    battery_to_station = (((1.0 + load * unit_weight)*dist) * cons_rate)
                    elapsed_time += dist/vel + (fuel_cap -(battery-battery_to_station))*refuel_rate
                    battery = fuel_cap
                    cost +=battery_to_station
                    required_battery = (((1.0 + load * unit_weight)*distances[current_pos][objective]) * cons_rate)  
            else:
                objective_rank_index+=1
        #THEN find way back to depot
        ranked_customers = [c for c in ranked_customers if c[1] not in route]
        routes.append(route)
        total_cost+=cost
    return routes


