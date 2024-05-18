#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

#define MOD 1'000'000'007
using lnt = long long int;

typedef struct matrix {
    lnt a, b, c, d;
} matrix2by2;

lnt add(lnt a, lnt b) {
    return ((a % MOD) + (b % MOD)) % MOD;
}

lnt mul(lnt a, lnt b) {
    return ((a % MOD) * (b % MOD)) % MOD;
}

matrix2by2 power(matrix2by2 A, lnt p) {
    if (p == 1) return A;

    matrix2by2 half = power(A, p / 2);
    lnt a = half.a, b = half.b, c = half.c, d = half.d;

    /**
     * [a b]^2 = [a^2+bc  ab+bd]
     * [c d]     [ca+dc  cb+d^2]
     */
    matrix2by2 half2 = {
        add(mul(a, a), mul(b, c)),
        add(mul(a, b), mul(b, d)),
        add(mul(c, a), mul(d, c)),
        add(mul(c, b), mul(d, d))
    };

    matrix2by2 ret = half2;
    if (p % 2 == 1) {
        ret = {
            add(mul(half2.a, A.a), mul(half2.b, A.c)),
            add(mul(half2.a, A.b), mul(half2.b, A.d)),
            add(mul(half2.c, A.a), mul(half2.d, A.c)),
            add(mul(half2.c, A.b), mul(half2.d, A.d))
        };
    }

    return ret;
}

void solution() {
    lnt n;
    cin >> n;

    if (n == 1) {
        cout << 1;
        return;
    }

    /**
     * [fn  ] = [fn-1 + fn-2] = [1 1][fn-1]
     * [fn-1]   [fn-1       ]   [1 0][fn-2]
     */
    matrix2by2 P = { 1, 1, 1, 0 };
    matrix2by2 Pn = power(P, n - 1);

    // lnt f1 = 1, f0 = 0;
    lnt fn = Pn.a % MOD;    // ((Pn.a * f1 % MOD) + (Pn.b * f0 % MOD)) % MOD;

    cout << fn;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
