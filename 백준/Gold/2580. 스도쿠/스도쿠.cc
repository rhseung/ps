#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

int board[9][9];
bool done = false;

// 3*3 체크
bool square_check(int i, int j, int n) {
	for (int x = (j / 3) * 3; x < (j / 3) * 3 + 3; x++) {
		for (int y = (i / 3) * 3; y < (i / 3) * 3 + 3; y++) {
			if (!(y == i && x == j) && board[y][x] == n) return false;
		}
	}

	return true;
}

// 가로줄, 세로줄 체크
bool line_check(int i, int j, int n) {
	for (int k = 0; k < 9; k++) {
		if (k != j && board[i][k] == n) return false;
		if (k != i && board[k][j] == n) return false;
	}

	return true;
}

void sudoku(int zero, int pos) {
	if (zero == 0) {
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				cout << board[i][j] << " ";
			}
			cout << endl;
		}

		done = true;
	}
	else {
		int i = pos / 9, j = pos % 9;

		if (board[i][j] != 0) {
			sudoku(zero, pos + 1);
		}
		else {
			for (int x = 1; x <= 9; x++) {
				if (line_check(i, j, x) && square_check(i, j, x)) {
					board[i][j] = x;
					sudoku(zero - 1, pos + 1);
					board[i][j] = 0;

					if (done) {
						break;
					}
				}
				else {
					continue;
				}
			}
		}		
	}
}

void solve() {
	int zero = 0;

	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			cin >> board[i][j];
			if (board[i][j] == 0) zero++;
		}
	}

	sudoku(zero, 0);
}

void setup() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);
	// cout << fixed;
	// cout.precision(6);
}

int main() {
	setup();
	solve();
	return 0;
}