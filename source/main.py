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
from charging_optimization import ChargingOptimization
from generate_route import GenerateRoute
from eval import EvalElecMulti, IsViable
from update_pheromones import UpdatePheromones
from local_search import LocalSearch
from initialize_elite import InitializeElitePopulation
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
    charging_population = InitializeChargingPopulation(population_size, distances, depots_count,recharger_count,customer_count)

    initial_max_pheromone = 1 / ((1 - RHO) * initial_cost)
    pheromone_matrix = np.full((vertex_count,vertex_count),initial_max_pheromone)
    np.fill_diagonal(pheromone_matrix,0)

    elite_solution_set=[(InitializeElitePopulation(depots_count,recharger_count,customer_count,distances,fuel_cap,load_cap,refuel_rate,vel,load_unit_cost,cons_rate,demand,ready_time,due_date,service_time))]
    if (not IsViable(elite_solution_set[0],distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
        raise Exception
    elite_population_costs=[EvalElecMulti(elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) for elite_solution in elite_solution_set]
    max_pheromone = 1 #maybe base on the first elite solution
    min_pheromone = 1
    for iteration in range(NUMBER_ITERATIONS):
        print(iteration)
        best_routing_ant,routing_ant_quality, routing_ant_charging_scheme = RoutingOptimization(vertex_count,depots_count,customer_count,recharger_count, pheromone_matrix, population_size, ALPHA, BETA, distances, demand,ready_time, service_time,due_date,load_cap, vel,load_unit_cost,cons_rate,fuel_cap,refuel_rate)
        offspring_population = ChargingOptimization(charging_population,routing_ant_charging_scheme)

        #combine and rate charging and offspring population
        charging_population = charging_population.astype(bool)
        combined_charging_population = np.concatenate((charging_population,offspring_population))
        charging_population_ratings = np.zeros(len(combined_charging_population))
        for im,member in enumerate(combined_charging_population):
            charging_population_ratings[im] = EvalElecMulti(GenerateRoute(best_routing_ant,member,depots_count,recharger_count),distances,vel,load_cap,demand,load_unit_cost,cons_rate)
        best_charging_schemes_indexes = np.argsort(charging_population_ratings)[:population_size]
        best_charging_scheme= combined_charging_population[best_charging_schemes_indexes[0]]
        charging_population = combined_charging_population[best_charging_schemes_indexes]
        new_solution = GenerateRoute(best_routing_ant, best_charging_scheme, depots_count,recharger_count)
        new_solution_cost = EvalElecMulti(new_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate)
        
        if (IsViable(new_solution,distances, vel, demand,ready_time, service_time,due_date, load_cap, load_unit_cost, fuel_cap, cons_rate,refuel_rate,depots_count,recharger_count)):
            if (len(elite_solution_set)<population_size):
                elite_solution_set.append(new_solution)
                elite_population_costs = [EvalElecMulti(elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) for elite_solution in elite_solution_set]
            else:
                elite_population_costs = [EvalElecMulti(elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) for elite_solution in elite_solution_set]
                elite_solution_set = [es for _,es in sorted(zip(elite_population_costs,elite_solution_set))]
                if (new_solution_cost<max(elite_population_costs)):
                    elite_solution_set[-1]= new_solution
                    elite_population_costs = [EvalElecMulti(elite_solution,distances,vel,load_cap,demand,load_unit_cost,cons_rate) for elite_solution in elite_solution_set]
        else:
            new_solution = []
        best_solution_cost = EvalElecMulti(elite_solution_set[-1],distances,vel,load_cap,demand,load_unit_cost,cons_rate)
        max_pheromone = 1 / ((1 - RHO) * best_solution_cost)
        min_pheromone = (max_pheromone*(1 - pow(0.005,(1/vertex_count)))) / ((vertex_count/2 - 1)*pow(0.005,(1/vertex_count)))
        pheromone_matrix = UpdatePheromones(RHO, pheromone_matrix, elite_solution_set, elite_population_costs, new_solution, new_solution_cost, max_pheromone, min_pheromone)
    best_solution= elite_solution_set[-1]
    best_solution_cost = EvalElecMulti(best_solution,distances, vel, load_cap, demand, load_unit_cost, cons_rate)
    tentative_improved_solution, improved_solution_cost = LocalSearch(best_solution,best_solution_cost,depots_count,recharger_count, demand,ready_time, service_time,due_date,vel,load_cap,distances,1.0,load_unit_cost,cons_rate,fuel_cap,refuel_rate,1000)
    if (improved_solution_cost<best_solution_cost): #and it is valid!
        best_solution=tentative_improved_solution
        best_solution_cost=improved_solution_cost
    for route in best_solution:
        for node in route:
            print(id[node]+"->",end="")
        print("END")
    print("Electric Unit Cost:"+str(best_solution_cost))
    



if __name__ == "__main__":
    main()