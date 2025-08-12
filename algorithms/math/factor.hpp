//
// Created by Hyunseung Ryu on 2025. 8. 13..
//

#ifndef PS_FACTOR_HPP
#define PS_FACTOR_HPP

#include <map>
#include <ranges>
#include <__numeric/gcd_lcm.h>
#include "mod_operation.hpp"

using ll = long long int;
using ull = unsigned long long int;

// https://github.com/kth-competitive-programming/kactl/blob/main/content/number-theory/Factor.h

namespace math {
    /**
     * Pollard's rho 알고리즘을 사용하여 n의 소인수 중 하나를 찾습니다.
     * 이 알고리즘은 n이 합성수일 때 작동하며, n이 소수일 경우에는 실패할 수 있습니다.
     * 따라서 이 함수를 사용하기 전에 `is_prime_fast` 함수를 사용하여 n이 소수인지 확인하는 것이 좋습니다.
     * @param n
     * @return n의 1도 아니고 n도 아닌 소인수 중 하나
     */
    inline ull pollard(const ull n) {
        ull x = 0, y = 0, t = 30, prd = 2, i = 1, q;
        auto f = [&](const ull x_) {
            return modmul(x_, x_, n) + i;
        };

        while (t++ % 40 || __gcd(prd, n) == 1) {
            if (x == y) x = ++i, y = f(x);
            if ((q = modmul(prd, max(x, y) - min(x, y), n))) prd = q;
            x = f(x), y = f(f(y));
        }

        return __gcd(prd, n);
    }

    /**
     * n의 소인수를 찾습니다.
     * 이 함수는 Pollard's rho 알고리즘을 사용하여 n의 소인수 중 하나를 찾고,
     * 재귀적으로 나머지 소인수를 찾습니다
     * @param n
     * @return n의 소인수들의 벡터 (정렬되어 있지 않습니다)
     */
    inline vector<ull> factor(const ull n) {
        if (n <= 1) return {};
        if (is_prime_fast(n)) return {n};

        const ull x = pollard(n);
        auto l = factor(x), r = factor(n / x);
        l.insert(l.end(), r.begin(), r.end());

        return l;
    }

    /**
     * n의 소인수와 그 개수를 맵 형태로 반환합니다.
     * 예를 들어, n = 12이면 {2: 2, 3: 1}을 반환합니다.
     * 이 함수는 `factor` 함수를 사용하여 n의 소인수를 찾고,
     * 각 소인수의 개수를 세어 맵에 저장합니다.
     * @param n
     * @return n의 소인수와 그 개수를 저장한 맵
     */
    inline map<ull, ull> factor_map(const ull n) {
        map<ull, ull> ret;
        for (const ull f : factor(n)) {
            if (!ret.contains(f))
                ret[f] = 0;
            ret[f]++;
        }

        return ret;
    }

    /**
     * n의 소인수와 그 개수를 쌍(pair) 형태로 반환합니다.
     * 예를 들어, n = 12이면 {(2, 2), (3, 1)}을 반환합니다.
     * 이 함수는 `factor_map` 함수를 사용하여 n의 소인수를 찾고,
     * 각 소인수와 그 개수를 쌍(pair)으로 만들어 벡터에 저장합니다.
     * @param n
     * @return n의 소인수와 그 개수를 저장한 벡터
     */
    inline vector<pair<ull, ull>> factor_pair(const ull n) {
        vector<pair<ull, ull>> ret;
        for (const auto& [factor, count] : factor_map(n)) {
            ret.emplace_back(factor, count);
        }
        return ret;
    }
}

#endif //PS_FACTOR_HPP
