#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int t;
    cin >> t;

    while (t--) {
        int k;
        cin >> k;

        multiset<int> Q;
        while (k--) {
            char oper;
            int value;
            cin >> oper >> value;

            if (oper == 'I') {
                Q.insert(value);
            }
            else if (oper == 'D') {
                if (!Q.empty()) {
                    if (value == 1)     // 최댓값 삭제
                        Q.erase(prev(Q.end()));
                    else if (value == -1)   // 최솟값 삭제
                        Q.erase(Q.begin());
                }
            }
        }

        if (Q.empty())
            cout << "EMPTY" << endl;
        else
            cout << *prev(Q.end()) << " " << *Q.begin() << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
