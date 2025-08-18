// BOJ 1644 - 소수의 연속합
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

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

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    const auto primes = primes_up_to(n);
    vector<ull> primes_acc(primes.size() + 1);
    for (std::size_t i = 0; i < primes.size(); ++i) {
        primes_acc[i + 1] = primes_acc[i] + primes[i];
    }

    int cnt = 0;
    ull l = 0, r = 0;
    while (l <= r) {
        ull sum = primes_acc[r + 1] - primes_acc[l];

        if (sum < n) {
            r += 1;
        }
        else if (sum > n) {
            l += 1;
        }
        else {
            cnt++;
            r += 1;
        }
    }

    cout << cnt << endl;

    return 0;
}
