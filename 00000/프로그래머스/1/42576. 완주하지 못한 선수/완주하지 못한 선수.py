from collections import defaultdict

def solution(participant, completion):
    people = defaultdict(int)
    for name in participant:
        people[name] += 1
    for name in completion:
        people[name] -= 1
        if people[name] == 0:
            del people[name]
    
    return next(iter(people))