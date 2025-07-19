__problem__ = 'https://boj.kr/1753', '최단경로'

import sys
from math import inf
from heapq import heappop, heappush

input = sys.stdin.readline

n, e = map(int, input().split())
start = int(input().strip())

graph: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]

for _ in range(e):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))

def dijkstra(graph: list[list[tuple[int, int]]], start: int):
    dp = [inf] * (n + 1)
    dp[start] = 0
    visited = {start}

    now = start

    for _ in range(n):
        for v, w in graph[now]:
            dp[v] = min(dp[now] + w, dp[v])

        min_i = None
        for i in range(1, n + 1):
            if i not in visited:
                if (inf if not min_i else dp[min_i]) > dp[i]:
                    min_i = i

        now = min_i
        visited.add(now)

    return dp

def dijkstra_fast(graph: list[list[tuple[int, int]]], start: int):
    dp: list[int] = [inf] * (n + 1)
    dp[start] = 0
    pq = [(0, start)]

    while pq:
        w, u = heappop(pq)

        if w > dp[u]:
            continue

        for v, dist in graph[u]:
            if dp[v] > w + dist:
                dp[v] = w + dist
                heappush(pq, (dp[v], v))

    return dp

dp = dijkstra_fast(graph, start)

for i in range(1, n + 1):
    if dp[i] == inf:
        print('INF')
    else:
        print(dp[i])
