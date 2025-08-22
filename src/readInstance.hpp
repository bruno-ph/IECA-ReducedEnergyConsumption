#ifndef READINSTANCE_H
#define READINSTANCE_H
#include <vector>
#include <string>
#include "vertex.hpp"
using namespace std;

void readInstance(vector<Vertex> &rechargers, vector<Vertex> &depots, vector<Vertex> &customers,
                  float &fuelCap,
                  float &loadCap, float &consRate,
                  float &refuelRate,
                  float &vel,
                  std::string filename);
#endif