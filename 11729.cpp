#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void hanoi(int n, int from, int tmp, int to) {
    /*
     * 1~n x     x
     * n   1~n-1 x
     * x   1~n-1 n
     * x   x     1~n
     */

    if (n == 1) {
        cout << from << ' ' << to << endl;
    }
    else {
        hanoi(n - 1, from, to, tmp);    // n - 1개 from -> tmp 로 이동
        cout << from << ' ' << to << endl;      // 가장 큰 원판 from -> to 로 이동
        hanoi(n - 1, tmp, from, to);    // n - 1개 tmp -> to 로 이동
    }
}

// pow 함수는 double 반환해서 수가 커지면 지수표현식(ex. 3.02e08) 써서 오류 났었음.
int power(int b, int p) {
    if (p == 0) return 1;
    else return power(b, p / 2) * power(b, p / 2) * (p % 2 == 0 ? 1 : b);
}

void solution() {
    int n;
    cin >> n;
    auto cnt = pow(2, n) - 1;
    cout << (power(2, n) - 1) << endl;
    hanoi(n, 1, 2, 3);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
