#include <bits/stdc++.h>
#include <ranges>

#define endl '\n'
#define setup ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout << fixed; cout.precision(6);
using namespace std;
using lnt = long long int;
using uint = unsigned int;

lnt phi(lnt n) {
    lnt result = n;

    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            while (n % i == 0) {
                n /= i;
            }
            result -= result / i;
        }
    }

    if (n > 1) {
        result -= result / n;
    }

    return result;
}

int main() { setup;
    lnt n;
    cin >> n;

    if (n == 1) {
        cout << 1 << endl;
        return 0;
    }

    for (lnt x = 2; x <= n; ++x) {
        if (n % x == 0) {
            if (x * phi(x) == n) {
                cout << x << endl;
                return 0;
            }
        }
    }

	cout << -1 << endl;
	return 0;
}