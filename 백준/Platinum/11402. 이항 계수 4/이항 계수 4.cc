#include <bits/stdc++.h>
#include <ranges>

#define endl '\n'
#define setup ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout << fixed; cout.precision(6);
using namespace std;
using lnt = long long int;
using uint = unsigned int;

lnt power(lnt n, int p, int mod) {
    if (p == 0) return 1;
    else if (p == 1) return n;

    lnt x = (power(n, p / 2, mod) % mod) * (power(n, p / 2, mod) % mod) % mod;
    if (p % 2 == 0) return x;
    else return (x * n) % mod;
}

lnt combination(lnt n, lnt r, int mod) {
    if (r == 0) return 1;
    else if (n == r) return 1;
    else {
        lnt ret = 1;
        for (lnt i = 1; i <= r; i++) {
            ret = (ret * (n - i + 1)) % mod;
            ret = (ret * power(i, mod - 2, mod)) % mod;
        }
        return ret;
    }
}

deque<lnt> seperate(lnt n, int p) {
    deque<lnt> ret;
    while (n > 0) {
        ret.push_back(n % p);
        n /= p;
    }
    return ret;
}

int main() { setup;
    lnt n, k;
    int m;
    cin >> n >> k >> m;

    deque<lnt> n_s = seperate(n, m);
    deque<lnt> k_s = seperate(k, m);

    lnt ret = 1;

    // n_s, k_s 출력
//    cout << "n_s: ";
//    for (auto i: n_s) cout << i << " ";
//    cout << endl << "k_s: ";
//    for (auto i: k_s) cout << i << " ";
//    cout << endl;

    for (int i = 0; i < min(n_s.size(), k_s.size()); ++i) {
        ret = (ret % m * combination(n_s[i], k_s[i], m) % m) % m;
    }

    cout << ret << endl;

    return 0;
}