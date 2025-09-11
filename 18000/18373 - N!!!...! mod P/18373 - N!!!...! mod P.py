# BOJ 18373 - N!!!...! mod P
import sys
input = sys.stdin.readline

def fact_mod_prime(n: int, p: int) -> int:
    if n >= p:
        return 0
    
    L = p - 1 - n
    
    if n <= L:
        res = 1
        for i in range(2, n + 1):
            res = (res * i) % p
        
        return res
    else:
        facL = 1
        for i in range(2, L + 1):
            facL = (facL * i) % p
        inv_facL = pow(facL, p - 2, p)
        sign = p - 1 if (L % 2 == 0) else 1
        
        return (sign * inv_facL) % p


def main():
    n, k, p = map(int, input().split())

    if n >= p:
        print(0)
        return

    if n == 2:
        print(2 % p)
        return

    if n == 3:
        if k == 1:
            print(6 % p)
            return
        
        n = 6
        k -= 1

    if n >= 4:
        if k >= 3:
            print(0)
            return
        
        if k == 1:
            print(fact_mod_prime(n, p))
            return
        
        if k == 2:
            m = 1
            for i in range(2, n + 1):
                m *= i
                if m >= p:
                    print(0)
                    return
            
            print(fact_mod_prime(m, p))
            return

    print(fact_mod_prime(n, p))


if __name__ == "__main__":
    main()
