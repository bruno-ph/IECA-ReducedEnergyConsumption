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
import vertex
from calc_distances import CalcDistances
from nearest_neighbour import NearestNeighbourCost
from routing_optimization import RoutingOptimization
from initialize_population import InitializeChargingPopulation
from charging_optimization import ChargingOptimization, TournamentSelection
from generate_route import GenerateRoute
from eval import EvalElecMulti, IsViable, EvalDisMulti, EvalConstraint
from update_pheromones import UpdatePheromones
from local_search import LocalSearch
from initialize_elite import InitializeElitePopulation
from binary_population import BinaryPopulation, CalculateCost
from environmental_selection import EnvironmentalSelection
def main():
    instanceFile = (sys.argv[1])
    print (instanceFile)

    id, types,pos,demand,ready_time,due_date,service_time,recharger_count,depots_count,customer_count,fuel_cap, load_cap, cons_rate, refuel_rate, vel = read_instance.ReadInstance(instanceFile)
    real_to_virtual_cargo_ratio = REAL_MAX_PAYLOAD_WEIGHT/load_cap
    load_unit_cost = real_to_virtual_cargo_ratio/REAL_VEHICLE_WEIGHT
    vertex_count= recharger_count+depots_count+customer_count
    distances=CalcDistances(pos)

    initial_cost = NearestNeighbourCost(distances,vertex_count)
    print(initial_cost)

    population_size = min(customer_count,MAX_ELITE)

    charging_population_masks = InitializeChargingPopulation(population_size, distances, depots_count,recharger_count,customer_count)
    charging_population = [BinaryPopulation(mask,CalculateCost(mask, distances, depots_count, recharger_count,load_cap,cons_rate,load_unit_cost), 1e15)  for mask in charging_population_masks]
    charging_population,front_number,crowding_distance = EnvironmentalSelection(charging_population, population_size)

    initial_max_pheromone = 1 / ((1 - RHO) * initial_cost)
    pheromone_matrix = np.full((vertex_count,vertex_count),initial_max_pheromone)
    np.fill_diagonal(pheromone_matrix,0)

    first_elite_solution=(InitializeElitePopulation(depots_count,recharger_count,customer_count,distances,fuel_cap,load_cap,refuel_rate,vel,load_unit_cost,cons_rate,demand,ready_time,due_date,service_time))
    if (not IsViable(first_elite_solution,distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
        raise Exception
    first_elite_cost = EvalElecMulti(first_elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) 
    elite_population =[(first_elite_cost,first_elite_solution)]
    
    max_pheromone = 1 #maybe base on the first elite solution
    min_pheromone = 1

    hits = 0
    #best_solution
    elec_timeline = np.zeros((NUMBER_ITERATIONS+1))
    dist_timeline = np.zeros((NUMBER_ITERATIONS+1))
    iteration_best_found = -1
    time_best_found = 0
    time_initialize_elite = 0
    time_routing_split = 0
    time_routing_2opt = 0
    time_charging_opt = 0
    time_interaction = 0
    time_iterated_greedy = 0
    # best_elec_cost = elite_population_costs[0]
    # best_dist_cost = EvalDisMulti(elite_solution_set[-1])

    for iteration in range(NUMBER_ITERATIONS):
        print(iteration)
        best_routing_ant,routing_ant_quality, routing_ant_charging_scheme = RoutingOptimization(vertex_count,depots_count,customer_count,recharger_count, pheromone_matrix, population_size, ALPHA, BETA, distances, demand,ready_time, service_time,due_date,load_cap, vel,load_unit_cost,cons_rate,fuel_cap,refuel_rate)
        mating_pool = TournamentSelection(2,2*population_size,front_number,-crowding_distance)
        offspring_population = ChargingOptimization(charging_population[mating_pool],routing_ant_charging_scheme)

        #combine and rate charging and offspring population
        #charging_population = charging_population.astype(bool)
        
        best_penalty = 1e15
        best_cost = 1e15
        best_offspring = offspring_population[0]
        for mi,member in enumerate(offspring_population):
            created_ant = GenerateRoute(best_routing_ant,member.mask,depots_count,recharger_count,distances)
            member.cost = (EvalElecMulti(created_ant,distances,vel,load_cap,demand,load_unit_cost,cons_rate))
            member.cons = (EvalConstraint(created_ant))
            if ((best_penalty>member.cons) or((best_penalty==member.cons) and (best_cost>member.cost))):
                best_offspring = member
        
        combined_charging_population = (charging_population + offspring_population)
        charging_population,front_number,crowding_distance = EnvironmentalSelection(combined_charging_population, population_size)
        new_solution = GenerateRoute(best_routing_ant, best_offspring, depots_count,recharger_count,distances)
        new_solution_cost = EvalElecMulti(new_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate)
        
        if (IsViable(new_solution,distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
            
            if (len(elite_population)<population_size):
                elite_population.append((new_solution_cost,new_solution))
                elite_population.sort()
            elif (new_solution_cost<max(elite_population)[0]):
                    elite_population[-1]= (new_solution_cost,new_solution)
                    elite_population.sort()
            hits+=1
        else:
            new_solution = []
        best_solution_cost = elite_population[0][0]
        max_pheromone = 1 / ((1 - RHO) * best_solution_cost)
        min_pheromone = (max_pheromone*(1 - pow(0.005,(1/vertex_count)))) / ((vertex_count/2 - 1)*pow(0.005,(1/vertex_count)))
        
        pheromone_matrix = UpdatePheromones(RHO, pheromone_matrix, elite_population, new_solution, new_solution_cost, max_pheromone, min_pheromone)
    best_solution= elite_population[0][1]
    best_solution_cost = elite_population[0][0]
    # tentative_improved_solution, improved_solution_cost = LocalSearch(best_solution,best_solution_cost,depots_count,recharger_count, demand,ready_time, service_time,due_date,vel,load_cap,distances,1.0,load_unit_cost,cons_rate,fuel_cap,refuel_rate,1000)
    # if (improved_solution_cost<best_solution_cost): #and it is valid!
    #     best_solution=tentative_improved_solution
    #     best_solution_cost=improved_solution_cost
    for route in best_solution:
        for node in route:
            print(id[node]+"->",end="")
        print("END")
    print("Electric Unit Cost:"+str(best_solution_cost))
    



if __name__ == "__main__":
    main()