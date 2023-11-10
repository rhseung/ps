__problem__ = 'https://boj.kr/2178', '미로 탐색'

import sys
from collections import deque

input = sys.stdin.readline

n, m = map(int, input().split())
maze = [list(map(int, list(input().strip()))) for _ in range(n)]

def bfs(g, s: tuple[int, int]):
    visited = [[False] * m for _ in range(n)]

    visited[s[0]][s[1]] = True
    q = deque([s])

    while q:
        a, b = q.popleft()

        for x, y in [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]:
            if 0 <= x < n and 0 <= y < m:
                if g[x][y] != 0:
                    if not visited[x][y]:
                        visited[x][y] = True
                        g[x][y] = g[a][b] + 1
                        q.append((x, y))

bfs(maze, (0, 0))
print(maze[n-1][m-1])
