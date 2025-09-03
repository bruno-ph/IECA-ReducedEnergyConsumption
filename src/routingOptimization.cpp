#include "routingOptimization.hpp"
#include <vector>
#include "vertex.hpp"
#include "RouletteWheel.hpp"
#include "randomItem.hpp"
#include "iostream"
using namespace std;
void routingOptimization(vector<vector<float>> &pheromoneMatrix,
                         vector<Vertex> &depots, vector<Vertex> &customers, const vector<Vertex> &rechargers,
                         vector<vector<float>> &distances, int vertexCount, vector<vector<int>> &routingPopulation,
                         vector<Vertex> allVertexes, vector<int> &bestRouteAnt, vector<bool> &pBestChargeScheme,
                         float alpha, float beta)
{

    vector<Vertex> Nodes = allVertexes;
    cout << "vc:" << vertexCount << "And here's the numbers>\n"
         << endl;
    for (int i = 0; i < allVertexes.size(); i++)
    {
        cout << allVertexes[i].number << "  ";
    }
    for (int k = 1; k < vertexCount; k++)
    {
        cout << "k: " << k << endl;
        vector<int> rechargeUses(rechargers.size(), (2 * customers.size()));
        vector<Vertex> Nodes = allVertexes;
        for (int i = 0; i < Nodes.size(); i++)
        {
            cout << Nodes[i].number << "  ";
        }
        vector<int> route{};
        int randomNode = getRandomInt(0, Nodes.size() - 1);
        cout << "Random node was:" << randomNode << endl;
        cout << Nodes.size();
        cout << "random node number: " << Nodes[randomNode].number << endl;
        route.push_back(Nodes[randomNode].number);

        if (Nodes[randomNode].type == "f")
        {
            rechargeUses[randomNode - depots.size()]--;
            if (rechargeUses[randomNode - depots.size()] == 0)
            {
                Nodes.erase(Nodes.begin() + randomNode);
            }
        }
        else
        {
            Nodes.erase(Nodes.begin() + randomNode);
        }
        cout << "Entering roullete\n test: " << k << endl;
        while (!(Nodes.empty()))
        {
            cout << "route is:\n";
            for (int i = 0; i < route.size(); i++)
            {
                cout << route[i] << "  ";
            }
            cout << "ok?" << endl;
            cout << "nodes remaining is:\n";
            for (int i = 0; i < Nodes.size(); i++)
            {
                cout << Nodes[i].number << "  ";
            }
            cout << "ok?" << endl;
            int selected = RouletteWheel(Nodes, route.back(), distances, alpha, beta, pheromoneMatrix);
            cout << "\nselected:" << selected << " number:" << Nodes[selected].number << endl;
            route.push_back(Nodes[selected].number);
            if (Nodes[selected].type == "f")
            {
                rechargeUses[selected - depots.size()]--;
                if (rechargeUses[selected - depots.size()] == 0)
                {
                    Nodes.erase(Nodes.begin() + selected);
                    rechargeUses.erase(rechargeUses.begin() + selected);
                }
            }
            else
            {
                Nodes.erase(Nodes.begin() + selected);
            }
            for (int i = 0; i < route.size(); i++)
            {
                cout << route[i] << "  ";
            }
            cout << "still alive \n";
        }
        cout << "route:\n";
        for (int i = 0; i < route.size(); i++)
        {
            cout << route[i] << " ";
        }
    }
}