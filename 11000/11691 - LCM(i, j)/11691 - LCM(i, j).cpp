// BOJ 11691 - LCM(i, j)
#include <ios>
#include <iostream>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

constexpr ll MOD = 1000000007;

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

ll F(ll x) {
    ll ret = 0;
    for (ll i = 2; i <= x; ++i) {
        ret += i * i * phi(i) / 2;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n;
    cin >> n;



    return 0;
}
