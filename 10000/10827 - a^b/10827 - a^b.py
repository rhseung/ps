# BOJ 10827 - a^b
import sys

input = sys.stdin.readline


def main():
    a_str, b_str = input().split()
    b = int(b_str)

    if '.' in a_str:
        dot_idx = a_str.index('.')
        frac_digits_len = len(a_str) - dot_idx - 1
        base_digits = a_str[:dot_idx] + a_str[dot_idx + 1:]
    else:
        frac_digits_len = 0
        base_digits = a_str

    base_digits = base_digits.lstrip('0') or '0'

    int_base = int(base_digits)
    pow_val = int_base ** b

    total_frac_digits = frac_digits_len * b

    s = str(pow_val)
    if total_frac_digits == 0:
        print(s)
        return

    if len(s) <= total_frac_digits:
        s = '0' * (total_frac_digits - len(s) + 1) + s

    point_idx = len(s) - total_frac_digits
    result = s[:point_idx] + '.' + s[point_idx:]

    result = result.lstrip('0')
    if result.startswith('.'):
        result = '0' + result
    result = result.rstrip('0')
    if result.endswith('.'):
        result = result[:-1]

    print(result)


if __name__ == "__main__":
    main()
