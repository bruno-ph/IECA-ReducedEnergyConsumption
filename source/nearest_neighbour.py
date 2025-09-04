import numpy as np
from random import randint
def calcCost(distances,vertices):
    cost=0.0
    for i in range(0,len(vertices)-1):
        cost+=distances[vertices[i]][vertices[i+1]]
    return cost

def NearestNeighbourCost(distances, vertex_count):
    was_visited = np.zeros(vertex_count)
    initial_value = randint(0,vertex_count-1)
    current = initial_value
    route=np.full(vertex_count,-1)
    route[0]=initial_value
    was_visited[initial_value]=1
    route_size=1
    while (route_size!=vertex_count):
        best_dist = 1e15
        best_neigh = -1
        possible_neighbours = np.where(was_visited == 0)[0]
        for neighbour in possible_neighbours:
            curr_dist = distances[current][neighbour]
            if (curr_dist<best_dist):
                best_dist = curr_dist
                best_neigh = neighbour
        if (best_dist<1e15):
            route[route_size] = best_neigh
            current = best_neigh
            route_size+=1
            was_visited[best_neigh]=1
    return calcCost(distances,route)



