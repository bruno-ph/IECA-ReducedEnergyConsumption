
#ifndef ROULETTE_H
#define ROULETTE_H
#include <vector>
#include "vertex.hpp"
using namespace std;
int RouletteWheel(vector<Vertex> nodes, int origin, vector<vector<float>> &distances,
                  float alpha, float beta, vector<vector<float>> &pheromoneMatrix);

#endif