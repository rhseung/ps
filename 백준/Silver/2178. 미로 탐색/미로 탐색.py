__problem__ = 'https://boj.kr/2178', '미로 탐색'

import sys
from collections import deque

input = sys.stdin.readline

n, m = map(int, input().split())
maze = [list(map(int, list(input().strip()))) for _ in range(n)]

# graph = {
#     (1, 1): [(1, 2), ...],
#     (1, 2): [...],
# }
graph = {(r, c): set() for r in range(n) for c in range(m) if maze[r][c] == 1}

for i in range(n):
    for j in range(m):
        if maze[i][j] >= 1:
            ways = [(i-1, j), (i-1, j), (i, j-1), (i, j+1)]

            for a, b in ways:
                if (a >= 0 and b >= 0) and (a < n and b < m) and maze[a][b] >= 1:
                    graph[i, j].add((a, b))
                    graph[a, b].add((i, j))

for key in graph:
    graph[key] = list(graph[key])

depth = 1
def bfs(g: dict[tuple[int, int], list[tuple[int, int]]], start: tuple[int, int]):
    global depth

    visited = set()
    visited.add(start)
    queue = deque([start])

    while queue:
        top = queue.popleft()
        if top == (n - 1, m - 1):
            return

        for w in g[top]:
            if w not in visited:
                queue.append(w)
                visited.add(w)

            maze[w[0]][w[1]] = maze[top[0]][top[1]] + 1

bfs(graph, (0, 0))

# for e in maze:
#     print(*e, sep='\t')
print(maze[n-1][m-1])
