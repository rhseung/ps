n = int(input())
m = int(input())
graph = [[] for _ in range(n + 1)]

for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

cnt = 0
def dfs(g, v, V):
    global cnt
    cnt += 1
    V[v] = True

    for w in g[v]:
        if not V[w]:
            dfs(g, w, V)

dfs(graph, 1, [False] * (n + 1))
print(cnt - 1)
