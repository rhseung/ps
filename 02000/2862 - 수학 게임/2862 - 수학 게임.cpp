// BOJ 2862 - 수학 게임
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

// 1, 2, 3, 5, 8, ... (1과 2에서 시작)
vector<ull> fibo;

ull solve_rec(const ull n) {
    if (n == 1) return 1;
    if (n == 2) return 2;

    const size_t k = ranges::upper_bound(fibo, n) - fibo.begin() - 1;

    if (n == fibo[k])
        return fibo[k];
    return solve_rec(n % fibo[k]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    fibo.reserve(100);
    fibo.push_back(1);
    fibo.push_back(2);
    while (fibo.back() <= static_cast<ull>(1e16)) {
        const ull next = fibo[fibo.size() - 1] + fibo[fibo.size() - 2];
        fibo.push_back(next);
    }

    ull n;
    cin >> n;

    const size_t k = ranges::upper_bound(fibo, n) - fibo.begin() - 1;
    if (n == fibo[k] || n == fibo[k + 1]) {
        cout << n << endl;
        return 0;
    }

    cout << solve_rec(n % fibo[k]) << endl;
    return 0;
}