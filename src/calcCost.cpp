
#include <vector>
#include "iostream"
// #include "vertex.hpp"
using namespace std;

float calcCost(vector<vector<float>> &distances,vector<int> &vertices){
    float cost = 0;
    // for (int i = 0; i < vertices.size();i++){
    //     cout << vertices[i] << " ";
    // }
    for (int i = 0; i < vertices.size()-1;i++){
        cost+=distances[vertices[i]][vertices[i+1]];
    }
    return cost;
}
