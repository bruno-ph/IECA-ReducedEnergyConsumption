import numpy as np
from random import choices
def InitializeChargingPopulation(pop_size,distances, depots_count,rechargers_count,customers_count):
    mask = np.zeros((pop_size,customers_count))
    associated_stations = np.zeros(customers_count)
    dmax= 1e-18
    dmin=1e18
    #fazer associações de cliente e estação mais próximas
    for i in range(0,customers_count):
        offset_customer_index = i+depots_count + rechargers_count
        candidate_stations_distances = distances[offset_customer_index][depots_count: depots_count+rechargers_count]
        best_dist = min(candidate_stations_distances)
        tmp = np.where(candidate_stations_distances ==best_dist)
        associated_stations[i] = tmp[0][0] + depots_count
        #encontrar distancia máxima e minima entre um par cliente estação
        if (best_dist>dmax): dmax = best_dist
        if (best_dist<dmin): dmin = best_dist
    for i in range (0,customers_count):
        dist = distances[depots_count+rechargers_count+i][int(associated_stations[i])]
        probability = (dmax-dist)/((dmax+1)-dmin) 
        for j in range(0,pop_size):
            mask[j][i]= choices([1,0],weights=[probability,1-probability],k=1)[0]
    return mask
    
    
