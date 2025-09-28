import numpy as np
def InitializeElitePopulation(depots_count,rechargers_count,customers_count,distances,fuel_cap,load_cap,refuel_rate, vel, unit_weight,cons_rate,all_coors):
    routes = []
    ranked_customers = sorted([(all_coors[x].ready_time,x) for x in range(depots_count+rechargers_count-1,customers_count)])
    #find nearest recharging station for all nodes
    
    nearest_stations = [depots_count+np.argmin([distances[x][rs] for rs in range(depots_count,rechargers_count+1)]) for x in range (0,len(distances))]

    total_cost =0.0
    while (ranked_customers):
        route = [0]
        load = load_cap
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
            return_battery = (((1.0 + load-objective_demand * unit_weight)*distances[objective][nearest_stations[objective]]) * cons_rate)
            potential_elapsed_time = elapsed_time + dist/vel
            objective_ready_time = ranked_customers[objective_rank_index][0]
            if (required_battery+return_battery<battery and potential_elapsed_time<objective_ready_time):
                route.append(objective)
                battery -= required_battery
                cost +=required_battery
                load -= objective_demand
                elapsed_time = objective_ready_time + all_coors[objective].service_time
                ranked_customers.pop(objective_rank_index)
            elif (required_battery+return_battery<battery):
                pass
                #find a route through all? possible station combinations to satisfy both battery and time conditions
            else:
                objective_rank_index+=1
        #THEN find way back to depot


