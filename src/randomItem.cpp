#include "randomItem.hpp"
#include <random>
using namespace std;
int getRandomInt(int min, int max)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> randRange(min, max);
    int initialValue = randRange(gen);
    return initialValue;
}