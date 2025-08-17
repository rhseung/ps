// BOJ 2239 - 스도쿠
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

bool is_valid(const int sudoku[9][9], const int i, const int j, const int value) {
    for (int p = 0; p < 9; ++p) {
        if (sudoku[p][j] == value || sudoku[i][p] == value || sudoku[i / 3 * 3 + p / 3][j / 3 * 3 + p % 3] == value)
            return false;
    }

    return true;
}

void backtrack(int sudoku[9][9], const int i, const int j) {
    // cout << i << ", " << j << endl;

    if (i == 9 && j == 0) {
        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                cout << sudoku[r][c];
            }
            cout << endl;
        }
        exit(0);
    }
    else if (sudoku[i][j] == 0) {
        for (int test = 1; test <= 9; ++test) {
            if (is_valid(sudoku, i, j, test)) {
                sudoku[i][j] = test;
                if (j == 8)
                    backtrack(sudoku, i + 1, 0);
                else
                    backtrack(sudoku, i, j + 1);
                sudoku[i][j] = 0;
            }
        }
    }
    else {
        if (j == 8)
            backtrack(sudoku, i + 1, 0);
        else
            backtrack(sudoku, i, j + 1);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int sudoku[9][9];
    for (int i = 0; i < 9; ++i) {
        string tmp;
        cin >> tmp;
        for (int j = 0; j < 9; ++j) {
            sudoku[i][j] = tmp[j] - '0';
        }
    }

    backtrack(sudoku, 0, 0);

    return 0;
}
