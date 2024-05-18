W = [list(map(int, list(input().strip()))) for _ in range(4)]
W.insert(0, [None]*8)
W.append([None]*8)

R = [0] * 6

def rotate(w: list[int], direction: int) -> list[int]:
    if direction == 1:
        end = w.pop()
        w.insert(0, end)
        return w
    elif direction == -1:
        begin = w.pop(0)
        w.append(begin)
        return w

def right(n: int, direction: int):
    if 1 <= n <= 4:
        # rotate(W[n], direction)
        R[n] = direction
        if W[n][2] != W[n + 1][-2]:
            right(n + 1, -direction)

def left(n: int, direction: int):
    if 1 <= n <= 4:
        # rotate(W[n], direction)
        R[n] = direction
        if W[n][-2] != W[n - 1][2]:
            left(n - 1, -direction)

k = int(input().strip())
for i in range(k):
    n, direction = map(int, input().split())
    
    right_eq = W[n][2] == W[n + 1][-2]
    left_eq = W[n][-2] == W[n - 1][2]
    
    # rotate(W[n], direction)
    R[n] = direction
    if not right_eq:
        right(n + 1, -direction)
    if not left_eq:
        left(n - 1, -direction)
        
    for j in range(1, 5):
        rotate(W[j], R[j])
    R = [0] * 6

score = sum(2**(i - 1) * (W[i][0] == 1) for i in range(1, 5))
print(score)
