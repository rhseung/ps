import sys

problem_name = "DNA 비밀번호"
problem_url = "https://boj.kr/12891"
input = sys.stdin.readline

length, part_length = map(int, input().split())
dna_str = input().strip()
min_A, min_C, min_G, min_T = map(int, input().split())

count = 0
min_limit = {'A': min_A, 'C': min_C, 'G': min_G, 'T': min_T}
end = part_length

part = dna_str[end - part_length:end]
freq = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
for c in part:
	freq[c] += 1

while True:
	if all(freq[k] >= min_limit[k] for k in freq):
		# print(dna_str[end - part_length:end])
		count += 1
	
	if end == length:
		break
	
	freq[dna_str[end - part_length]] -= 1
	freq[dna_str[end]] += 1
	end += 1

print(count)
