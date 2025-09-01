# 13358. [Exponial](https://www.acmicpc.net/problem/13358)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/20.svg" width="50%" /> | 2 초 | 512 MB | 919 | 212 | 176 | 22.194% |

---

## 문제

Everybody loves big numbers (if you do not, you might want to stop reading at this point). There are many ways of constructing really big numbers known to humankind, for instance:

- Exponentiation: \(  $42^{2016}$= \underbrace {42 \cdot 42 \cdot ... \cdot 42}_\text{2016 times} \)
- Factorials: 2016! = 2016 · 2015 · . . . · 2 · 1.

In this problem we look at their lesser-known love-child the exponial, which is an operation defined for all positive integers n as

exponial(n) = \( $n^{{(n-1)}$^{{{(n-2)}^{{...}^{{2^1}}}}}} \)

For example, exponial(1) = 1 and exponial(5) = \( $5^{4^{3^{2^1}$}} \) ≈ 6.206 · $10^{183230}$
which is already pretty big. Note that exponentiation is right-associative: \( $a^{b^c}$=$a^{(b^c)}$ \).

Since the exponials are really big, they can be a bit unwieldy to work with. Therefore we would like you to write a program which computes exponial(n) mod m (the remainder of exponial(n) when dividing by m).

## 입력

The input consists of two integers n (1 ≤ n ≤ $10^{9}$
) and m (1 ≤ m ≤ $10^{9}$
)

## 출력

Output a single integer, the value of exponial(n) mod m.

## 예제

### 예제 입력 1

```
2 42
```

### 예제 출력 1

```
2
```

## 예제

### 예제 입력 2

```
5 123456789
```

### 예제 출력 2

```
16317634
```

## 예제

### 예제 입력 3

```
94 265
```

### 예제 출력 3

```
39
```

## 출처

![image](https://licensebuttons.net/l/by-sa/3.0/88x31.png)

ICPC
\> 
Regionals
\> 
Europe
\> 
Northwestern European Regional Contest
\> 
Nordic Collegiate Programming Contest
\> 
NCPC 2016
E번

- 문제를 만든 사람: Per Austrin

## 알고리즘 분류

- 수학
- 정수론
- 분할 정복을 이용한 거듭제곱
- 소인수분해
- 오일러 피 함수

