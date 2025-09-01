##g++ src/readInstance.cpp src/main.cpp -o iecaRun

CC = g++


all: src/readInstance.cpp src/main.cpp
	$(CC) -o iecaRun src/main.cpp src/readInstance.cpp