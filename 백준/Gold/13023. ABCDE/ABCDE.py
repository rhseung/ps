n, m = map(int, input().split())
graph = [[] for _ in range(n)]

for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

flag = False

def dfs(g, v, V, d):
    if d == 4:
        global flag
        flag = True
        return

    V[v] = True

    for w in g[v]:
        if not V[w]:
            dfs(g, w, V, d + 1)

    V[v] = False

for i in range(n):
    dfs(graph, i, [False] * n, 0)
    if flag:
        print(1)
        break
else:
    print(0)
