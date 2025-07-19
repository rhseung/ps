__problem__ = 'https://boj.kr/1260', 'DFS와 BFS'

import sys
from collections import deque

input = sys.stdin.readline

n, m, v = map(int, input().split())
graph = [[] for _ in range(n+1)]

for _ in range(m):
    a, b = map(int, input().split())

    graph[a].append(b)
    graph[b].append(a)

# 작은 것부터 방문해야 하므로 sort 해야됨
for i in range(n+1):
    graph[i].sort()

def dfs(graph, now, visited):
    visited[now] = True
    print(now, end=' ')

    for w in graph[now]:
        if not visited[w]:
            dfs(graph, w, visited)

def bfs(graph, start):
    visited = [False]*(n+1)
    visited[start] = True
    queue = deque([start])

    while queue:
        top = queue.popleft()
        print(top, end=' ')

        for w in graph[top]:
            if not visited[w]:
                queue.append(w)
                visited[w] = True

dfs(graph, v, [False]*(n+1))
print()
bfs(graph, v)
