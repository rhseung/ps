n = int(input())
A = list(map(int, input().split()))
m = int(input())
X = list(map(int, input().split()))

A.sort()

for x in X:
    flag = False
    left, right = 0, n - 1

    while left <= right:
        mid = (left + right) // 2

        if x < A[mid]:
            right = mid - 1
        elif A[mid] < x:
            left = mid + 1
        else:
            flag = True
            break

    print(int(flag))
