import sys

problem_name = "합 구하기"
problem_url = "https://boj.kr/11441"
input = sys.stdin.readline

length = int(input())
arr = list(map(int, input().split()))
interval_length = int(input())
intervals = []
for _ in range(interval_length):
	intervals.append(tuple(map(int, input().split())))

cum_arr = [arr[0]]
for i in range(1, length):
	cum_arr.append(arr[i] + cum_arr[i - 1])
	
for start, end in intervals:
	start -= 1
	end -= 1
	
	print(cum_arr[end] - (0 if start == 0 else cum_arr[start - 1]))
