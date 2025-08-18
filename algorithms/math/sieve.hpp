//
// Created by Hyunseung Ryu on 2025. 8. 18..
//

#ifndef PS_SIEVE_HPP
#define PS_SIEVE_HPP

#include <vector>
using ull = unsigned long long int;

namespace math {
    /**
     * 에라토스테네스 체입니다. 시간 복잡도 O(N log log N).
     * @note
     * @param lim
     * @return
     */
    inline std::vector<bool> sieve(const std::size_t lim) {
        std::vector<bool> sieve(lim + 1, true);
        sieve[0] = false;
        if (lim >= 1)
            sieve[1] = false;

        for (std::size_t i = 2; i * i <= lim; ++i) {
            if (sieve[i]) {
                for (std::size_t j = i * i; j <= lim; j += i) {
                    sieve[j] = false;
                }
            }
        }

        return sieve;
    }

    inline std::vector<ull> primes_up_to(const std::size_t lim) {
        auto is_prime = sieve(lim);

        std::vector<ull> primes;
        for (std::size_t i = 2; i <= lim; ++i) {
            if (is_prime[i]) {
                primes.push_back(i);
            }
        }

        return primes;
    }
}

#endif //PS_SIEVE_HPP
