# Interaction-Enhanced Co-evolutionary algorithm for Reduced Energy Consumption in Electric Vehicle Routing

A Python implementation of the interaction-enhanced co-evolutionary algorithm for electric vehicle routing, based on the work of [Shouliang Zhu and Chao Zang](https://www.sciencedirect.com/science/article/abs/pii/S1568494624008871), simplified and modified with a focus on low energy consumption.

Numpy is required, it can by installed with `pip install numpy`

The program utilizes the following parameters
|Parameter| Description|
|---------|------------|
|-file|E-VRPTW instance file (_required_)|
|-rho|permanence rate of ant-colony pheromones (0.98 by default)|
|-alpha|weight of pheromones on routing decisions (1 by default)|
|-beta|weight of node distancs on routing decisions (2 by default)|
|-it|number of iterations to be run (5000 by default)|
|-pop|maximum size of the utilized ant populations (note that, regardless of this value, the number of ants will never exceed the number of customers in an instance)|
|-outfile|location and name of output JSON file (output.json by default)|

The program may be minimally run with

```
python <path-to-project>/source/main.py -file <path-to-instance>/<instance_name>.txt
```

Dataset source:
Goeke, Dominik (2019), “E-VRPTW instances”, Mendeley Data, V1, doi: 10.17632/h3mrm5dhxw.1
