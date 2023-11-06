#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

int** board;
int r = 0;

void queen(int N, int q) {
	if (q == 0) {
		r++;
	}
	else {
		for (int i = 0; i < N; i++) {
			if (board[N - q][i] > 0) continue;

			board[N - q][i]++;
			for (int x = 0; x < N; x++) {
				for (int y = N - q + 1; y < N; y++) {
					if ((y - x) == (N - q - i) || (y + x) == (N - q + i) || x == i || y == (N - q)) board[y][x]++;
				}
			}

			queen(N, q - 1);

			board[N - q][i]--;
			for (int x = 0; x < N; x++) {
				for (int y = N - q + 1; y < N; y++) {
					if ((y - x) == (N - q - i) || (y + x) == (N - q + i) || x == i || y == (N - q)) {
						if (board[y][x] > 0) board[y][x]--;
					}
				}
			}
		}
	}
}

void solve() {
	int N;
	cin >> N;

	board = new int*[N];
	for (int i = 0; i < N; i++) {
		board[i] = new int[N];
		fill_n(board[i], N, 0);
	}

	queen(N, N);

	cout << r;
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