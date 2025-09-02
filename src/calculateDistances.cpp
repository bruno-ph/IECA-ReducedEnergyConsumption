#include "calculateDistances.hpp"
#include <vector>
#include "vertex.hpp"
#include <math.h>
using namespace std;

float dist(Vertex a, Vertex b){
    return dist(a.x,a.y,b.x,b.y);
}

float dist(float x1,float y1, float x2, float y2){
    float tmp = ((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1));
    return (sqrt(tmp));
}

void calculateDistances(vector<Vertex> &allVertexes,
    vector<vector<float>> &distances){
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