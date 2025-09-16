# 10562. [나이트](https://www.acmicpc.net/problem/10562)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/21.svg" width="20px" /> | 60 초 | 256 MB | 303 | 171 | 112 | 61.202% |

---

## 문제

![image](https://www.acmicpc.net/upload/images2/knights.png)

강호는 M행 N열 크기의 체스판 위에 나이트를 놓으려고 한다. 각각의 칸에는 최대 1개의 나이트가 놓여질 수 있다.

이때, 체스판 위에 있는 나이트가 서로 공격을 할 수 있으면 안 된다. 나이트가 놓여져 있을 때, 공격할 수 있는 칸의 위치는 아래 그림에 X로 표시되어 있다.

![image](https://onlinejudgeimages.s3-ap-northeast-1.amazonaws.com/problem/10562/1.png)

체스판의 크기가 주어졌을 때, 나이트를 놓을 수 있는 방법의 수를 구하는 프로그램을 작성하시오.

## 입력

첫째 줄에 테스트 케이스의 개수 T (T ≤ 10)가 주어진다. 각각의 테스트 케이스는 두 정수 M과 N으로 이루어져 있다. (1 ≤ M ≤ 4, 1 ≤ N ≤ $10^{9}$
)

## 출력

각각의 테스트 케이스마다, 나이트를 놓을 수 있는 방법의 수를 1,000,000,009로 나눈 나머지를 출력한다.

## 예제

### 예제 입력 1

```
4
1 2
2 2
3 2
4 31415926
```

### 예제 출력 1

```
4
16
36
413011760
```

## 출처

![image](https://licensebuttons.net/l/by-sa/3.0/88x31.png)

ICPC
\> 
Regionals
\> 
North America
\> 
Pacific Northwest Regional
\> 
2014 Pacific Northwest Region Programming Contest
\> 
Division 1
F번
ICPC
\> 
Regionals
\> 
North America
\> 
Southeast USA Regional
\> 
2014 Southeast USA Regional Programming Contest
\> 
Division 1
F번

- 문제를 번역한 사람: baekjoon

## 알고리즘 분류

- 수학
- 다이나믹 프로그래밍
- 비트마스킹
- 비트필드를 이용한 다이나믹 프로그래밍
- 분할 정복을 이용한 거듭제곱
- 벌리캠프–매시

