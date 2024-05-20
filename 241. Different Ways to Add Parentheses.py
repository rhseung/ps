def diff(input):
    def calc(left, right, op):
        result = []
        for l in left:
            for r in right:
                result.append(eval(str(l) + op + str(r)))
        return result
    
    if input.isdigit():
        return [int(input)]
    
    result = []
    for i, v in enumerate(input):
        if v in '-+*':
            left = diff(input[:i])
            right = diff(input[i+1:])
            result.extend(calc(left, right, v))
        
    return result

print(diff("2*3-4*5"))
