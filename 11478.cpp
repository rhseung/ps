#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    string s;
    cin >> s;

    set<string> set;
    for (int i = 0; i < s.length(); ++i) {
        for (int j = i + 1; j <= s.length(); ++j) {
            set.insert(s.substr(i, j - i));
        }
    }

    cout << set.size();
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
