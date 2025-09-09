# 7677. [Fibonacci](https://www.acmicpc.net/problem/7677)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/14.svg" width="20px" /> | 1 초 | 128 MB | 1335 | 926 | 844 | 73.200% |

---

## 문제

In the Fibonacci integer sequence, $F_{0}$ = 0, $F_{1}$ = 1, and $F_{n}$ = $F_{n−1}$ + $F_{n−2}$
for n ≥ 2. For example, the first ten terms of the Fibonacci sequence are:

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, . . .

An alternative formula for the Fibonacci sequence is

\[\begin{bmatrix} $F_{ n+1 }$ & $F_{ n }$ \\ $F_{ n }$ & $F_{ n-1 }$ \end{bmatrix}=\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}^n\]

Given an integer n, your goal is to compute the last 4 digits of $F_{n}$
.

## 입력

The input test file will contain multiple test cases. Each test case consists of a single line containing n (where 0 ≤ n ≤ 1,000,000,000). The end-of-file is denoted by a single line containing the number -1.

## 출력

For each test case, print the last four digits of Fn. If the last four digits of Fn are all zeros, print ‘0’; otherwise, omit any leading zeros (i.e., print $F_{n}$
mod 10000).

## 예제

### 예제 입력 1

```
0
9
999999999
1000000000
-1
```

### 예제 출력 1

```
0
34
626
6875
```

## 출처

University
\> 
Stanford Local ACM Programming Contest
\> 
SLPC 2006
2번

## 알고리즘 분류

- 수학
- 정수론
- 분할 정복을 이용한 거듭제곱
- 피사노 주기

