#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

void f(const vector<int>& numbers, vector<int>& used, const int depth, const int max_depth) {
    if (depth >= max_depth) {
        for (const int u: used)
            cout << u << " ";
        cout << endl;

        return;
    }

    // TODO:
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<int> numbers(n), used;
    for (int i = 0; i < n; ++i)
        cin >> numbers[i];

    math::

    ranges::sort(numbers);
    f(numbers, used, 0, m);

    return 0;
}
