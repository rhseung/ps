// BOJ 11439 - 이항 계수 5
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

inline ll modpow(ll a, ll b, const ll c) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = ret * a % c;
        b >>= 1;
        a = a * a % c;
    }
    return ret;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n, k, m;
    cin >> n >> k >> m;

    const auto sieve = new bool[n + 1];
    sieve[0] = true;
    sieve[1] = true;

    for (ll i = 2; i * i <= n; ++i) {
        if (!sieve[i]) {
            for (ll j = i * 2; j <= n; j += i) {
                sieve[j] = true;
            }
        }
    }

    vector<ll> primes;
    for (ll i = 2; i <= n; ++i) {
        if (!sieve[i]) {
            primes.push_back(i);
        }
    }

    unordered_map<ll, ll> prime_factors;
    for (const ll i : primes) {
        for (ll j = i; j <= n; j *= i) {
            // nCk = n! / (k! * (n - k)!) 에서 i라는 소인수의 개수, i, i^2, i^3, ...의 배수로 나누어 떨어지는 개수를 구함
            const ll power = (n / j) - (k / j) - ((n - k) / j);
            if (power == 0) continue;

            if (!prime_factors.contains(i))
                prime_factors[i] = 0;
            prime_factors[i] += power;
        }
    }

    ll res = 1;
    for (const auto& [prime, count] : prime_factors) {
        res = res * modpow(prime, count, m) % m;
        if (res == 0) {
            break;
        }
    }

    cout << res << endl;

    delete[] sieve;
};
