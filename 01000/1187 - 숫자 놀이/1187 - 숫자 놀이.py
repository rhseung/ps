import sys

input = sys.stdin.readline

n = int(input().strip())
A = list(map(int, input().split()))

sm_levels = {}
lev_levels = {}

sm_levels[n] = A[:]


# sys.setrecursionlimit(10000)

def build(a: int, u: int) -> None:
    if a == 1:
        return
    cur = sm_levels[a]
    m = 2 * a - 1
    used = [False] * m
    next_vals = []
    next_parents = []

    prv = -1
    for i in range(m):
        if cur[i] % u != 0 and not used[i]:
            if prv == -1:
                prv = i
            else:
                used[prv] = used[i] = True
                next_vals.append(cur[prv] + cur[i])
                next_parents.append((prv, i))
                prv = -1

    prv = -1
    for i in range(m):
        if not used[i] and cur[i] % u == 0:
            if prv == -1:
                prv = i
            else:
                used[prv] = used[i] = True
                next_vals.append(cur[prv] + cur[i])
                next_parents.append((prv, i))
                prv = -1

    assert len(next_vals) == a - 1

    sm_levels[a // 2] = next_vals
    lev_levels[a // 2] = next_parents

    build(a // 2, u * 2)


build(n, 2)

res = []


def unwind(a: int, idx: int):
    if a == n:
        res.append(sm_levels[a][idx])
        return

    p, q = lev_levels[a][idx]
    unwind(a * 2, p)
    unwind(a * 2, q)


unwind(1, 0)

print(*res)
