//
// Created by Hyunseung Ryu on 2025. 8. 9..
//

#ifndef PS_PHI_HPP
#define PS_PHI_HPP

using ll = long long int;
using ull = unsigned long long int;

namespace math {
    /**
     * 오일러 피 함수, 1부터 n까지의 수 중에서 n과 서로소인 수의 개수, O(sqrt(n)).
     * @param n
     * @return phi(n)
     */
    inline ll phi(ll n) {
        ll result = n;

        for (ll i = 2; i * i <= n; ++i) {
            if (n % i == 0) {
                result -= result / i;
                while (n % i == 0) n /= i;
            }
        }

        if (n > 1)
            result -= result / n;

        return result;
    }
}

#endif //PS_PHI_HPP
