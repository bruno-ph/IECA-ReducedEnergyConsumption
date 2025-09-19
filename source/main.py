RHO = 0.98
ALPHA = 1
BETA = 2
NUMBER_ITERATIONS = 5000
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
        best_routing_ant,routing_ant_quality, routing_ant_charging_scheme = RoutingOptimization(vertex_count, len(depots),len(customers),len(rechargers), pheromone_matrix, population_size, ALPHA, BETA, distances, all_coor,load_cap, vel)
        offspring_population = ChargingOptimization(charging_population,routing_ant_charging_scheme)

        #combine and rate charging and offspring population
        charging_population = charging_population.astype(bool)
        combined_charging_population = np.concatenate((charging_population,offspring_population))
        charging_population_ratings = np.zeros(len(combined_charging_population))
        for im,member in enumerate(combined_charging_population):
            charging_population_ratings[im] = EvalElecMulti(GenerateRoute(best_routing_ant,member,len(depots),len(rechargers)),distances,vel,load_cap,all_coor)

        #EnhancedInteraction(selected_charging_population, selected_population_rankings, elite_solution_set, best_routing_ant )



if __name__ == "__main__":
    main()