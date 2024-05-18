#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

bool is_star(int r, int c) {
    if (r == 0 && c == 0)
        return true;
    else if (r % 3 == 1 && c % 3 == 1)
        return false;
    else
        return is_star(r / 3, c / 3);
}

void solution() {
    int n;
    cin >> n;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (is_star(i, j)) cout << "*";
            else cout << " ";
        }
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
