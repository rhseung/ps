#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

constexpr int MAX_N = 200000;

static ll vp_fact(ll n, const int p) {
    ll cnt = 0;
    while (n) {
        n /= p;
        cnt += n;
    }

    return cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    static int spf[MAX_N + 1];
    for (int i = 2; i <= MAX_N; ++i) {
        if (!spf[i]) {
            spf[i] = i;

            if (i * i <= MAX_N) {
                for (ll j = 1LL * i * i; j <= MAX_N; j += i) {
                    if (!spf[j]) spf[j] = i;
                }
            }
        }
    }

    int T;
    cin >> T;

    vector<int> Ns(T);
    int max_N = 0;
    for (int i = 0; i < T; ++i) {
        cin >> Ns[i];
        max_N = max(max_N, Ns[i]);
    }

    vector R(max_N + 1, 1);
    if (max_N >= 1) R[1] = 1; // (1!)^2 | 1! 이므로 K=1

    int k = 1;
    for (int i = 2; i <= max_N; ++i) {
        k = R[i - 1];
        int x = i;

        while (x > 1) {
            const int p = spf[x];
            while (x % p == 0) x /= p;

            // e = 2*v_p(i!) - v_p(k!)
            ll need = (vp_fact(i, p) << 1) - vp_fact(k, p);
            while (need > 0) {
                int t = ++k;
                while (t % p == 0) {
                    t /= p;
                    --need;
                }
            }
        }

        R[i] = k;
    }

    for (const int n : Ns) {
        cout << R[n] << endl;
    }

    return 0;
}
