//
// Created by Hyunseung Ryu on 2025. 8. 1..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll R, r;
    cin >> R >> r;

    // d^2 = R^2 - 2Rr
    ll d_sq = R * R - 2 * R * r;
    cout << d_sq << endl;

    return 0;
}
