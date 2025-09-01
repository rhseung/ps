// BOJ 2473 - 세 용액
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n;
    cin >> n;

    const auto A = new ll[n];
    for (ll i = 0; i < n; ++i)
        cin >> A[i];

    sort(A, A + n);

    ll min_diff = 3e9;
    tuple<ll, ll, ll> min_solve;

    for (ll a = 0; a < n - 2; ++a) {
        if (min_diff == 0)
            break;

        ll b = a + 1, c = n - 1;
        while (b < c) {
            const ll s = A[a] + A[b] + A[c];
            if (abs(s) < abs(min_diff)) {
                min_diff = s;
                min_solve = {A[a], A[b], A[c]};
            }

            if (s > 0) {
                c -= 1;
            }
            else if (s < 0) {
                b += 1;
            }
            else {
                break;
            }
        }
    }

    cout << get<0>(min_solve) << " " << get<1>(min_solve) << " " << get<2>(min_solve) << endl;

    delete[] A;

    return 0;
}
