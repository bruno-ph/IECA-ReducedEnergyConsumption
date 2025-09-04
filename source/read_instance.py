
from vertex import Vertex

fuel_cap_index = 30
load_cap_index = 25
cons_rate_index = 25
refuel_rate_index = 26
vel_index = 20

def ReadInstance(instanceFile):
    file = open(instanceFile,"r")
    depots=[]
    rechargers=[]
    customers=[]
    counter=0
    filelines=file.readlines()
    for line in filelines[1:-6]:
        id, type,x,y, demand,ready_time,due_date,service_time =line.split()
        match type:
            case "f":
                rechargers.append(Vertex(float(x),float(y),float(demand), float(ready_time), float(due_date),float(service_time),counter,id,type))
            case "c":
                customers.append(Vertex(float(x),float(y),float(demand), float(ready_time), float(due_date),float(service_time),counter,id,type))
            case "d":
                depots.append(Vertex(float(x),float(y),float(demand), float(ready_time), float(due_date),float(service_time),counter,id,type))
        counter+=1
    for v in depots+rechargers+customers:
        print(v)
    fuel_cap = float(filelines[-5][fuel_cap_index:-2])
    load_cap = float(filelines[-4][load_cap_index:-2])
    cons_rate=float(filelines[-3][cons_rate_index:-2])
    refuel_rate=float(filelines[-2][refuel_rate_index:-2])
    vel=float(filelines[-1][vel_index:-2])
    return ([rechargers,depots,customers,fuel_cap,load_cap,cons_rate,refuel_rate,vel])

    
    print(fuel_cap)
    

        
