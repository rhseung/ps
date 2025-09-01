//
// Created by Hyunseung Ryu on 2025. 8. 9..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

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

    // gcd(f_k, f_n) = f_gcd(k, n) = 1 => gcd(k, n) = 1 or 2
    // gcd(k, n) = 1인 k 개수: phi(n)
    // gcd(k, n) = 2인 k 개수: n이 홀수면 0개, n이 짝수면 phi(n / 2)개

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        // 1은 자기 자신과 서로소라서 phi(1) = 1이 나오는 걸 잘 체크해야함
        const auto phi_1 = n != 1 ? phi(n) : 0;
        const auto phi_2 = n % 2 == 0 ? (n != 2 ? phi(n / 2) : 0) : 0;
        cout << (phi_1 + phi_2) << endl;
    }

    return 0;
}
