air_density = 1.2041 #kg/m³
roll_resist = 0.01
drag_resist = 0.48
gravity = 9.81 #m/s²
vehicle_surf_area = 11.112 #m²
transmission_effic = 0.89
vehicle_weight = 1.0
#speed m/s, a is m/s², h is kW (second by second)

def EvalElecSingle(vehicle_route,distances, speed, initial_load_amm, demand,unit_weight, cons_rate):
    cost=0.0
    load_amm = sum([demand[x] for x in vehicle_route])
    if (load_amm>initial_load_amm):
            raise Exception("Vehicle load exceeds max cargo size")
    for i in range(0,len(vehicle_route)-1):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        energy_consumption = ((vehicle_weight + load_amm * unit_weight)*dist) * cons_rate
        cost += energy_consumption
        load_amm = max(load_amm - demand[vehicle_route[i+1]],0)
    return cost

def EvalDisSingle(vehicle_route,distances):
    cost=0.0
    for i in range(0,len(vehicle_route)-1):
        cost+=distances[vehicle_route[i]][vehicle_route[i+1]]
    return cost

def EvalElecMulti(split_routes,distances, speed, initial_load_mass, demand,load_unit_cost,cons_rate):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalElecSingle(vehicle_route,distances,speed, initial_load_mass, demand,load_unit_cost,cons_rate)
    return cost

def EvalDisMulti(split_routes,distances):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalDisSingle(vehicle_route,distances)
    return cost

def IsViable(vehicle_routes, distances, speed, demand,ready_time, service_time,due_time, initial_load_amm, unit_weight, fuel_cap, cons_rate, refuel_rate,depots_count,rechargers_count):
    for vehicle_route in vehicle_routes:
        if (not RouteValid(vehicle_route, distances, speed, demand, ready_time, service_time, due_time, initial_load_amm, unit_weight, fuel_cap, cons_rate, refuel_rate, depots_count, rechargers_count)):
            return False
    customers = [x for x in range(depots_count+rechargers_count,len(distances))]
    combined_route = [node for route in vehicle_routes for node in route]
    check = [x for x in customers if x not in combined_route]
    if (check):
        return False
    return True

def RouteValid(vehicle_route, distances, speed, demand,ready_time, service_time,due_time, initial_load_amm, unit_weight, fuel_cap, cons_rate, refuel_rate,depots_count,rechargers_count):
    if (vehicle_route[0]>=depots_count or vehicle_route[-1]>=depots_count):
        return False
    vehicle_battery = fuel_cap
    vehicle_load = sum([demand[x] for x in vehicle_route])
    if (vehicle_load>initial_load_amm):
            raise Exception("Vehicle load exceeds max cargo size")
    elapsed_time = 0.0
    for i in range(0,len(vehicle_route)-1):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        elapsed_time += dist/speed
        vehicle_battery -= ((vehicle_weight + vehicle_load * unit_weight)*dist) * cons_rate
        if (vehicle_battery<0):
            #print("BATTERY DEAD")
            return False
        if (vehicle_route[i+1]> depots_count+rechargers_count):
            next_node = vehicle_route[i+1]
            if (vehicle_load < demand[next_node]):
                raise Exception(f"Negative Vehicle Load - Current Load{vehicle_load} - Demand: {[demand[vehicle_route[i+1]]]}")
            elif (elapsed_time>due_time[next_node]):
                #print("OUT OF TIME")
                return False
            else:
                elapsed_time += max(ready_time[next_node] - elapsed_time,0) + service_time[next_node]
                vehicle_load -= demand[next_node]  
        else:
            elapsed_time += (fuel_cap-vehicle_battery) * refuel_rate
            vehicle_battery = fuel_cap
    return True

def EvalConstraint(new_solution,distances, vel, demand,ready_time, service_time,due_time, load_cap, unit_weight, fuel_cap, cons_rate,refuel_rate,depots_count,rechargers_count):
    battery_penalty = 0
    demand_penalty = 0
    time_penalty = 0
    for vehicle_route in new_solution:    
        if (vehicle_route[0]>=depots_count or vehicle_route[-1]>=depots_count):
            raise Exception
        vehicle_battery = fuel_cap
        vehicle_load = sum([demand[x] for x in vehicle_route])
        if (vehicle_load>load_cap):
                raise Exception("Vehicle load exceeds max cargo size")
        elapsed_time = 0.0
        for i in range(0,len(vehicle_route)-1):
            dist =distances[vehicle_route[i]][vehicle_route[i+1]]
            elapsed_time += dist/vel
            vehicle_battery -= ((vehicle_weight + vehicle_load * unit_weight)*dist) * cons_rate
            if (vehicle_battery<0):
                battery_penalty-=vehicle_battery
            if (vehicle_route[i+1]> depots_count+rechargers_count):
                next_node = vehicle_route[i+1]
                if (vehicle_load < demand[next_node]):
                    demand_penalty += demand[next_node]-vehicle_load
                    raise Exception(f"Negative Vehicle Load - Current Load{vehicle_load} - Demand: {[demand[vehicle_route[i+1]]]}")
                elif (elapsed_time>due_time[next_node]):
                    time_penalty+= elapsed_time - due_time[next_node]
                else:
                    elapsed_time += max(ready_time[next_node] - elapsed_time,0) + service_time[next_node]
                    vehicle_load -= demand[next_node]  
            else:
                elapsed_time += (fuel_cap-vehicle_battery) * refuel_rate
                vehicle_battery = fuel_cap
    if (((battery_penalty+demand_penalty+time_penalty)==0)!=IsViable(new_solution,distances, vel, demand,ready_time, service_time,due_time, load_cap, unit_weight, fuel_cap, cons_rate,refuel_rate,depots_count,rechargers_count)):
        raise Exception
    return (battery_penalty+demand_penalty+time_penalty)

