a1, a0 = map(int, input().split())
c = int(input())
n0 = int(input())

if c == a1:
    print(int(a0 <= 0))
elif c > a1:
    print(int(n0 >= a0/(c-a1)))
else:
    print(0)
    # print(int(n0 <= a0/(c-a1)))
