__problem__ = 'https://boj.kr/13023', 'ABCDE'

import sys

input = sys.stdin.readline

n, m = map(int, input().split())
graph = [[] for _ in range(n)]

for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

def dfs(graph, now, visited: list[bool], depth: int):
    if depth == 5:
        print(1)
        exit()

    visited[now] = True

    for w in graph[now]:
        if not visited[w]:
            dfs(graph, w, visited, depth+1)

    visited[now] = False
    # depth가 5인 경로를 찾지 못하고 종료되는 경우가 가능
    # 1->2,3 | 2->1,4,5 | 3->1,5 | 4->2 | 5->2,3 인 그래프에서
    # 1을 기준으로 시작하면 1->2->4->5->3 순회는 dfs 순회이긴 하나 depth가 5가 안되고 종료됨
    # 1을 기준으로 시작할 때 1->3 으로 출발하는 것이 dfs 순회이면서 depth가 5가 됨
    # 따라서 이 문제를 해결하려면 visited를 다시 초기화하는 방법이 있음
for now in range(n):
    dfs(graph, now, [False]*n, 1)
print(0)
