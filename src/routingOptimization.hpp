#ifndef ROUTINGOPTIMIZATION_H
#define ROUTINGOPTIMIZATION_H
#include <vector>
#include "vertex.hpp"
using namespace std;
void routingOptimization(vector<vector<float>> &pheromoneMatrix,
                         vector<Vertex> &depots, vector<Vertex> &customers, const vector<Vertex> &rechargers,
                         vector<vector<float>> &distances, int vertexCount, vector<vector<int>> &routingPopulation,
                         vector<Vertex> allVertexes, vector<int> &bestRouteAnt, vector<bool> &pBestChargeScheme,
                         float alpha, float beta);

#endif