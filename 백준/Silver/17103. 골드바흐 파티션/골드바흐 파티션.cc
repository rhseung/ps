#include <bits/stdc++.h>
#include <ranges>
#define ceil(x, y) ((x % y == 0) ? x / y : x / y + 1)
#define endl "\n"
#define mod 1'000'000'007
#define SIZE 1'000'001
using namespace std;
using uint = unsigned int;
using lnt = long long int;
void solve();
void sieve();
int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

    sieve();

    size_t T; cin >> T; while (T--)
	{ solve(); }
	return 0;
}

bool primes[SIZE];
void sieve() {
    for (bool &prime : primes) {
        prime = true;
    }

    for (int i = 2; i < SIZE; ++i) {
        if (!primes[i]) continue;

        for (int j = 2*i; j < SIZE; j += i) {
            primes[j] = false;
        }
    }
}

int goldbach(int x) {
    int count = 0;
    for (int i = 2; i <= ceil(x, 2); ++i) {
        if (primes[i] and primes[x - i])
            count++;
    }

    return count;
}

void solve() {
	int x;
    cin >> x;
    cout << goldbach(x) << endl;
}