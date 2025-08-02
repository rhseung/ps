cmake_minimum_required(VERSION 3.31)
project(ps)

set(CMAKE_CXX_STANDARD 20)

add_executable(ps
        algorithms/graph.hpp
        algorithms/math.hpp
        algorithms/search.hpp
        "12000/12781 - PIZZA ALVOLOC.cpp"
)
