import numpy as np
import math
def CalcDistances(coordinates):
    distances= np.zeros((len(coordinates),len(coordinates)))
    for i in range(0,len(coordinates)):
        for j in range(0,len(coordinates)):
            if (i!=j):
                distances[i][j]=math.dist([coordinates[i][0],coordinates[i][1]],[coordinates[j][0],coordinates[j][1]])
    np.fill_diagonal(distances, 1e15)
    return distances