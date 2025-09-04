class Vertex:
    def __init__(self,x,y,demand,ready_time,due_time,service_time,number,id,type):
        self.x=x
        self.y= y
        self.demand = demand
        self.ready_time = ready_time
        self.due_time = due_time
        self.service_time = service_time
        self.number = number
        self.id = id
        self.type = type
    
    def __str__(self):
        return f"({self.x,self.y}, D:{self.demand}kg, {self.ready_time}-{self.due_time} in {self.service_time}, {self.number},{self.id},{self.type})"
    
    def printself(self):
        print(f"({self.x,self.y}, D:{self.demand}kg, {self.ready_time}-{self.due_time} in {self.service_time}, {self.number},{self.id},{self.type})")