#include <bits/stdc++.h>
#include <ranges>

#define endl '\n'
#define setup ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout << fixed; cout.precision(6);
using namespace std;
using lnt = long long int;
using uint = unsigned int;

int main() { setup;
	int row, col, block;
	cin >> row >> col >> block;
	
	int max_height = 0, min_height = 256;
	deque<deque<int>> heights(row, deque<int>(col));
	for (int i = 0; i < row; ++i) {
		for (int j = 0; j < col; ++j) {
			cin >> heights[i][j];
			max_height = max(max_height, heights[i][j]);
			min_height = min(min_height, heights[i][j]);
		}
	}
	
	int min_sec = 64'000'000, height = max_height;
	for (int h = max_height; h >= min_height; --h) {
		int over = 0, under = 0;
		
		for (int i = 0; i < row; ++i) {
			for (int j = 0; j < col; ++j) {
				if (heights[i][j] > h) over += heights[i][j] - h;
				else if (heights[i][j] < h) under += h - heights[i][j];
			}
		}
		
		if (under > over + block) continue;
		
		if (min_sec > over * 2 + under * 1) {
			min_sec = over * 2 + under * 1;
			height = h;
		}
	}
	
	cout << min_sec << " " << height;
	
	return 0;
}