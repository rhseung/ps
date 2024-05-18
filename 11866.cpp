#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    
    int n, k;
    cin >> n >> k;

    queue<int> q;
    for (int i = 1; i <= n; i++)
        q.push(i);

    cout << "<";

    int c = 0;
    while (!q.empty()) {
        c = (c + 1) % k;

        if (c != 0) {
            q.push(q.front());
            q.pop();
        }
        else {
            cout << q.front();
            q.pop();

            if (!q.empty())
                cout << ", ";
        }
    }

    cout << ">";
    
    return 0;
}
