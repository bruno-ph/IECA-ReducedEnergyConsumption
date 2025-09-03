##g++ src/readInstance.cpp src/main.cpp -o iecaRun

CC = g++


all: src/randomItem.cpp src/rouletteWheel.cpp src/routingOptimization.cpp src/calcCost.cpp src/nearestNeighbour.cpp src/calculateDistances.cpp src/readInstance.cpp src/main.cpp
	$(CC) -o iecaRun src/main.cpp src/readInstance.cpp src/calculateDistances.cpp src/nearestNeighbour.cpp src/calcCost.cpp src/randomItem.cpp src/rouletteWheel.cpp src/routingOptimization.cpp