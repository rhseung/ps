//
// Created by Hyunseung Ryu on 2025. 8. 9..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

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

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    ull ret = 0;
    for (int i = 2; i <= n; ++i) {
        ret += phi(i);
    }

    cout << ret << endl;

    return 0;
}
