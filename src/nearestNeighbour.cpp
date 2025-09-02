#include <vector>
#include "vertex.hpp"
#include <random>
#include <algorithm>
#include <cfloat>
#include "calculateDistances.hpp"
#include "calcCost.hpp"
#include "iostream"
using namespace std;

float NearestNCost(vector<vector<float>> &distances, int vertexCount){
    vector<int> unvistedVertices(vertexCount);
    vector<int> visitedVertices {};
    iota(unvistedVertices.begin(),unvistedVertices.end(),0);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> randRange(0, vertexCount-1);

    int initialValue = randRange(gen);
    auto iter = find(unvistedVertices.begin(),unvistedVertices.end(),initialValue);
    unvistedVertices.erase(iter);

    int utilizedCount = 1;
    visitedVertices.push_back(initialValue);

    while (utilizedCount!=vertexCount){
        float bestDist = FLT_MAX;
        vector<int>::iterator bestIter;
        for (vector<int>::iterator it = unvistedVertices.begin();it!=unvistedVertices.end();++it){
            if (distances[visitedVertices.back()][*it] < bestDist){
                bestDist = distances[visitedVertices.back()][*it];
                bestIter = it;
            }
        }
        if (bestDist!=FLT_MAX){
            utilizedCount++;
            visitedVertices.push_back(*bestIter);
            unvistedVertices.erase(bestIter);
        }
    }

    return (calcCost(distances,visitedVertices));
}