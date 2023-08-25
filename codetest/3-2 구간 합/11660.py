import sys
input = sys.stdin.readline

size, testcase = map(int, input().split())
cum_arr = []

for _ in range(size):
	tmp = list(map(int, input().split()))
	
	cum_tmp = [tmp[0]]
	for i in range(1, len(tmp)):
		cum_tmp.append(tmp[i] + cum_tmp[i - 1])
		
	cum_arr.append(cum_tmp)

for _ in range(testcase):
	x1, y1, x2, y2 = map(lambda x: int(x) - 1, input().split())
	
	sum = 0
	for row in range(x1, x2 + 1):
		sum += (cum_arr[row][y2] - (0 if y1 == 0 else cum_arr[row][y1 - 1]))
	
	print(sum)