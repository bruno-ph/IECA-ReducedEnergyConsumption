#include <iostream>
#include <string>
#include <vector>
#include "vertex.hpp"
#include "readInstance.hpp"
using namespace std;

int main(int argc, char *argv[])
{
    string instanceFile = argv[1];
    cout << "File name is " << instanceFile << endl;
    vector<Vertex> rechargers, depots, customers;
    float fuelCap, loadCap, consRate, refuelRate, vel;
    readInstance(rechargers, depots, customers, fuelCap, loadCap, consRate, refuelRate, vel, instanceFile);
    // cout << rechargers[0].x << endl;
    // cout << fuelCap << " " << loadCap << " " << consRate << " " << refuelRate << " " << vel;
}