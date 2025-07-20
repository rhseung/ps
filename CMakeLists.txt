cmake_minimum_required(VERSION 3.31)
project(ps)

set(CMAKE_CXX_STANDARD 20)

add_executable(ps
        algorithms/graph.hpp
        algorithms/math.hpp
        "24000/24480 - 알고리즘 수업 - 깊이 우선 탐색 2 - 2.cpp"
)
