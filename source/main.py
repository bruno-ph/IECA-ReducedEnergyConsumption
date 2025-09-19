RHO = 0.98
ALPHA = 1
BETA = 2
NUMBER_ITERATIONS = 5000
REAL_MAX_PAYLOAD_WEIGHT = 3650
REAL_VEHICLE_WEIGHT = 6350
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
from eval import EvalElecMulti

def main():
    instanceFile = (sys.argv[1])
    print (instanceFile)
    rechargers = []
    depots = []
    customers=[]

    rechargers, depots, customers,fuel_cap, load_cap, cons_rate, refuel_rate, vel = read_instance.ReadInstance(instanceFile)
    real_to_virtual_cargo_ratio = REAL_MAX_PAYLOAD_WEIGHT/load_cap
    load_unit_cost = real_to_virtual_cargo_ratio/REAL_VEHICLE_WEIGHT
    all_coor= depots+rechargers+customers
    vertex_count = len(all_coor)
    distances=CalcDistances(all_coor)

    initial_cost = NearestNeighbourCost(distances,vertex_count)
    print(initial_cost)

    population_size = len(customers)
    charging_population = InitializeChargingPopulation(population_size, distances, len(depots), len(rechargers), len(customers))

    initial_max_pheromone = 1 / ((1 - RHO) * initial_cost)
    pheromone_matrix = np.full((vertex_count,vertex_count),initial_max_pheromone)
    np.fill_diagonal(pheromone_matrix,0)

    elite_solution_set=[]

    for iteration in range(NUMBER_ITERATIONS):
        best_routing_ant,routing_ant_quality, routing_ant_charging_scheme = RoutingOptimization(vertex_count, len(depots),len(customers),len(rechargers), pheromone_matrix, population_size, ALPHA, BETA, distances, all_coor,load_cap, vel,load_unit_cost)
        offspring_population = ChargingOptimization(charging_population,routing_ant_charging_scheme)

        #combine and rate charging and offspring population
        charging_population = charging_population.astype(bool)
        combined_charging_population = np.concatenate((charging_population,offspring_population))
        charging_population_ratings = np.zeros(len(combined_charging_population))
        for im,member in enumerate(combined_charging_population):
            charging_population_ratings[im] = EvalElecMulti(GenerateRoute(best_routing_ant,member,len(depots),len(rechargers)),distances,vel,load_cap,all_coor,load_unit_cost)
        best_charging_schemes_indexes = np.argsort(charging_population_ratings)[:population_size]
        best_charging_scheme= combined_charging_population[best_charging_schemes_indexes[0]]
        charging_population = combined_charging_population[best_charging_schemes_indexes]
        new_solution = GenerateRoute(best_routing_ant, best_charging_scheme, len(depots), len(rechargers))
        if (len(elite_solution_set)<population_size and IsViable(new_solution)):
            elite_solution_set.append(new_solution)
        else:
            #rank the elite solutions and replace the worst one

        #if there exists an electricity-feasible solution s′ that is better than s then  7 s ← s′;  
        # 8 Update pheromone matrix φ by s; 
        # 9 Update pheromone matrix φ using Qbest;




if __name__ == "__main__":
    main()