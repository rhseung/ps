#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

void solution() {
    int k, n;
    cin >> k >> n;

    lnt *A = new lnt[k];
    lnt max_val = LONG_LONG_MIN;
    for (int i = 0; i < k; ++i) {
        cin >> A[i];
        max_val = max(max_val, A[i]);
    }

    // 길이가 길수록 랜선 수는 감소, 서로 역방향
    // 길이의 최대 -> 랜선 수의 최소
    auto f = [k, A](lnt x) {
        lnt ret = 0;
        for (int i = 0; i < k; ++i)
            ret += A[i] / x;
        return ret;
    };

    // 길이의 범위: 1 ~ max(A)   맨 처음에 min(A) 인 줄 알았는데 반례 찾아보니까 아예 랜선을 안 써도 된다고..
    lnt l = 1, r = max_val;
    lnt result;

    while (l <= r) {
        lnt mid = (l + r) / 2;
        lnt wire = f(mid);

        if (wire >= n) {
            result = mid;
            l = mid + 1;
        }
        else {
            r = mid - 1;
        }
    }

    cout << result;

    delete(A);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
