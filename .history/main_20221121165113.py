import json
#import system


def check_for_win(b):
    # checks for horizontal win
    for i in range(6):
        for a in range(4):
            if b[i][a] != 0 and b[i][a] == b[i][a + 1] == b[i][a + 2] == b[i][a + 3]:
                return b[i][a]
    # checks for vertical win
    for a in range(7):
        for i in range(3):
            if b[i][a] != 0 and b[i][a] == b[i + 1][a] == b[i + 2][a] == b[i + 3][a]:
                return b[i][a]
    # checks for diagonal wins
    for a in range(3):
        for i in range(4):
            if b[a][i] != 0 and b[a][i] == b[a + 1][i + 1] == b[a + 2][i + 2] == b[a + 3][i + 3]:
                return b[a][i]
    for a in range(5, 2, -1):
        for i in range(3):
            if b[a][i] != 0 and b[a][i] == b[a - 1][i + 1] == b[a - 2][i + 2] == b[a - 3][i + 3]:
                return b[a][i]
    for i in range(6):
        if 0 in b[i]:
            return 0
    return 3



def valid_moves(b):
    
    moves = [None, None, None, None, None, None, None]
    new_moves = []
    for i in range(5, -1, -1):
        for a in range(6):
            if moves[a] is None and b[i][a] == 0:
                moves[a] = (i, a)
    return moves


def update_board_pos(b, move, player):
    b[move[0]][move[1]] = player
    return b


def user_choice(b, player):
    moves = valid_moves(b)
    p_board(b)
    c = 1
    for i in range(len(moves)):
        if moves[i] != None:
            print('Move {} column {}'.format(c, moves[i][1]))
            c += 1
    choice = int(input('Enter your choice: ').strip()) - 1
    while moves[choice] == None:
        choice = int(input('Try again enter your choice: ').strip()) - 1
    b = update_board_pos(b, moves[choice], player)
    return b


def p_board(b):
    for row in b:
        for col in row:
            print('{} '.format(col), end='')
        print('\n', end='')


def add_to_db(b1, b2, board_db):
    print(board_db)
    board_db[b1] = b2
    return board_db


def board_to_binary(b):
    b_binary = ''
    m_binary = ''
    for i in range(6):
        for a in range(7):
            if b[i][a] > 0:
                b_binary += '1'
            else:
                b_binary += '0'
            if b[i][a] == 1:
                m_binary += '1'
            else:
                m_binary += '0'
    return (b_binary, m_binary)


def binary_to_board(b):
    board = []
    for i in range(0, 36, 7):
        row = []
        for a in range(7):
            row.append(int(b[0][i + a]))
        board.append(row)
    return board


if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

    p_board(binary_to_board(board_to_binary(board)))

    print('\n')
    board_db = dict()

    count = 1
    while check_for_win(board) == 0:
        if count % 2 == 0:
            p = 2
        else:
            p = 1
        board = user_choice(board, p)
        if count > 1:
            add_to_db(board_to_binary(board), board_to_binary(old_board), board_db)
        old = board 
        count += 1
        
    print(board_db)
    p_board(board)
    print('Player {} wins congrats'.format(p))

    with open('data.json', 'w') as outfile:
        json.dumps(board_db, indent = 4) 
