// BOJ 1557 - 제곱 ㄴㄴ
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

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

// https://math.stackexchange.com/questions/20529/fast-method-for-nth-squarefree-number-using-mathematica
// mu[x] != 0이면 x는 sqf이다를 이용해서 O(N)으로 구할 수 있다. 그러나 아래와 같이 하면 O(sqrt(N)).
ll count_sqf(const ll x, const vector<int>& mu) {
    ll cnt = 0;
    for (size_t i = 1; i * i <= x; ++i) {
        cnt += mu[i] * (x / (i * i));
    }
    return cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int k;
    cin >> k;

    // sqrt(INT_MAX) <= 46340
    auto mu = mobius_sieve(46340);

    ll l = 1, r = 2 * k + 1000;
    while (l < r) {
        const ll mid = (l + r) / 2;
        if (count_sqf(mid, mu) < k)
            l = mid + 1;
        else
            r = mid;
    }

    cout << l << endl;

    return 0;
}
