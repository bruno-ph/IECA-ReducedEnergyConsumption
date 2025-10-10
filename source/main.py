RHO = 0.98
ALPHA = 1
BETA = 2
NUMBER_ITERATIONS = 5000
REAL_MAX_PAYLOAD_WEIGHT = 3650
REAL_VEHICLE_WEIGHT = 6350
MAX_ELITE = 30
import sys
import numpy as np
import read_instance as read_instance
from calc_distances import CalcDistances
from nearest_neighbour import NearestNeighbourCost
from routing_optimization import RoutingOptimization
from initialize_population import InitializeChargingPopulation
from charging_optimization import ChargingOptimization, TournamentSelection
from generate_route import GenerateRoute
from eval import EvalElecMulti, IsViable, EvalConstraint, EvalDisMulti
from update_pheromones import UpdatePheromones
from initialize_elite import InitializeElitePopulation
from binary_population import BinaryPopulation, CalculateCost
from environmental_selection import EnvironmentalSelection
from time import perf_counter
def main():
    start_time = perf_counter()
    instanceFile = (sys.argv[1])
    hits = 0
    #best_solution
    elec_timeline = np.zeros((NUMBER_ITERATIONS))
    #dist_timeline = np.zeros((NUMBER_ITERATIONS+1))
    time_initialize_charging = 0
    time_initialize_elite = 0
    time_routing = 0
    time_charging_opt = 0
    time_interaction = 0
    time_pheromone_update = 0
    time_charging_selection = 0

    id, types,pos,demand,ready_time,due_date,service_time,recharger_count,depots_count,customer_count,fuel_cap, load_cap, cons_rate, refuel_rate, vel = read_instance.ReadInstance(instanceFile)
    real_to_virtual_cargo_ratio = REAL_MAX_PAYLOAD_WEIGHT/load_cap
    load_unit_cost = real_to_virtual_cargo_ratio/REAL_VEHICLE_WEIGHT
    vertex_count= recharger_count+depots_count+customer_count
    distances=CalcDistances(pos)

    initial_cost = NearestNeighbourCost(distances,vertex_count)
    #print(initial_cost)

    population_size = min(customer_count,MAX_ELITE)
    time_tmp = perf_counter()
    charging_population_masks = InitializeChargingPopulation(population_size, distances, depots_count,recharger_count,customer_count)
    charging_population = [BinaryPopulation(mask,CalculateCost(mask, distances, depots_count, recharger_count,load_cap,cons_rate,load_unit_cost), 1e15)  for mask in charging_population_masks]
    charging_population,front_number,crowding_distance = EnvironmentalSelection(charging_population, population_size)
    time_initialize_charging = perf_counter()-time_tmp
    initial_max_pheromone = 1 / ((1 - RHO) * initial_cost)
    pheromone_matrix = np.full((vertex_count,vertex_count),initial_max_pheromone)
    np.fill_diagonal(pheromone_matrix,0)

    time_tmp = perf_counter()
    first_elite_solution=(InitializeElitePopulation(depots_count,recharger_count,customer_count,distances,fuel_cap,load_cap,refuel_rate,vel,load_unit_cost,cons_rate,demand,ready_time,due_date,service_time))
    if (not IsViable(first_elite_solution,distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
        raise Exception
    first_elite_cost = EvalElecMulti(first_elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) 
    elite_population =[(first_elite_cost,first_elite_solution)]
    time_initialize_elite = perf_counter()-time_tmp
    
    max_pheromone = 1
    min_pheromone = 1


    #elec_timeline[0] = (elite_population[0][0])
    #dist_timeline[0] = EvalDisMulti(elite_population[0][1])

    for iteration in range(NUMBER_ITERATIONS):
        # print(iteration)
        time_tmp = perf_counter()
        best_routing_ant,routing_ant_quality, routing_ant_charging_scheme = RoutingOptimization(vertex_count,depots_count,customer_count,recharger_count, pheromone_matrix, population_size, ALPHA, BETA, distances, demand,ready_time, service_time,due_date,load_cap, vel,load_unit_cost,cons_rate,fuel_cap,refuel_rate)
        time_routing += perf_counter()-time_tmp

        time_tmp = perf_counter()
        crowding_distance = [-cd for cd in crowding_distance]
        tourney_results = TournamentSelection(2,2*population_size,front_number,crowding_distance)
        mating_pool = [charging_population[int(mate)] for mate in tourney_results]
        offspring_population = ChargingOptimization(mating_pool,routing_ant_charging_scheme,customer_count)
        time_charging_opt += perf_counter()-time_tmp

        time_tmp = perf_counter()
        best_penalty = 1e15
        best_cost = 1e15
        for mi,member in enumerate(offspring_population):
            created_ant = GenerateRoute(best_routing_ant,member.mask,depots_count,recharger_count,distances)
            member.cost = (EvalElecMulti(created_ant,distances,vel,load_cap,demand,load_unit_cost,cons_rate))
            member.cons = (EvalConstraint(created_ant, distances, vel, demand, ready_time, service_time, due_date, load_cap, load_unit_cost, fuel_cap, cons_rate, refuel_rate, depots_count, recharger_count))
            if ((best_penalty>member.cons) or((best_penalty==member.cons) and (best_cost>member.cost))):
                best_cost = member.cost
                best_penalty= member.cons
                best_generated_route = created_ant
        
    
        new_solution = best_generated_route
        new_solution_cost = best_cost
        
        
        if (best_penalty==0):
            if (not IsViable(new_solution,distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
                raise Exception
            if (len(elite_population)<population_size):
                elite_population.append((new_solution_cost,new_solution))
                elite_population.sort()
            elif (new_solution_cost<max(elite_population)[0]):
                    elite_population[-1]= (new_solution_cost,new_solution)
                    elite_population.sort()
            hits+=1
        else:
            new_solution = []
        time_interaction += perf_counter()-time_tmp

        time_tmp = perf_counter()
        combined_charging_population = (charging_population + offspring_population)
        charging_population,front_number,crowding_distance = EnvironmentalSelection(combined_charging_population, population_size)
        time_charging_selection+= perf_counter() - time_tmp

        best_solution_cost = elite_population[0][0]
        
        time_tmp = perf_counter()
        max_pheromone = 1 / ((1 - RHO) * best_solution_cost)
        min_pheromone = (max_pheromone*(1 - pow(0.005,(1/vertex_count)))) / ((vertex_count/2 - 1)*pow(0.005,(1/vertex_count)))
        pheromone_matrix = UpdatePheromones(RHO, pheromone_matrix, elite_population, new_solution, new_solution_cost, max_pheromone, min_pheromone)
        time_pheromone_update+= perf_counter() - time_tmp
        elec_timeline[iteration] = best_solution_cost
    
    best_solution= elite_population[0][1]
    best_solution_cost = elite_population[0][0]
    total_time = perf_counter() - start_time
    for route in best_solution:
        for node in route:
            print(id[node]+"->",end="")
        print("END")
    print("Electric Unit Cost: "+str(best_solution_cost))
    print("Distance Cost: "+str(EvalDisMulti(best_solution,distances)))
    
    print(f"Time- Initialize Charging Population: {time_initialize_charging} ({(time_initialize_charging/total_time)*100}%)")
    print(f"Time- Initialize First Elite Solution:  {time_initialize_elite} ({(time_initialize_elite/total_time)*100}%)")
    print(f"Time- Routing Optimization: {time_routing} ({(time_routing/total_time)*100}%)")
    print(f"Time- Charging Optimization: {time_charging_opt} ({(time_charging_opt/total_time)*100}%)")
    print(f"Time- Enhanced Population Interaction: {time_interaction} ({(time_interaction/total_time)*100}%)")
    print(f"Time- Charging Environmental Selection: {time_charging_selection} ({(time_charging_selection/total_time)*100}%)")
    print(f"Time- Pheromones Update: {time_pheromone_update} ({(time_pheromone_update/total_time)*100}%)")
    other_time = total_time - (time_initialize_charging + time_initialize_elite + time_routing + time_charging_opt + time_charging_selection + time_interaction + time_pheromone_update)
    print(f"Time- Other: {other_time} ({(other_time/total_time)*100}%)")
    print(f"Electric Cost Timeline: ", end ="")
    for i in range(len(elec_timeline)-1):
        print(f"{elec_timeline[i]} - ", end="")
    print(f"{elec_timeline[-1]}")

    
if __name__ == "__main__":
    main()