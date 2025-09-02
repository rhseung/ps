from collections import deque, defaultdict

def tour(start_x, start_y, end_x, end_y):
    board: defaultdict[tuple[int, int], int] = defaultdict(int)

    q = deque([(start_x, start_y)])
    board[start_x, start_y] = 0

    while q:
        x, y = q.popleft()
        if (x, y) == (end_x, end_y):
            return board
        
        ways = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (-2,1), (2,-1), (-2,-1)]
        ways.sort(key=lambda d: (end_x - (x + d[0])) + (end_y - (y + d[1])))

        for dx, dy in ways:
            if board[x + dx, y + dy] == 0:
                q.append((x + dx, y + dy))
                board[x + dx, y + dy] = board[x, y] + 1
                
while (inp := input()) != 'END':
    x, y = map(int, inp.split())
    board = tour(0, 0, x, y)
    print(board[x, y])
