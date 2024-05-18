#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

bool not_prime[1'000'000] = {false, };

void solution() {
    int m, n;
    cin >> m >> n;

    not_prime[0] = true;
    not_prime[1] = true;

    for (int i = 2; i <= n; ++i) {
        if (not_prime[i])
            continue;

        int x = 2;
        while (i * x <= n) {
            not_prime[i * x] = true;
            x += 1;
        }
    }

    for (int i = m; i <= n; ++i) {
        if (!not_prime[i])
            cout << i << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
