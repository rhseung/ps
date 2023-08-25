from fractions import Fraction
a, b = map(int, input().split())
c, d = map(int, input().split())
e = Fraction(a, b) + Fraction(c, d)
print(e.numerator, e.denominator)