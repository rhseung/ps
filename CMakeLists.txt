cmake_minimum_required(VERSION 3.31)
project(ps)

set(CMAKE_CXX_STANDARD 20)

add_executable(ps
    "algorithms/graph.hpp"
    "algorithms/math.hpp"
    "algorithms/search.hpp"
    "algorithms/math/berlekamp_massey.hpp"
    "algorithms/graph/kruskal.hpp"
    "algorithms/graph/prim.hpp"
    "algorithms/graph/weighted_edge.hpp"
)
