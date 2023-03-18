#include <bits/stdc++.h>
#include <ranges>

#define endl '\n'
#define setup ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout << fixed; cout.precision(6);
using namespace std;
using lnt = long long int;
using uint = unsigned int;

int dp[50] = {0, 1, };
int fibo(int n) {
	if (n == 0) return 0;
	else if (n == 1) return 1;
	else if (dp[n] != 0) return dp[n];
	dp[n] = fibo(n - 1) + fibo(n - 2);
	return dp[n];
}

int main() { setup;
	int T;
	cin >> T;
	
	while (T--) {
		int n;
		cin >> n;
		int first = n == 0 ? 1 : fibo(n - 1);
		int second = fibo(n);
		cout << first << " " << second << endl;
	}
	
	return 0;
}