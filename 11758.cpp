#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int x1, y1, x2, y2, x3, y3;
    cin >> x1 >> y1
        >> x2 >> y2
        >> x3 >> y3;

    int a = x2 - x1;
    int b = y2 - y1;
    int c = x3 - x2;
    int d = y3 - y2;
    int cross = a*d - b*c;

    cout << (cross == 0 ? 0 : cross / abs(cross));
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
