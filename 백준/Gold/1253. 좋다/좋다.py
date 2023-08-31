import sys

problem_name = "좋다"
problem_url = "https://boj.kr/1253"
input = sys.stdin.readline

length = int(input())
numbers = list(map(int, input().split()))

numbers.sort()

count = 0
for i in range(len(numbers)):
	except_numbers = numbers[:i] + numbers[i+1:]
	number = numbers[i]
	left, right = 0, len(except_numbers) - 1
	
	while left < right:
		key = except_numbers[left] + except_numbers[right]
		
		if key > number:
			right -= 1
		elif key < number:
			left += 1
		else:
			count += 1
			break
		
print(count)
