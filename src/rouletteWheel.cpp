#include "rouletteWheel.hpp"
#include <vector>
#include "vertex.hpp"
#include <cmath>
#include <limits>
#include <random>
#include "iostream"
using namespace std;
int RouletteWheel(vector<Vertex> nodes, int origin, vector<vector<float>> &distances,
                  float alpha, float beta, vector<vector<float>> &pheromoneMatrix)
{

    vector<float> chances{};
    float sum = 0;
    cout << "\nnodes.size" << nodes.size() << endl;
    for (int j = 0; j < nodes.size(); j++)
    {
        cout << "origin and number: " << origin << " " << nodes[j].number << endl;
        cout << "is it zero " << pow(distances[origin][nodes[j].number], beta) << endl;
        float p = pow(pheromoneMatrix[origin][nodes[j].number], alpha) / pow(distances[origin][nodes[j].number], beta);
        cout << "p: " << p << endl;
        if (isnan(p))
            p = 1e-8;
        if (isinf(p))
        {
            if (origin == nodes[j].number)
            {
                p = 1e-8;
            }
            else
            {
                p = sum;
            };
        }
        chances.push_back(sum + p);
        sum += p;
    }
    random_device rd;
    mt19937 generator(rd());
    uniform_real_distribution<float> distribution(0.0, sum);
    float randomSpot = distribution(generator);
    cout << "sum=" << sum << endl;
    cout << "random spot=" << randomSpot << endl
         << "random chances:";
    for (int i = 0; i < chances.size(); i++)
    {
        cout << chances[i] << " ";
    }
    int j = 0;
    for (; j < chances.size(); j++)
    {

        if (randomSpot <= chances[j])
        {
            cout << j << "about to break\n";
            break;
        }
    }
    return j;
}