from collections import deque

n, m = map(int, input().split())
A = [list(map(int, list(input().strip()))) for _ in range(n)]

def bfs(i, j):
    visited = [[False] * m for _ in range(n)]
    visited[i][j] = True

    queue = deque([(i, j)])
    while queue:
        a, b = queue.popleft()

        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if 0 <= a + di < n and 0 <= b + dj < m:
                if A[a + di][b + dj] > 0:
                    if not visited[a + di][b + dj]:
                        visited[a + di][b + dj] = True
                        queue.append((a + di, b + dj))
                        A[a + di][b + dj] = A[a][b] + 1

bfs(0, 0)
print(A[n - 1][m - 1])
