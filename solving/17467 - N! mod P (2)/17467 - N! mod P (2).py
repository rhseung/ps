# BOJ 17467 - N! mod P (2)
import sys
input = sys.stdin.buffer.readline

def prod_mod_upto(k: int, mod: int) -> int:
    if k < 2:
        return 1
    
    a = 1
    m = mod
    i = 2
    
    while i + 1 <= k:
        a = (a * ((i * (i + 1)) % m)) % m
        i += 2
    
    if i == k:
        a = (a * i) % m
    return a


def main() -> None:
    n, p = map(int, input().split())

    r = p - 1 - n

    if n == 0:
        print(1)
        return
    if r == 0:
        print(p - 1)
        return
    if r == 1:
        print(1)
        return

    if n <= r:
        ans = prod_mod_upto(n, p)
        print(ans)
    else:
        a = prod_mod_upto(r, p)
        inv = pow(a, -1, p)
        
        if (r & 1) == 0:
            print((p - inv) % p)
        else:
            print(inv)


if __name__ == "__main__":
    main()
