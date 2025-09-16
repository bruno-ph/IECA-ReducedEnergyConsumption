air_density = 1.2041
roll_resist = 0.01
drag_resist = 0.48
gravity = 9.81
vehicle_surf_area = 11.112
transmission_effic = 0.89

def EvalElecSingle(vehicle_route,distances, speed, initial_load_mass, all_coors):
    #speed is m/s, mass is kg, h in watt per km, distance in km (probably)
    cost=0.0
    load_mass = initial_load_mass
    for i in range(0,len(vehicle_route)-1):
        dist =distances[vehicle_route[i]][vehicle_route[i+1]]
        alpha = (0.5 * roll_resist * air_density * vehicle_surf_area * pow(speed,3)) /(1000*transmission_effic)
        beta = (gravity*drag_resist*speed)/(1000*transmission_effic)
        h = alpha+beta*load_mass #watt per km
        cost += h*dist
        load_mass = max(load_mass - all_coors[i+1].demand,0)
    return cost

def EvalDisSingle(vehicle_route,distances):
    cost=0.0
    for i in range(0,len(vehicle_route)-1):
        cost+=distances[vehicle_route[i]][vehicle_route[i+1]]
    return cost

def EvalElecMulti(split_routes,distances, speed, initial_load_mass, all_coors):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalElecSingle(vehicle_route,distances,speed, initial_load_mass, all_coors)
    return cost

def EvalDisMulti(split_routes,distances):
    cost = 0.0
    for vehicle_route in split_routes:
        cost+= EvalDisSingle(vehicle_route,distances)
    return cost