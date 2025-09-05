cmake_minimum_required(VERSION 3.31)
project(ps)

set(CMAKE_CXX_STANDARD 20)

add_executable(ps
    "algorithms/graph.hpp"
    "algorithms/math.hpp"
    "algorithms/search.hpp"
    "solving/14860 - GCD 곱/14860 - GCD 곱.cpp"
    "solving/10999 - 구간 합 구하기 2/10999 - 구간 합 구하기 2.cpp"
)
