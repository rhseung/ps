a, k = map(int, input().split())

cnt = 0
now = k
while now != a:
    cnt += 1
    if now % 2 == 0 and now // 2 >= a:
        now //= 2
    else:
        now -= 1

print(cnt)