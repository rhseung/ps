#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int a, b, c;
    cin >> a >> b >> c;

    // int l = pow(10, floor(log10(b) + 1));
    // int l = 1;
    // for (; l <= a; l *= 10);

    cout << a + b - c << endl;
    cout << stoi(to_string(a) + to_string(b)) - c << endl;
    // cout << a * l + b - c << endl;
}
