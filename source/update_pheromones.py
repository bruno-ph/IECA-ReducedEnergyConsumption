def UpdatePheromones(rho, pheromone_matrix, elite_set, new_ant,new_ant_cost,max_phero,min_phero):
    pheromone_matrix = pheromone_matrix * rho
    pheromone_matrix[pheromone_matrix > max_phero] = max_phero
    pheromone_matrix[pheromone_matrix < min_phero] = min_phero
    # if ((not (elite_set)) and new_ant):
    #     for route in new_ant:
    #         for i in range (0,len(route)-1):
    #             pheromone_matrix[route[i],route[i+1]] += 1/new_ant_cost
    for i in range (len(elite_set)):
        cost = elite_set[i][0]
        for route in elite_set[i][1]:
            for j in range (0,len(route)-1):
                pheromone_matrix[route[j],route[j+1]] += 1/cost
        for route in new_ant:
            for j in range (0,len(route)-1):
                pheromone_matrix[route[j],route[j+1]] += 1/new_ant_cost
    pheromone_matrix[pheromone_matrix > max_phero] = max_phero
    pheromone_matrix[pheromone_matrix < min_phero] = min_phero
    return pheromone_matrix

        
