from copy import deepcopy

def dfs(now, graph, visited):
    visited[now] = True
    st = [now]
    cnt = 1

    while st:
        v = st.pop()

        for w in graph[v]:
            if not visited[w]:
                visited[w] = True
                st.append(w)
                cnt += 1
    
    return cnt, visited

def full_search(n, graph, visited):
    counts = []
    
    for i in range(1, n + 1):     
        if visited[i]:
            continue
        
        cnt, visited = dfs(i, graph, visited)
        counts.append(cnt)
    
    return counts

def solution(n, wires):
    ret = 1e9
    graph = [[] for _ in range(n + 1)]
    
    for u, v in wires:
        graph[u].append(v)
        graph[v].append(u)
        
    for u, v in wires:
        g = deepcopy(graph)
        g[u].remove(v)
        g[v].remove(u)
        
        counts = full_search(n, g, [False] * (n + 1))
        if len(counts) == 2:
            ret = min(ret, abs(counts[0] - counts[1]))
    
    return ret