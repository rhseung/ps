__problem__ = 'https://boj.kr/2606', '바이러스'

import sys

input = sys.stdin.readline

n_coms = int(input())
n_edges = int(input())

cnt = 0
graph = [[] for _ in range(n_coms + 1)]
for _ in range(n_edges):
    v, w = map(int, input().split())

    graph[v].append(w)
    graph[w].append(v)

def dfs(graph: list[list[int]], now: int, visited: list[bool]):
    global cnt
    visited[now] = True
    cnt += 1

    for w in graph[now]:
        if not visited[w]:
            dfs(graph, w, visited)

dfs(graph, 1, [False]*(n_coms + 1))

print(cnt - 1)  # 1번 컴퓨터는 배제
