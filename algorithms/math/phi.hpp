//
// Created by Hyunseung Ryu on 2025. 8. 9..
//

#ifndef PS_PHI_HPP
#define PS_PHI_HPP

namespace math {
    inline std::size_t phi(std::size_t n) {
        std::size_t result = n;

        for (std::size_t i = 2; i * i <= n; ++i) {
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
