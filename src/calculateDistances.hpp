#ifndef CALCULATEDISTANCES_H
#define CALCULATEDISTANCES_H
#include <vector>
#include "vertex.hpp"
using namespace std;

float dist(float x1,float y1, float x2, float y2);

void calculateDistances(vector<Vertex> &depots, vector<Vertex> &rechargers, vector<Vertex> &customers,
                  vector<vector<float>> &distances);
#endif