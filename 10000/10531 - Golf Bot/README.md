# 10531. [Golf Bot](https://www.acmicpc.net/problem/10531)

| 티어                                                                  | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
| --------------------------------------------------------------------- | --------- | ----------- | ---: | ---: | --------: | --------: |
| <img src="https://static.solved.ac/tier_small/20.svg" width="20px" /> | 1 초      | 256 MB      | 3839 | 1817 |      1019 |   47.684% |

---

## 문제

![image](https://www.acmicpc.net/upload/images2/golf.png)

Do you like golf? I hate it. I hate golf so much that I decided to build the ultimate golf robot, a robot that will never miss a shot. I simply place it over the ball, choose the right direction and distance and, flawlessly, it will strike the ball across the air and into the hole. Golf will never be played again.

Unfortunately, it doesn’t work as planned. So, here I am, standing in the green and preparing my first strike when I realize that the distance-selector knob built-in doesn’t have all the distance options! Not everything is lost, as I have 2 shots.

Given my current robot, how many holes will I be able to complete in 2 strokes or less?

## 입력

The first line has one integer: N, the number of different distances the Golf Bot can shoot. Each of the following N lines has one integer, $k_{i}$
, the distance marked in position i of the knob.

Next line has one integer: M, the number of holes in this course. Each of the following M lines has one integer, $d_{j}$
, the distance from Golf Bot to hole j.

## 출력

You should output a single integer, the number of holes Golf Bot will be able to complete. Golf Bot cannot shoot over a hole on purpose and then shoot backwards.

## 제한

- 1 ≤ N, M ≤ 200 000
- 1 ≤ $k_{i}$ , $d_{j}$ ≤ 200 000

## 예제

### 예제 입력 1

```
3
1
3
5
6
2
4
5
7
8
9
```

### 예제 출력 1

```
4
```

## 힌트

Golf Bot can shoot 3 different distances (1, 3 and 5) and there are 6 holes in this course at distances 2, 4, 5, 7, 8 and 9. Golf Bot will be able to put the ball in 4 of these:

- The 1st hole, at distance 2, can be reached by striking two times a distance of 1.
- The 2nd hole, at distance 4, can be reached by striking with strength 3 and then strength 1 (or vice-versa).
- The 3rd hole can be reached with just one stroke of strength 5.
- The 5th hole can be reached with two strikes of strengths 3 and 5.

Holes 4 and 6 can never be reached.

## 출처

![image](https://licensebuttons.net/l/by-sa/3.0/88x31.png)

ICPC
\>
Regionals
\>
Europe
\>
Southwestern European Regional Contest
\>
SWERC 2014
C번

## 알고리즘 분류

- 수학
- 고속 푸리에 변환
