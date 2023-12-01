__problem__ = 'https://boj.kr/2234', '성곽'

import sys
from collections import deque

input = sys.stdin.readline
pos = tuple[int, int]

col, row = map(int, input().split())
castle = [list(map(int, input().split())) for _ in range(row)]

visited = set()
room_count = 0
max_room = 0

def bfs(now: pos) -> int:
    queue = deque([now])
    visited.add(now)
    room_size = 1

    while queue:
        i, j = queue.popleft()
        v = castle[i][j]

        ways = []
        if not v & 1:   # west
            ways.append((i, j - 1))
        if not v & 2:   # north
            ways.append((i - 1, j))
        if not v & 4:   # east
            ways.append((i, j + 1))
        if not v & 8:   # south
            ways.append((i + 1, j))

        for r, c in ways:
            if row > r >= 0 and col > c >= 0:     # 벽 부수고 이동할 때 적절한 위치인지 확인 ex. (0, 0) -> 왼쪽 벽 부수고 (0, -1)
                if (r, c) not in visited:
                    queue.append((r, c))
                    visited.add((r, c))
                    room_size += 1

    return room_size

for i in range(row):
    for j in range(col):
        if (i, j) not in visited:
            room_count += 1
            max_room = max(max_room, bfs((i, j)))

print(room_count)
print(max_room)

# 가장 큰 사이즈의 방이 벽 하나를 두고 옆에 안 붙어있을 수도 있음
# room_sizes.sort()
# print(room_sizes[-1] + room_sizes[-2])

visited = set()
max_room = 0

for i in range(row):
    for j in range(col):
        if (i, j) not in visited:
            for wall in (1, 2, 4, 8):
                if castle[i][j] >= wall:
                    visited = set()
                    castle[i][j] -= wall
                    max_room = max(max_room, bfs((i, j)))
                    castle[i][j] += wall

print(max_room)
