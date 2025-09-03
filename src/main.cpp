#include <iostream>
#include <string>
#include <vector>
#include "vertex.hpp"
#include "readInstance.hpp"
#include "calculateDistances.hpp"
#include "nearestNeighbour.hpp"
#include "routingOptimization.hpp"
using namespace std;

const float rho = 0.98;
const float alpha = 1;
const float bbeta = 2;
const int numberIterations = 5000;

int main(int argc, char *argv[])
{
    string instanceFile = argv[1];

    cout << "File name is " << instanceFile << endl;
    vector<Vertex> rechargers, depots, customers;
    float fuelCap, loadCap, consRate, refuelRate, vel;
    readInstance(rechargers, depots, customers, fuelCap, loadCap, consRate, refuelRate, vel, instanceFile);
    int vertexCount = depots.size() + rechargers.size() + customers.size();

    vector<Vertex> allVertexes{};
    allVertexes.insert(allVertexes.end(), depots.begin(), depots.end());
    allVertexes.insert(allVertexes.end(), rechargers.begin(), rechargers.end());
    allVertexes.insert(allVertexes.end(), customers.begin(), customers.end());

    // Pre-Calculate all distances
    vector<vector<float>> distances;
    calculateDistances(allVertexes, distances);

    float initialCost = NearestNCost(distances, vertexCount);
    // for (int i = 0; i < vertexCount ; i++){
    //     for (int j = 0 ; j < vertexCount; j++){
    //         cout << i << " "  << j << " " << distances[i][j] << endl;
    //     }
    // }
    // cout << vertexCount;

    // Initate routing(integer) and charging(0-1) population
    int populationSizeN = customers.size();
    vector<vector<int>> routingPopulation(populationSizeN);
    vector<vector<bool>> chargingPopulation(populationSizeN);

    vector<vector<float>> pheromoneMatrix;
    float initialMaxPhero = 1 / ((1 - rho) * initialCost);
    for (int i = 0; i < vertexCount; i++)
    {
        pheromoneMatrix.push_back({});
        for (int j = 0; j < vertexCount; j++)
        {
            pheromoneMatrix[i].push_back(((i != j) ? initialMaxPhero : 0));
        }
    }

    vector<vector<int>> eliteSolutionSet{};

    for (int iteration = 0; iteration < numberIterations; iteration++)
    {
        vector<bool> pBestChargeScheme{};
        vector<int> bestRouteAnt;

        routingOptimization(pheromoneMatrix, depots, customers, rechargers, distances, vertexCount, routingPopulation, allVertexes, bestRouteAnt, pBestChargeScheme, alpha, bbeta);
    }
    cout << "It didn't die" << endl;

    // cout << rechargers[0].x << endl;
    // cout << fuelCap << " " << loadCap << " " << consRate << " " << refuelRate << " " << vel;

    // ATUALIZAR FEROMONIOS A CADA CICLO
}