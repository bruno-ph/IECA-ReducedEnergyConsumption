#include <iostream>
#include <string>
#include <vector>
#include "vertex.hpp"
#include "readInstance.hpp"
#include "calculateDistances.hpp"
using namespace std;


int main(int argc, char *argv[])
{
    string instanceFile = argv[1];
    int populationSizeN = stoi(argv[2]); //should maybe be the number of depots+customers+chargers
    cout << "File name is " << instanceFile << endl;
    vector<Vertex> rechargers, depots, customers;
    float fuelCap, loadCap, consRate, refuelRate, vel;
    readInstance(rechargers, depots, customers, fuelCap, loadCap, consRate, refuelRate, vel, instanceFile);
    int vertexCount = depots.size() + rechargers.size() + customers.size();

    //Calculate all distances
    vector<vector<float>> distances;
    calculateDistances(depots,rechargers,customers,distances);

    // for (int i = 0; i < vertexCount ; i++){
    //     for (int j = 0 ; j < vertexCount; j++){
    //         cout << i << " "  << j << " " << distances[i][j] << endl;
    //     }
    // }
    // cout << vertexCount;

    // Initate routing(integer) and charging(0-1) population
    // Probably shouldnt be zeroes, check later
    vector<int> routingPopulation(populationSizeN);
    vector<bool> chargingPopulation(populationSizeN);

    
    
    float pheromoneMatrix[vertexCount][vertexCount];

    // cout << rechargers[0].x << endl;
    // cout << fuelCap << " " << loadCap << " " << consRate << " " << refuelRate << " " << vel;
}