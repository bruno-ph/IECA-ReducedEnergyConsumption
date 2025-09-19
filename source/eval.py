air_density = 1.2041 #kg/m³
roll_resist = 0.01
drag_resist = 0.48
gravity = 9.81 #m/s²
vehicle_surf_area = 11.112 #m²
transmission_effic = 0.89
vehicle_weight = 1.0
#speed m/s, a is m/s², h is kW (second by second)

def EvalElecSingle(vehicle_route,distances, speed, initial_load_amm, all_coors,unit_weight):
    #speed is m/s, mass is kg, h in joule per second, distance is m
    cost=0.0
    load_amm = initial_load_amm
    for i in range(0,len(vehicle_route)-2):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        energy_consumption = (vehicle_weight + load_amm * unit_weight)*dist
        # alpha = (0.5 * roll_resist * air_density * vehicle_surf_area * pow(speed,3)) /(1000*transmission_effic)
        # beta = (gravity*drag_resist*speed)/(1000*transmission_effic)
        # h = alpha+beta*load_mass #watt or joule per second
        # cost += h*(dist/speed) #total joules
        cost += energy_consumption
        load_amm = max(load_amm - all_coors[vehicle_route[i+1]].demand,0)
    return cost

def EvalDisSingle(vehicle_route,distances):
    cost=0.0
    for i in range(0,len(vehicle_route)-1):
        cost+=distances[vehicle_route[i]][vehicle_route[i+1]]
    return cost

def EvalElecMulti(split_routes,distances, speed, initial_load_mass, all_coors,load_unit_cost):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalElecSingle(vehicle_route,distances,speed, initial_load_mass, all_coors,load_unit_cost)
    return cost

def EvalDisMulti(split_routes,distances):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalDisSingle(vehicle_route,distances)
    return cost