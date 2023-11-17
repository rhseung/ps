__problem__ = 'https://boj.kr/1920', '수 찾기'

import sys

input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))
m = int(input())
K = list(map(int, input().split()))

A.sort()

for key in K:
    flag = False

    i, j = 0, n - 1
    while i <= j:
        mid = (i + j) // 2

        if A[mid] > key:
            j = mid - 1
        elif A[mid] < key:
            i = mid + 1
        else:
            flag = True
            break

    print(int(flag))
