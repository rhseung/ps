#include <bits/stdc++.h>
#include <cmath>
#define endl '\n'
using namespace std;

void f(int n) {
    if (n == 0) {
        cout << "-";
        return;
    }

    f(n - 1);
    cout << string(pow(3, n - 1), ' ');
    f(n - 1);
}

void solution() {
    int n;
    while (cin >> n) {
        f(n);
        cout << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
