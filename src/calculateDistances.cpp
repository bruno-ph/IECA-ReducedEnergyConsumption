#include "calculateDistances.hpp"
#include <vector>
#include "vertex.hpp"
#include <math.h>
using namespace std;

float dist(float x1,float y1, float x2, float y2){
    float tmp = ((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1));
    return (sqrt(tmp));
}

void calculateDistances(vector<Vertex> &depots, vector<Vertex> &rechargers, vector<Vertex> &customers,
    vector<vector<float>> &distances){
        vector<Vertex> allVertexes {};
        allVertexes.insert(allVertexes.end(),depots.begin(),depots.end());
        allVertexes.insert(allVertexes.end(),rechargers.begin(),rechargers.end());
        allVertexes.insert(allVertexes.end(),customers.begin(),customers.end());
        for (int i = 0; i < allVertexes.size() ; i++){
            distances.push_back({});
            for (int j = 0 ; j < allVertexes.size(); j++){
                if (i==j){
                    distances[i].push_back(0.0);
                } else {
                    distances[i].push_back(dist(allVertexes[i].x,allVertexes[i].y,allVertexes[j].x,allVertexes[j].y));
                }

            }

        }
    }