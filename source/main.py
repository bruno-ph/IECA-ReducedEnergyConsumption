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
    charging_population = np.zeros((population_size,population_size))
    #Properly initialize charging population later

    initial_max_pheromone = 1 / ((1 - RHO) * initial_cost)
    pheromone_matrix = np.full((vertex_count,vertex_count),initial_max_pheromone)
    np.fill_diagonal(pheromone_matrix,0)

    elite_solution_set=[]

    for i in range(NUMBER_ITERATIONS):
        RoutingOptimization(vertex_count, len(depots),len(customers),len(rechargers), pheromone_matrix, population_size, ALPHA, BETA, distances, all_coor,load_cap, vel)




if __name__ == "__main__":
    main()