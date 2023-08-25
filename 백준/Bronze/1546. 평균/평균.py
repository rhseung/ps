import sys
input = sys.stdin.readline

n = int(input())
scores = list(map(int, input().split()))
sum = sum(scores) / max(scores) * 100

print(sum / n)
