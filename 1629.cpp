#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using i64 = int64_t;

i64 fast_pow(int d, int p, int mod) {
    if (p == 0) return 1;
    else if (p == 1) return d % mod;

    i64 half = fast_pow(d, p / 2, mod);
    i64 rest = fast_pow(d, p % 2, mod);

    i64 half2 = ((i64)half * half) % mod;
    return (half2 * rest) % mod;
}

void solution() {
    int a, b, c;
    cin >> a >> b >> c;
//    cout << (a**b%c);
    cout << fast_pow(a, b, c);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
