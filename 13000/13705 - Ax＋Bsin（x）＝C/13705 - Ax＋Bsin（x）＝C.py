from decimal import *

getcontext().prec = 30
getcontext().rounding = ROUND_HALF_UP
pi = Decimal('3.141592653589793238462643383279502884197169399375105820')
A, B, C = list(map(Decimal, input().split(' ')))
f = lambda x: A * x + B * sin(x) - C
df = lambda x: A + B * cos(x)


def cos(x):
    if -2*pi <= x <= 2*pi:
        getcontext().prec += 2
        last_value, value = Decimal('0'), Decimal('1')
        i, num = Decimal('1'), Decimal('1')
        while value != last_value:
            last_value = value
            num *= -x * x / (i * (i + Decimal('1')))
            value += num
            i += 2
        getcontext().prec -= 2
        return value
    else:
        return cos(x % (2*pi))


def sin(x):
    if -2*pi <= x <= 2*pi:
        getcontext().prec += 2
        last_value, value = 0, x
        i, num = 2, x
        while value != last_value:
            last_value = value
            num *= -x * x / (i * (i + Decimal('1')))
            value += num
            i += 2
        getcontext().prec -= 2
        return value
    else:
        return sin(x % (2*pi))


def newton(A, B, C):
    low = (C - B) / A - B
    high = (C + B) / A + B
    x_last = (low + high) / 2
    x = x_last - f(x_last) / df(x_last)
    while abs(x - x_last) > Decimal('1E-25'):
        x_last = x
        x = x_last - f(x_last) / df(x_last)
        #print(f'x: {x}, x_last: {x_last}, x - x_last: {x - x_last}\nf(x_last): {f(x_last)}, df(x_last): {df(x_last)}')

    return x


sol = newton(A, B, C)
print(round(sol, 6))
