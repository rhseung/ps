#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

lnt D[31];

void solution() {
    int n;
    cin >> n;

    D[0] = 1;
    D[1] = 0;
    D[2] = 3;

    for (int i = 3; i <= n; ++i) {
        // D[4]일 때 특이 케이스가 2개 추가됨, D[6]도 가로 이으면 2개 추가
        // D[i] = D[2] * D[i - 2] + 2 * D[i - 4] + 2 * D[i - 6] + ... + 2 ;
        lnt ret = D[2] * D[i - 2];

        for (int j = 4; i - j >= 0; j += 2) {
            ret += 2 * D[i - j];
        }

        D[i] = ret;
    }

    cout << D[n];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
