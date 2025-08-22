#include <string>
#ifndef VERTEX_H
#define VERTEX_H
struct Vertex
{
    float x;
    float y;
    float demand;
    float readyTime;
    float dueTime;
    float serviceTimes;
    std::string id;
    std::string type;
};
#endif