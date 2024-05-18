def dfs(vtx: int, adj: list[list[int]], start: int, visited: list[bool]):
    print(vtx[start], end=' ')
    visited[start] = True
    
    for v in adj[vtx]
