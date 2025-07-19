__problem__ = 'https://boj.kr/1167', '트리의 지름'

import sys
from collections import deque

input = sys.stdin.readline

n = int(input())
graph = [[] for _ in range(n + 1)]

for _ in range(n):
    inp = list(map(int, input().split()))

    idx = inp[0]
    for i in range(1, len(inp) - 1, 2):
        graph[idx].append((inp[i], inp[i + 1]))

def bfs(g, s: int) -> list[int]:
    distance = [-1] * (n + 1)
    visited = [False] * (n + 1)

    visited[s] = True
    q = deque([(s, 0)])

    while q:
        v, dist_to_v = q.popleft()
        distance[v] = dist_to_v

        for w, d in g[v]:
            if not visited[w]:
                visited[w] = True
                q.append((w, dist_to_v + d))

    return distance

distance_from_1 = bfs(graph, 1)

idxmax = 0
for i in range(1, n + 1):
    if distance_from_1[idxmax] < distance_from_1[i]:
        idxmax = i

print(max(bfs(graph, idxmax)))
