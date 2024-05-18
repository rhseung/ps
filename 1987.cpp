#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int max_depth = 0;
bool visited[26];

void dfs(int x, int y, int r, int c, vector<vector<char>> &board, int depth) {
    visited[board[x][y] - 'A'] = true;
    max_depth = max(max_depth, depth);

    int ways[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (auto [dx, dy] : ways) {
        if (0 <= x + dx && x + dx < r && 0 <= y + dy && y + dy < c) {
            if (!visited[board[x + dx][y + dy] - 'A']) {
                dfs(x + dx, y + dy, r, c, board, depth + 1);
                visited[board[x + dx][y + dy] - 'A'] = false;
            }
        }
    }
}

void $(int r, int c, vector<vector<char>>& board) {
    dfs(0, 0, r, c, board, 1);
    cout << max_depth;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int r, c;
    cin >> r >> c;

    vector<vector<char>> board(r, vector<char>(c));
    for (int i = 0; i < r; ++i)
        for (int j = 0; j < c; ++j)
            cin >> board[i][j];

    $(r, c, board);
}
