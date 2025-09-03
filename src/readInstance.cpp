#include <vector>
#include "vertex.hpp"
#include "readInstance.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
using namespace std;

// Parameters are read at specific collumns in the last line of instance file
const int fuelCapIndex = 30;
const int loadCapIndex = 25;
const int consRateIndex = 25;
const int refuelRateIndex = 26;
const int velIndex = 20;

// Reads a instance file and passes data to program structures via reference
// Dataset: https://data.mendeley.com/datasets/h3mrm5dhxw/1
void readInstance(vector<Vertex> &rechargers, vector<Vertex> &depots, vector<Vertex> &customers,
                  float &fuelCap,
                  float &loadCap, float &consRate,
                  float &refuelRate,
                  float &vel,
                  string filename)
{
    std::ifstream file(filename);
    string line;
    getline(file, line);
    getline(file, line);
    string idStr, typeStr, xStr, yStr, demandStr, readyStr, dueStr, serviceStr;
    int counter = 0;
    while (!line.empty())
    {
        stringstream ss(line);

        ss >> idStr;
        ss >> typeStr;
        ss >> xStr;
        ss >> yStr;
        ss >> demandStr;
        ss >> readyStr;
        ss >> dueStr;
        ss >> serviceStr;
        Vertex v = {stof(xStr), stof(yStr), stof(demandStr), stof(readyStr), stof(dueStr), stof(serviceStr), counter, idStr, typeStr};
        counter++;
        if (typeStr == "f")
        {
            rechargers.push_back(v);
        }
        else if (typeStr == "d")
        {
            depots.push_back(v);
        }
        else if (typeStr == "c")
        {
            customers.push_back(v);
        }
        cout << counter << ": " << v.number << endl;
        getline(file, line);
    }
    getline(file, line);
    fuelCap = stof(line.substr(fuelCapIndex));
    getline(file, line);
    loadCap = stof(line.substr(loadCapIndex));
    getline(file, line);
    consRate = stof(line.substr(consRateIndex));
    getline(file, line);
    refuelRate = stof(line.substr(refuelRateIndex));
    getline(file, line);
    vel = stof(line.substr(velIndex));
    // cout << fuelCap << " " << loadCap << " " << consRate << " " << refuelRate << " " << vel << endl;
    return;
}