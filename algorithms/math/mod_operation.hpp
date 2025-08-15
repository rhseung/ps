//
// Created by Hyunseung Ryu on 2025. 8. 13..
//

#ifndef PS_MOD_OPERATION_HPP
#define PS_MOD_OPERATION_HPP

using ll = long long int;
using ull = unsigned long long int;

// https://github.com/kth-competitive-programming/kactl/blob/main/content/number-theory/ModMulLL.h

namespace math {
    inline ull modmul(const ull a, const ull b, const ull M) {
        const ll ret = a * b - M * static_cast<ull>(1.L / M * a * b);
        return ret + M * (ret < 0) - M * (ret >= static_cast<ll>(M));
    }

    inline ull modpow(ull b, ull e, const ull M) {
        ull ans = 1;
        for (; e; b = modmul(b, b, M), e /= 2)
            if (e & 1) ans = modmul(ans, b, M);
        return ans;
    }

    inline ll modpow(ll a, ll b, const ll c) {
        ll ret = 1;
        while (b) {
            if (b & 1) ret = ret * a % c;
            b >>= 1;
            a = a * a % c;
        }
        return ret;
    }

    inline int modpow(int a, int b, const int c) {
        int ret = 1;
        while (b) {
            if (b & 1) ret = ret * a % c;
            b >>= 1;
            a = a * a % c;
        }
        return ret;
    }
}

#endif //PS_MOD_OPERATION_HPP
