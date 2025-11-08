import sys

class Mat2x2:
    def __init__(self, value: tuple[tuple[int, int], tuple[int, int]], mod: int) -> None:
        if not isinstance(mod, int):
            raise TypeError("mod must be an int")
        self.mod = mod
        a, b = value[0]
        c, d = value[1]
        self.a = a % self.mod
        self.b = b % self.mod
        self.c = c % self.mod
        self.d = d % self.mod

    def __add__(self, o: 'Mat2x2') -> 'Mat2x2':
        if not isinstance(o, Mat2x2):
            return NotImplemented

        return Mat2x2((( (self.a + o.a) % self.mod, (self.b + o.b) % self.mod),
                       ( (self.c + o.c) % self.mod, (self.d + o.d) % self.mod)), mod=self.mod)

    def __sub__(self, o: 'Mat2x2') -> 'Mat2x2':
        if not isinstance(o, Mat2x2):
            return NotImplemented

        return Mat2x2((( (self.a - o.a) % self.mod, (self.b - o.b) % self.mod),
                       ( (self.c - o.c) % self.mod, (self.d - o.d) % self.mod)), mod=self.mod)

    def __matmul__(self, o: 'Mat2x2') -> 'Mat2x2':
        if not isinstance(o, Mat2x2):
            return NotImplemented

        a = (self.a * o.a + self.b * o.c) % self.mod
        b = (self.a * o.b + self.b * o.d) % self.mod
        c = (self.c * o.a + self.d * o.c) % self.mod
        d = (self.c * o.b + self.d * o.d) % self.mod
        return Mat2x2(((a, b), (c, d)), mod=self.mod)

    def __mul__(self, k: 'int | Mat2x2') -> 'Mat2x2':
        if isinstance(k, Mat2x2):
            return self.__matmul__(k)
        if not isinstance(k, int):
            return NotImplemented

        a = (self.a * k) % self.mod
        b = (self.b * k) % self.mod
        c = (self.c * k) % self.mod
        d = (self.d * k) % self.mod
        return Mat2x2(((a, b), (c, d)), mod=self.mod)

    def __rmul__(self, k: int) -> 'Mat2x2':
        return self.__mul__(k)

    def __repr__(self) -> str:
        return f"Mat2x2(({self.a},{self.b}),({self.c},{self.d})) mod={self.mod}"

    def __pow__(self: 'Mat2x2', exp: int) -> 'Mat2x2':
        if exp == 0:
            return Mat2x2(((1, 0), (0, 1)), mod=self.mod)

        result = Mat2x2(((1, 0), (0, 1)), mod=self.mod)
        cur = self
        e = exp
        while e > 0:
            if e & 1:
                result = result @ cur
            cur = cur @ cur
            e >>= 1
        return result

def input() -> str: return sys.stdin.readline()

x0, x1, a, b, k = map(int, input().split())
q = int(input())
p = 100003

# f(n) = n^k mod p with period p
F = [1 if k == 0 else 0] * p
if k != 0:
    for i in range(1, p):
        F[i] = pow(i, k % (p - 1), p)
def f(n: int) -> int:
    return F[n % p]

A = Mat2x2(((a % p, b % p), (1, 0)), mod=p)

Z2 = Mat2x2(((0, 0), (0, 0)), mod=p)
I2 = Mat2x2(((1, 0), (0, 1)), mod=p)

A_pows: list[Mat2x2] = [I2]
for _ in range(1, p + 1):
    A_pows.append(A_pows[-1] @ A)

# V_1...p where V_n = (x_n, x_(n-1)) vector
V: list[tuple[int, int]] = [(0, 0)] * (p + 1)
V[1] = (x1 % p, x0 % p)
prev2 = x0 % p
prev1 = x1 % p
for n in range(2, p + 1):
    xn = (a * prev1 + b * prev2 + f(n)) % p
    V[n] = (xn, prev1)
    prev2, prev1 = prev1, xn

def mv_mul(M: Mat2x2, v: tuple[int, int]) -> tuple[int, int]:
    x, y = v
    return (M.a * x + M.b * y) % p, (M.c * x + M.d * y) % p

def v_add(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return (u[0] + v[0]) % p, (u[1] + v[1]) % p

def v_sub(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return (u[0] - v[0]) % p, (u[1] - v[1]) % p

# (M^t, S_t) where S_t = I + M + ... + M^{t-1}
def pow_sum(M: Mat2x2, t: int) -> tuple[Mat2x2, Mat2x2]:
    P = I2
    S = Z2
    Mp = M
    Sp = I2
    x = t
    while x:
        if x & 1:
            S = S + (P @ Sp)
            P = P @ Mp
        # (Mp, Sp) -> (Mp^2, Sp + Mp*Sp)
        Mp2 = Mp @ Mp
        Sp2 = Sp + (Mp @ Sp)
        Mp, Sp = Mp2, Sp2
        x >>= 1
    return P, S

# C_r (r=0..p-1)
Ap = A_pows[p]
C: list[tuple[int, int]] = [(0, 0)] * p
acc0 = (0, 0)
for i in range(1, p + 1):
    Ai = A_pows[p - i]
    fi = f(i)
    acc0 = v_add(acc0, mv_mul(Ai, (fi, 0)))
C[0] = acc0

Ap_minus_I = Ap - I2
for r in range(0, p - 1):
    fi = f(r + 1)
    term = mv_mul(Ap_minus_I, (fi, 0))
    AC = mv_mul(A, C[r])
    C[r + 1] = v_sub(AC, term)

for _ in range(q):
    n = int(input())
    if n == 0:
        print(x0 % p)
        continue

    r = ((n - 1) % p) + 1  # 1..p
    t = (n - r) // p
    phase = r % p
    if t == 0:
        print(V[r][0] % p)
        continue

    Pt, St = pow_sum(Ap, t)
    pr = mv_mul(Pt, V[r])
    sc = mv_mul(St, C[phase])
    print((pr[0] + sc[0]) % p)
