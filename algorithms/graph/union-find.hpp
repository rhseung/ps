#ifndef UNION_FIND_HPP
#define UNION_FIND_HPP

#include <vector>

// https://4legs-study.tistory.com/94?category=886581

namespace graph {
    // 경로 압축 최적화 적용됨
    inline int find_root(std::vector<int>& parents, const int x) {
        if (x == parents[x]) return x;
        return parents[x] = find_root(parents, parents[x]);
    }

    inline void union_root(std::vector<int>& parents, int x, int y) {
        x = find_root(parents, x);
        y = find_root(parents, y);

        if (x != y) {
            parents[x] = y;
        }
    }

    // union by rank 최적화 적용됨
    inline void union_root_fast(std::vector<int>& parents, std::vector<int>& ranks, int x, int y) {
        x = find_root(parents, x);
        y = find_root(parents, y);

        if (x != y) {
            if (ranks[x] < ranks[y])
                parents[x] = y;
            else if (ranks[x] > ranks[y])
                parents[y] = x;
            else {
                parents[y] = x;
                ranks[x]++;
            }
        }
    }
}

#endif
