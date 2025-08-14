//
// Created by Hyunseung Ryu on 2025. 8. 14..
//

#ifndef PS_WEIGHTED_EDGE_HPP
#define PS_WEIGHTED_EDGE_HPP

#include <type_traits>

namespace graph {
    template <typename T> requires std::is_integral_v<T> || std::is_floating_point_v<T>
    struct Edge {
        T weight;
        int from, to;

        bool operator<(const Edge& other) const {
            return weight < other.weight || (weight == other.weight && (from < other.from || (from == other.from && to < other.to)));
        }
    };
}

#endif //PS_WEIGHTED_EDGE_HPP
