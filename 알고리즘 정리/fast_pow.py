def slow_power(x, p):
    result = 1
    for _ in range(p):
        result *= x
    return result

def fast_power(x, p):
    if p == 1:
        return x
    elif p % 2 == 0:
        return fast_power(x*x, p // 2)
    else:
        return x * fast_power(x*x, (p - 1) // 2)

def fast_power_4(x, p):
    if p == 1:
        return x
    elif p % 4 == 0:
        return fast_power(x*x*x*x, p // 4)
    elif p % 4 == 1:
        return x * fast_power(x*x*x*x, (p - 1) // 4)
    elif p % 4 == 2:
        return x*x * fast_power(x*x*x*x, (p - 2) // 4)
    else:
        return x*x*x * fast_power(x*x*x*x, (p - 3) // 4)

if __name__ == "__main__":
    from time import time
    
    print(f"Brute-force         = {slow_power(2, 500)}")
    print(f"Divide-and-conquer  = {fast_power(2, 500)}")
    print(f"Divide-and-conquer2 = {fast_power_4(2, 500)}")
    
    t1 = time()
    for i in range(100000): slow_power(2, 500)
    t2 = time()
    for i in range(100000): fast_power(2, 500)
    t3 = time()
    for i in range(100000): fast_power_4(2, 500)
    t4 = time()
    for i in range(100000): 2**500
    t5 = time()
    
    print(f"Brute-force         = {t2 - t1}")
    print(f"Divide-and-conquer  = {t3 - t2}")
    print(f"Divide-and-conquer2 = {t4 - t3}")
    print(f"Vanilla             = {t5 - t4}")
    