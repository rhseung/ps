// BOJ 9267 - A+B
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

/**
 * 유클리드 호제법
 * @param a
 * @param b
 * @return gcd(a, b)
 */
inline ll gcd(const ll a, const ll b) {
    if (b == 0)
        return a;

    return gcd(b, a % b);
}

/**
 * 확장 유클리드 호제법, Extended Euclidean Algorithm (EEA)
 * @param a
 * @param b
 * @return ax + by = gcd(a, b) 를 만족하는 (x, y, gcd(a, b)) 튜플
 *  => Ax + By = C 형태의 방정식에서 A, B, C가 주어졌을 때 x, y를 구할 수 있음.
 * where C % gcd(A, B) == 0
 */
inline tuple<ll, ll, ll> extended_gcd(const ll a, const ll b) {
    if (a == b)
        return {1, 0, a};
    if (b == 0)
        return {1, 0, a};

    ll x_1 = 1, y_1 = 0, r_1 = a;
    ll x_2 = 0, y_2 = 1, r_2 = b;

    while (r_2 != 0) {
        const ll q = r_1 / r_2;

        const ll r_t = r_1 - q * r_2;
        const ll x_t = x_1 - q * x_2;
        const ll y_t = y_1 - q * y_2;

        x_1 = x_2;
        y_1 = y_2;
        r_1 = r_2;
        x_2 = x_t;
        y_2 = y_t;
        r_2 = r_t;
    }

    return {x_1, y_1, r_1};
}

inline __int128 iabs128(__int128 v) {
    return v < 0 ? -v : v;
}

inline __int128 gcd128(__int128 a, __int128 b) {
    a = iabs128(a);
    b = iabs128(b);
    while (b) {
        __int128 t = a % b;
        a = b;
        b = t;
    }
    return a;
}

inline __int128 div_floor128(__int128 a, __int128 b) {
    // floor(a / b) for signed 128-bit (b != 0)
    assert(b != 0);
    __int128 q = a / b;
    __int128 r = a % b;
    if (r != 0 && ((r > 0) != (b > 0))) --q;
    return q;
}

inline __int128 div_ceil128(__int128 a, __int128 b) {
    // ceil(a / b) for signed 128-bit (b != 0)
    assert(b != 0);
    __int128 q = a / b;
    __int128 r = a % b;
    if (r != 0 && ((r > 0) == (b > 0))) ++q;
    return q;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll a, b, s;
    cin >> a >> b >> s;

    if (s == 0) {
        cout << ((a > 0 && b > 0) ? "NO" : "YES") << endl;
        return 0;
    }

    if (a == 0 && b == 0) {
        cout << (s == 0 ? "YES" : "NO") << endl;
        return 0;
    }

    auto [x0, y0, g] = extended_gcd(a, b);
    if (s % g != 0) {
        cout << "NO" << endl;
        return 0;
    }

    const ll sg = s / g;
    __int128 X0 = (__int128)x0 * sg;
    __int128 Y0 = (__int128)y0 * sg;

    const __int128 step_x = (__int128)(b / g);
    const __int128 step_y = (__int128)(a / g);

    __int128 k_min, k_max;
    if (step_x == 0 && step_y == 0) {
        if (s != 0) {
            cout << "NO" << endl;
            return 0;
        }
        if (X0 < 0 || Y0 < 0) {
            cout << "NO" << endl;
            return 0;
        }
        cout << (gcd128(X0, Y0) == 1 ? "YES" : "NO") << endl;
        return 0;
    }
    if (step_x == 0) {
        if (X0 < 0) {
            cout << "NO" << endl;
            return 0;
        }
        k_min = 0;
        k_max = div_floor128(Y0, step_y);
    }
    else if (step_y == 0) {
        if (Y0 < 0) {
            cout << "NO" << endl;
            return 0;
        }
        __int128 d = gcd128(step_x, Y0);
        cout << ((gcd128(X0, d) == 1) ? "YES" : "NO") << endl;
        return 0;
    }
    else {
        k_min = div_ceil128(-X0, step_x);
        k_max = div_floor128(Y0, step_y);
    }

    if (k_min <= k_max) {
        bool found = false;

        for (__int128 k = k_min; k <= k_max; ++k) {
            const __int128 x = X0 + k * step_x;
            const __int128 y = Y0 - k * step_y;
            if (x < 0 || y < 0) continue;
            if (gcd128(x, y) == 1) {
                found = true;
                break;
            }
        }

        if (found) {
            cout << "YES" << endl;
        }
        else {
            cout << "NO" << endl;
        }
    }
    else {
        cout << "NO" << endl;
    }

    return 0;
}
