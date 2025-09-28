import numpy as np
import math
def CalcDistances(coordinates):
    distances= np.zeros((len(coordinates),len(coordinates)))
    for i in range(0,len(coordinates)):
        for j in range(0,len(coordinates)):
            if (i!=j):
                distances[i][j]=math.dist([coordinates[i].x,coordinates[i].y],[coordinates[j].x,coordinates[j].y])
    np.fill_diagonal(distances, 1e15)
    return distances