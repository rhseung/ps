# 11238. [Fibo](https://www.acmicpc.net/problem/11238)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/16.svg" width="20px" /> | 1 초 | 256 MB | 740 | 451 | 413 | 62.861% |

---

## 문제

Fibonacci sequence is a well-known integer sequence that has many beautiful properties. Fibonacci sequence is something looks like this 0, 1, 1, 2, 3, 5, 8, 13, 21, … To make it formal, the mathematical term of Fibonacci sequence is define by recurrence relation.

\[F_n = $F_{n-1}$ + $F_{n-2}$ \text{where } n = 2, 3, \dots \text{and } F_0 = 0, F_1 = 1\]

If you know the technique to solve recurrence relation it will look like

\[F_n = \frac{1}{\sqrt{5}} \left\{ \left( \frac{1+\sqrt{5}}{2} \right)^n - \left( \frac{1-\sqrt{5}}{2} \right)^n  \right\}\]

And these are some of its beautiful properties (there are a lot more!)

\[\$sum_{i=1}$^{n}{F_i} = $F_{n+2}$-1 \\ F_n | $F_{kn}$ \text{where } k = 0, 1, 2, \dots\]

Enough for an introduction, let’s get to the main point. This problem is about finding greatest common divisor (GCD) between Fibonacci numbers. Given two Fibonacci number, your task is to find their GCD! Simple right?

## 입력

The first line contains a single integer T indicate the number of test cases (1 ≤ T ≤ 1 000)

Each of next T lines contains two integer N, M separated by a space (0 < N, M ≤ 1 000 000 000)

## 출력

For each test case, print a line contains value of gcd($F_{n}$
,$F_{m}$
) modulo by 1000000 007

## 예제

### 예제 입력 1

```
2
7 10
6 12
```

### 예제 출력 1

```
1
8
```

## 출처

ICPC
\> 
Regionals
\> 
Asia Pacific
\> 
Thailand
\> 
Thailand First Round Online
\> 
Thailand First Round Online 2014
C번

## 알고리즘 분류

- 수학
- 정수론
- 분할 정복을 이용한 거듭제곱
- 유클리드 호제법

