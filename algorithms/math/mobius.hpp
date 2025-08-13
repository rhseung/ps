//
// Created by Hyunseung Ryu on 2025. 8. 13..
//

#ifndef PS_MOBIUS_HPP
#define PS_MOBIUS_HPP
#include "factor.hpp"

using ll = long long int;
using ull = unsigned long long int;

namespace math {
    /**
     * μ(n)를 구하는 함수.
     * @return
     *  <b>1</b>  if n == 1 <br>
     *  <b>0</b>  if n의 소인수에 제곱이 포함 <br>
     *  <b>-1</b> if n은 소인수 제곱이 없고, 소인수 개수가 홀수 <br>
     *  <b>1</b>  if n은 소인수 제곱이 없고, 소인수 개수가 짝수 <br>
     */
    inline int mobius_single(const ull n) {
        if (n == 1) return 1;
        auto fp = factor_pair(n);
        for (const auto& pe : fp) {
            if (pe.second >= 2) return 0;
        }
        const int k = static_cast<int>(fp.size());
        return k % 2 == 0 ? 1 : -1; // (-1)^k
    }

    /**
     * 선형 체를 이용하여 μ(1..N)을 O(N) 시간에 구하는 함수.
     * mu[0]은 사용되지 않으며, 1...N에 대해 유효합니다.
     */
    inline std::vector<int> mobius_sieve(const ull N) {
        std::vector<int> mu(N + 1, 0);
        std::vector<ull> least_prime_of(N + 1, 0); // least_prime_of[i] == i의 최소 소인수
        std::vector<ull> primes; // 소수 목록
        mu[1] = 1;

        for (std::size_t i = 2; i <= N; ++i) {
            if (least_prime_of[i] == 0) { // i는 소수
                least_prime_of[i] = i;
                primes.push_back(i);
                mu[i] = -1; // μ(p) = -1 왜냐면 p는 소수이므로 소인수 개수가 1개이고 제곱이 없기 때문
            }

            for (const ull p : primes) {
                const ull x = 1LL * p * i;
                if (x > N) break;
                least_prime_of[x] = p;

                if (p == least_prime_of[i]) {
                    mu[x] = 0; // p | i → p^2 | pi → p^2 | x
                    break;
                }
                else {
                    mu[x] = -mu[i]; // 새 소수 p를 하나 더 붙였으니 부호 반전
                }
            }
        }

        return mu;
    }

    /**
     * Mertens prefix M(n) = sum_{k<=n} μ(k). Input mu must be size >= N+1 with mu[0] unused.
     */
    inline std::vector<ll> mertens_from_mu(const std::vector<int>& mu) {
        std::vector<ll> M(mu.size(), 0);
        for (size_t i = 1; i < mu.size(); ++i) M[i] = M[i - 1] + mu[i];
        return M;
    }
}

#endif //PS_MOBIUS_HPP
