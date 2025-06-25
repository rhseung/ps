cmake_minimum_required(VERSION 3.31)
project(ps)

set(CMAKE_CXX_STANDARD 20)

include_directories(algorithms)

add_executable(ps
        main.cpp
)
