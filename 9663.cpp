#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int n, cnt = 0;
int queen_j[15];    // queen_j[i] 각 줄의 퀸 컬럼 위치

void dfs(int i_0, int j_0) {
    if (i_0 == n - 1) {     // depth가 곧 i
        // 종료 조건, cnt 갱신
        cnt += 1;
        return;
    }

    // i_0, j_0 위치에 퀸을 둬서 갱신되는 행동 처리
    queen_j[i_0] = j_0;

    // 다음 위치 고르기
    for (int j = 0; j < n; ++j) {
        bool can = true;

        for (int i = 0; i <= i_0; ++i) {
            int q_j = queen_j[i];
            if (q_j == -1) continue;

            // 세로 처리
            if (j == q_j) {
                can = false;
                break;
            }

            // 대각선 처리
            int i_diff = (i_0 + 1) - i;
            if (abs(q_j - j) == i_diff) {
                can = false;
                break;
            }
        }

        // 착수
        if (can) {
            dfs(i_0 + 1, j);
        }
    }

    // 백트래킹
    queen_j[i_0] = -1;
}

void solution() {
    memset(queen_j, -1, sizeof(queen_j));

    cin >> n;
    // n*n 체스판에 n개의 퀸을 두려면 적어도 한 줄에 하나는 존재해야함
    // 근데 퀸은 가로로도 이동 가능하니까 겹치지 않으려면 각 줄에 퀸은 반드시 1개여야함
    for (int j = 0; j < n; ++j)
        dfs(0, j);
    cout << cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
