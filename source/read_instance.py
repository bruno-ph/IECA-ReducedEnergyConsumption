
fuel_cap_index = 30
load_cap_index = 25
cons_rate_index = 25
refuel_rate_index = 26
vel_index = 20

def ReadInstance(instanceFile):
    file = open(instanceFile,"r")
    filelines=file.readlines()
    ids, types,pos,demands,ready_times,due_dates,service_times = [[],[],[],[],[],[],[]]
    recharger_count,depots_count,customer_count = 0,0,0
    for line in filelines[1:-6]:
        id, type,x,y, demand,ready_time,due_date,service_time =line.split()
        ids.append(id)
        types.append(type)
        pos.append((float(x),float(y)))
        demands.append(float(demand))
        ready_times.append(float(ready_time))
        due_dates.append(float(due_date))
        service_times.append(float(service_time))

        match type:
            case "f":
                recharger_count+=1
            case "c":
                customer_count+=1
            case "d":
                depots_count+=1
    fuel_cap = float(filelines[-5][fuel_cap_index:-2])
    load_cap = float(filelines[-4][load_cap_index:-2])
    cons_rate=float(filelines[-3][cons_rate_index:-2])
    refuel_rate=float(filelines[-2][refuel_rate_index:-2])
    vel=float(filelines[-1][vel_index:-2])
    return ([ids, types,pos,demands,ready_times,due_dates,service_times,recharger_count,depots_count,customer_count,fuel_cap,load_cap,cons_rate,refuel_rate,vel])

    
    print(fuel_cap)
    

        
