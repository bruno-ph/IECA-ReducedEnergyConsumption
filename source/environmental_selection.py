
import numpy as np
from binary_population import BinaryPopulation
#Performs modified Non-Dominated Sorting where constraints are more relevant than the (singular) element fitness
def NDSortCharging(fitness_list,constraints):
    dominates=[[] for _ in range (len(fitness_list))]
    dom_count = np.zeros((len(fitness_list)))
    fronts=[]
    for i,fitness_1 in enumerate(fitness_list):
        for j,fitness_2 in enumerate(fitness_list):
            if (i==j):
                continue
            if (constraints[j]>constraints[i]): #dominates, 2 breaks more constraints
                dominates[i].append(j)
            elif (constraints[i]>constraints[j]): #dominated, 1 breaks more constraints
                dom_count[i]+=1
            elif (fitness_1>fitness_2): #dominates
                dominates[i].append(j)
            elif (fitness_2>fitness_1): #dominated by
                dom_count[i]+=1
    selected_front = np.where(dom_count==0)[0]
    while (len(selected_front)>0):
        fronts.append(selected_front)
        for sf in selected_front:
            dom_count[sf]=-1
            for dominated in dominates[sf]:
                dom_count[dominated]-=1
        selected_front = np.where(dom_count==0)[0]
    return fronts

def CrowdingDistance(population,front_no):
    front_no = np.array(front_no).astype(int)
    cd = np.zeros((len(front_no)))
    for f in range(max(front_no)+1):
        front = np.array(np.where(front_no == f)[0])
        front_cost = [(population[f],f) for f in front]
        front_cost.sort()
        fcosts = [c[0] for c in front_cost]
        fmax = np.max(fcosts)
        fmin=np.min(fcosts)
        cd[front_cost[0][1]]=1e15
        cd[front_cost[-1][1]]=1e15
        if (fmax!=fmin):
            for i in range (1,len(front_cost)-1):
                cd[front_cost[i][1]] = (population[front_cost[i-1][1]] - population[front_cost[i+1][1]])/(fmax-fmin)
    return cd

#Filter population based on modified NDSorting and crowding distance
def EnvironmentalSelection(charging_population,pop_size):
    costs = [c.cost for c in charging_population]
    negative_costs = [-c for c in costs]
    cons =[c.cons for c in charging_population]
    fronts= NDSortCharging(negative_costs ,cons)
    next=[]
    front_counter=-1
    front_numbers = np.ones(len(charging_population))*-1
    while (len(next)<pop_size):
        front_counter+=1
        current_front = fronts[front_counter]
        [next.append(i) for i in current_front]
        for value in current_front:
            front_numbers[value] = front_counter
    crowd_distances_values = CrowdingDistance([costs[n] for n in next],[front_numbers[n] for n in next])
    crowd_distances = {number:crowd_distances_values[i] for i,number in enumerate(next)}
    if (len(next)>pop_size):
        trim_members= np.argwhere(front_numbers == front_counter)
        trim_values = [(crowd_distances[t[0]],t[0]) for t in trim_members]
        trim_values.sort()
        next[len(next)-len(trim_values):] = [t[1] for t in trim_values]
    next = next[:pop_size]
    c = [charging_population[n] for n in next]
    f = [front_numbers[n] for n in next]
    d = [crowd_distances[n] for n in next]
    return [c,f,d]
    
    
