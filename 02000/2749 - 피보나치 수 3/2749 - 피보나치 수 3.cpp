//
// Created by Hyunseung Ryu on 2025. 8. 8..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // 피사노 주기: f_n % M으로 나눈 나머지는 주기를 가지는데, M = 10^k일 때 주기의 길이는 15 * 10^(k-1)이다.
    // 따라서, M = 1,000,000일 때 주기의 길이는 1,500,000이다.

    constexpr int M = 1000000, P = 1500000;

    int fibo[P];
    fibo[0] = 0;
    fibo[1] = 1;

    for (int i = 2; i < P; i++) {
        fibo[i] = (fibo[i - 1] + fibo[i - 2]) % M;
    }

    ll n;
    cin >> n;
    cout << (fibo[n % P] % M);

    return 0;
}
