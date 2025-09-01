// BOJ 1806 - 부분합
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n, sum;
    cin >> n >> sum;

    auto C = new ll[n]{0};
    for (int i = 0; i < n; ++i) {
        if (i == 0)
            cin >> C[i];
        else {
            ll tmp;
            cin >> tmp;
            C[i] = C[i - 1] + tmp;
        }
    }

    // C는 누적합 배열이므로 오름차순 정렬된 상태
    size_t l = 0, r = 0;
    size_t min_len = SIZE_MAX;

    while (l <= r && l < n && r < n) {
        ll s = C[r] - (l == 0 ? 0 : C[l - 1]);
        if (s < sum) {
            r += 1;
        }
        else {
            // cout << l << " " << r << " " << s << endl;
            min_len = min(min_len, r - l + 1);
            l += 1;
        }
    }

    cout << (min_len == SIZE_MAX ? 0 : min_len) << endl;

    delete[] C;

    return 0;
}
