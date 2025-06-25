# 과반수가 되는 값 찾기. floor(n / 2) 보다 많음.
from collections import defaultdict

def solve(nums: list[int]) -> int:
    d = defaultdict(int)
    for n in nums:
        d[n] += 1
    print(d)
    
    for n in nums:
        if d[n] > len(nums) // 2:
            return n

def teacher(nums: list[int]) -> int:
    if not nums:
        return None
    elif len(nums) == 1:
        return nums[0]
    
    half = len(nums) // 2
    a = teacher(nums[:half])
    b = teacher(nums[half:])
    
    return [b, a][nums.count(a) > half]

print(solve([3,2,3]))
print(solve([6, 5, 5]))
print(solve([2,2,1,1,1,2,2]))