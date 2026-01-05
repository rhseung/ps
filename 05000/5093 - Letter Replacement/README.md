# 5093. [Letter Replacement](https://www.acmicpc.net/problem/5093)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/6.svg" width="20px" /> | 1 초 | 128 MB | 201 | 101 | 88 | 55.696% |

---

## 문제

Mr Sythe is teaching an ESL class about repeated letters in English words. As an exercise, he gets his students to replace all the repeated letters in a word with symbols.

The symbols used are as follows:

- * is used to replace the first repeated letter (the first letter encountered which has occurred before)
- ? for the second repeated letter
- / for the third repeated letter
- + for the fourth repeated letter
- ! for the fifth repeated letter.

No word that Mr Sythe uses has more than 5 repeated letters.

So, for example, the word Reindeer would become Reind**? because e is repeated twice and r is repeated once. The repeated e comes before the repeated r, hence the allocation of * to e and ? to r. Note that the first letter in the word is an upper case R, but this is treated as the same letter as the lower case r.

## 입력

In this problem, you will write a program to help Mr Sythe mark the exercise by giving him a list of correct answers. Input will consist of a list of words, one per line. Each word begins with an upper case letter and contains no more than 10 letters. The last line contains just a # - do not process this line.

## 출력

Output will be one word for each line of input each on a separate line. The output word must be the input word with repeated letters replaced as indicated by Mr Sythe's rules.

## 예제

### 예제 입력 1

```
Reindeer
Bubbles
Occurrence
#
```

### 예제 출력 1

```
Reind**?
Bu**les
Oc*ur?en*/
```

## 출처

ICPC
\> 
Regionals
\> 
South Pacific
\> 
South Pacific Region
\> 
New Zealand Programming Contest
\> 
NZPC 2011
H번

## 알고리즘 분류

- 구현
- 문자열

