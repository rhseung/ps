from collections import deque

n, m = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(m)]     # 이거 왜 n*m이 아니고 m*n 이냐
V = [[False] * n for _ in range(m)]

def bfs(v: tuple[int, int]):
    queue = deque([v])
    V[v[0]][v[1]] = True
    size = 1

    while queue:
        i, j = queue.popleft()
        num = A[i][j]

        ways = []
        if not num & 1:
            ways.append((i, j - 1))
        if not num & 2:
            ways.append((i - 1, j))
        if not num & 4:
            ways.append((i, j + 1))
        if not num & 8:
            ways.append((i + 1, j))

        for a, b in ways:
            if 0 <= a < m and 0 <= b < n:
                if not V[a][b]:
                    V[a][b] = True
                    queue.append((a, b))
                    size += 1

    return size

cnt = 0
max_size = 0
for i in range(m):
    for j in range(n):
        if not V[i][j]:
            max_size = max(max_size, bfs((i, j)))
            cnt += 1

print(cnt)
print(max_size)

V = [[False] * n for _ in range(m)]     # note: 처음에 리셋 해주는 거 까먹지 말기
max_size = 0
for i in range(m):
    for j in range(n):
        if not V[i][j]:
            c = 1
            while A[i][j] >= c:
                A[i][j] -= c
                # 다시 같은 방을 순회하기 위해 visited를 초기화하는데,
                # 다른 방들은 이미 돌고 for 문은 지나왔기에 다른 것도 다 초기화해도 알 빠 아님
                V = [[False] * n for _ in range(m)]
                max_size = max(max_size, bfs((i, j)))
                A[i][j] += c
                c *= 2

print(max_size)
