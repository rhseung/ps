n, m = map(int, input().split())
r, c, d = map(int, input().split())
room = [list(map(int, input().split())) for _ in range(n)]

cnt = 0

d_to_dp = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}

def dfs(now: tuple[int, int]):
    x, y = now
    
    global d
    if room[x][y] == 0:
        room[x][y] = -1
        global cnt
        cnt += 1
    
    all_clean = True
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if 0 <= x + dx < n and 0 <= y + dy < m:
            if room[x + dx][y + dy] == 0:
                all_clean = False

    if all_clean:
        dx, dy = d_to_dp[d]
        if 0 <= x - dx < n and 0 <= y - dy < m:
            if room[x - dx][y - dy] == 1:
                return
            else:
                dfs((x - dx, y - dy))
    else:
        found = False
        for i in range(4):
            d = (d - 1) % 4
            dx, dy = d_to_dp[d]
            if 0 <= x + dx < n and 0 <= y + dy < m:
                if room[x + dx][y + dy] == 0:
                    found = True
                    break
        
        if found:
            dx, dy = d_to_dp[d]
            dfs((x + dx, y + dy))

dfs((r, c))
print(cnt)
