#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int DP[1001][1001];

void solution() {
    string s1, s2;
    cin >> s1 >> s2;

    for (int i = 1; i <= s1.length(); ++i) {
        for (int j = 1; j <= s2.length(); ++j) {
            DP[i][j] = max(max(DP[i - 1][j], DP[i][j - 1]), DP[i - 1][j - 1] + (s1[i - 1] == s2[j - 1]));
        }
    }

    cout << DP[s1.length()][s2.length()];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
