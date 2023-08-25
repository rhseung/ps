#include <bits/stdc++.h>
#include <ranges>

using namespace std;
using uint = unsigned int;
using lnt = long long int;
void solve();
int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);
	//	size_t T; cin >> T; while (T--)
	{ solve(); }
	return 0;
}

#define mod 1'000'000'007
#define endl "\n"

int ceil(int x, int y) {
    return (x % y == 0) ? x / y : x / y + 1;
}

void solve() {
	int n, m;
    cin >> n >> m;

    deque<int> arr(n);
    for (int i = 0; i < n; ++i)
        cin >> arr[i];

    ranges::sort(arr, [](int a, int b) { return a > b; });

    int sum = 0, i = 1;
    for (; i < n; ++i) {
        int add = i * (arr[i - 1] - arr[i]);
        if (sum + add > m) break;
        sum += add;
    } i -= 1;

    int height = arr[i] - ceil(m - sum, i + 1);

    cout << height;
}