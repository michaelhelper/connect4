#!/usr/bin/env python
import json
import asyncio
import websockets
import copy
import random
import time


# import system


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
    for a in range(5, -1, -1):
        for i in range(3):
            if b[a][i] != 0 and b[a][i] == b[a - 1][i + 1] == b[a - 2][i + 2] == b[a - 3][i + 3]:
                return b[a][i]
    for i in range(6):
        if 0 in b[i]:
            return 0
    return 3


def valid_moves(b):
    n_moves = []
    moves = [None, None, None, None, None, None, None]
    for i in range(5, -1, -1):
        for a in range(7):
            if moves[a] is None and b[i][a] == 0:
                moves[a] = (i, a)
                n_moves.append((i, a))
    return n_moves


# Test case
'''
b = [[1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0]]
print(valid_moves(b))
'''


# Updates the board with a move
def update_board_pos(b, move, player):
    b[move[0]][move[1]] = player
    return b


# Asks the user for a move and updates the board based on the given move
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


# Prints the current game board
def p_board(b):
    for row in b:
        for col in row:
            print('{} '.format(col), end='')
        print('\n', end='')
    print()


# Takes two positions and adds them to the board database
def add_to_db(b1, b2, board_db):
    board_db[str(b1)] = b2
    return board_db


# Converts an array board to a binary board
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


# Converts a binary board to an array
def binary_to_board(b):
    board = []
    for i in range(0, 36, 7):
        row = []
        for a in range(7):
            row.append(int(b[0][i + a]))
        board.append(row)
    return board

#newcomment
# Checks if the current board position is in the database. If it is it returns the 'best' move
def check_database(database, position):
    if str(position) in database:
        return database[str(position)]

def evaluate_window(window, player):
    score = 0
    opp_piece = [1, 2]
    opp_piece.remove(int(player))
    opp_piece = opp_piece[0]

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_position(board, player, opponent=False):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[3])]
    center_count = center_array.count(player)
    score += center_count * 3

    ## Score Horizontal
    for r in range(6):
        row_array = [int(i) for i in list(board[r])]
        for c in range(7-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)

    ## Score Vertical
    for c in range(7):
        col_array = [list(board[i][c] for i in range(6))]
        for r in range(6-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    ## Score posiive sloped diagonal
    for r in range(6-3):
        for c in range(7-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    for r in range(6-3):
        for c in range(7-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    opp_piece = [1, 2]
    opp_piece.remove(int(player))
    opp_piece = opp_piece[0]
    if not opponent:
        score -= score_position(board, opp_piece, opponent = True)
    return score


def possible_scored_moves(board, player):
    moves = []
    for m in valid_moves(board):
        new_b = update_board_pos(copy.deepcopy(board), m, player)
        moves.append((score_position(new_b, player), m))
    moves.sort(reverse=True)
    print(moves)
    return moves[0][1]


# !Added
# Checks if the play can win on the next move
def immediate_win(board, player):
    for m in valid_moves(board):
        new_b = update_board_pos(copy.deepcopy(board), m, player)
        if check_for_win(new_b) == player:
            print('This wins')
            p_board(new_b)
            return m


# !Added
# Checks if the player can win in three moves
def three_move_win(board, player):
    if player == 2:
        o_player = 1
    else:
        o_player = 2
    # First branch
    for m in valid_moves(board):
        new_b = update_board_pos(copy.deepcopy(board), m, player)
        c = 0
        # Second branch
        for a in valid_moves(new_b):
            new_bb = update_board_pos(copy.deepcopy(new_b), a, o_player)
            if check_for_win(new_bb) != o_player:
                # Third branch
                for i in valid_moves(new_bb):
                    new_bbb = update_board_pos(copy.deepcopy(new_bb), i, player)
                    if check_for_win(new_bbb) == player:
                        c += 1
                        break
        if c == len(valid_moves(new_b)):
            return m


# print(three_move_win(board, 2))
# ! IDK if it works
def five_move_win(board, player, best=False):
    max_m = 0
    best_m = None
    if player == 2:
        o_player = 1
    else:
        o_player = 2
    # Creates first branch of boards
    for m in valid_moves(board):
        c = 0
        new_b1 = update_board_pos(copy.deepcopy(board), m, player)
        # Creates second branch of boards
        for a in valid_moves(new_b1):
            new_b2 = update_board_pos(copy.deepcopy(new_b1), a, o_player)
            if check_for_win(new_b2) != o_player:
                # Creates third branch of boards
                for i in valid_moves(new_b2):
                    c2 = 0
                    new_b3 = update_board_pos(copy.deepcopy(new_b2), i, player)
                    # Creates fourth branch of boards
                    for o in valid_moves(new_b3):
                        new_b4 = update_board_pos(copy.deepcopy(new_b3), o, o_player)
                        if check_for_win(new_b4) != o_player:
                            # Creates fifth branch of boards
                            for z in valid_moves(new_b4):
                                new_b5 = update_board_pos(copy.deepcopy(new_b4), z, player)
                                if check_for_win(new_b5) == player:
                                    c2 += 1
                                    break
                    if c2 == len(valid_moves(new_b3)):
                        c += 1
                        break
        if c >= len(valid_moves(new_b1)):
            return m
        if best == True and c > max_m:
            best_m = m
            max_m = c
    if best == True:
        return best_m


def shoot_in_foot(board, move, player, other, n):
    up_board = update_board_pos(copy.deepcopy(board), move, player)
    print(u)
    if immediate_win(copy.deepcopy(up_board), other):
        return False
    if three_move_win(copy.deepcopy(up_board), other) and n > 3:
        return False
    if five_move_win(copy.deepcopy(up_board), other) and n > 5:
        return False
    return True

def take_the_middle(board):
    if sum(board[5][:3] + board[5][4:]) == 0 or board[5][3] == 0:
        count = 0
        for i in range(6):
            if board[i][3] == 0:
                count += 1
        if count > 0:
            return 3
    
# Test case Should return 1
'''
board = [[0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 1, 0, 0],
        [0, 0, 0, 1, 2, 0, 0],
        [0, 2, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 2, 2, 0],
        [0, 2, 1, 2, 2, 1, 0]]
print('Move',five_move_win(board, 1))

# Test case Should return 1,2

board = [[0, 0, 0, 1, 1, 0, 0],
        [2, 0, 0, 2, 2, 0, 0],
        [1, 0, 0, 1, 2, 0, 0],
        [2, 0, 2, 1, 1, 0, 0],
        [1, 2, 1, 1, 2, 1, 0],
        [2, 2, 1, 2, 2, 1, 2]]
print('Move',five_move_win(board, 1))

board = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0]]
print('Move',five_move_win(board, 1))
'''


# ! We should still build a partial database and check it first.
# Calls multiple method to try and find the best move
def find_a_move(board, player, other):
    # Checks for immediate win
    middle = take_the_middle(board)
    if middle:
        print('Middle')
        return middle

    im_win = immediate_win(copy.deepcopy(board), player)
    if im_win:
        print('Immediate win')
        return im_win[1]

    # Checks if the other player can win if we don't block
    o_im_win = immediate_win(copy.deepcopy(board), other)
    if o_im_win and shoot_in_foot(board, o_im_win, player, other, 3):
        print('Opponent immediate win')
        return o_im_win[1]

    # Checks for three move win
    three_win = three_move_win(copy.deepcopy(board), player)
    if three_win and shoot_in_foot(board, three_win, player, other, 3):
        print('Win in 3')
        return three_win[1]

    # Checks if the other player can win in 3 moves if we don't block
    o_three_win = three_move_win(copy.deepcopy(board), other)
    if o_three_win and shoot_in_foot(board, o_three_win, player, other, 3):
        print('Opponent win in 3')
        return o_three_win[1]

    # Checks for five move win
    five_win = five_move_win(copy.deepcopy(board), player)
    if five_win and shoot_in_foot(board, five_win, player, other, 5):
        print('Win in 5')
        return five_win[1]

    # Checks if the other player can win in five moves if we don't block
    o_five_win = five_move_win(copy.deepcopy(board), other)
    if o_five_win and shoot_in_foot(board, o_five_win, player, other, 5):
        print('Opponent win in 5')
        return o_five_win[1]

    #Checks for a move based on rating
    
    scored_move = possible_scored_moves(copy.deepcopy(board), player)
    if scored_move and shoot_in_foot(board, scored_move, player, other, 7):
        print(shoot_in_foot(board, scored_move, player, other, 7))
        print('Possible scored move')
        return scored_move[1]
    
    # Last resort returns the highest performing move
    possible_good_move = five_move_win(copy.deepcopy(board), player, True)
    if possible_good_move and shoot_in_foot(board, possible_good_move, player, other, 7):
        print('Possible good move')
        return possible_good_move[1]

    # If nothing else can generate a move a random move is chosen
    L_moves = valid_moves(board)
    random.shuffle(L_moves)
    for m in L_moves:
        if shoot_in_foot(board, m, player, other, 7):
            print('Random non foot shooting move')
            return m[1]

    if five_move_win(copy.deepcopy(board), player, True):
        print('Least bad suicide move')
        return five_move_win(copy.deepcopy(board), player, True)[1]

    print('Suicide move (jumps off a bridge)')
    return random.choice(L_moves)[1]
"""
board = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0]]
print(find_a_move(board, 1, 2))

# Test case Should return 3

board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 0, 0, 0, 0],
         [2, 2, 2, 1, 0, 0, 0],
         [2, 2, 2, 1, 0, 0, 0]]
print('Move', find_a_move(board, 2, 1))

board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 2, 2, 1, 2, 0, 0],
         [1, 2, 1, 1, 2, 0, 0]]
print('Move', find_a_move(board, 2, 1))

board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]]
print('Move', find_a_move(board, 2, 1))

board = [[0, 0, 0, 2, 0, 0, 0],
         [0, 0, 1, 1, 2, 0, 0],
         [0, 1, 2, 2, 2, 1, 0],
         [1, 2, 2, 1, 1, 1, 2],
         [2, 1, 2, 2, 1, 2, 1],
         [1, 2, 1, 1, 2, 1, 2]]
print('Move', find_a_move(board, 1, 2))
print(immediate_win(copy.deepcopy(board), 1))
"""
board = [[0,0,0,1,0,0,0],
         [0,0,0,2,0,0,0],
         [0,0,0,2,0,1,2],
         [0,0,1,2,0,2,1],
         [0,0,2,1,0,1,2],
         [0,0,1,2,0,1,1]]
print('Move', find_a_move(board, 1, 2))


if __name__ == "__main__":

    '''
    old_board = board 
    print('\n')
    board_db = dict()
    count = 1

    while check_for_win(board) == 0:
        #Checks which players turn it is
        if count % 2 == 0:
            p = 2
        else:
            p = 1
        #Updates the board with the users choice
        board = user_choice(board, p)

        #Adds the board to the dictionary database 
        add_to_db(board_to_binary(board), board_to_binary(old_board), board_db)
        #Assigns the current board to the old board
        old_board = board 
        count += 1

    #prints the final board along with who won the game
    p_board(board)
    print('Player {} wins congrats'.format(p))

    #Saves the game data to a data.txt file to use as a future table base reference
    data = open('data.txt', 'w')
    data.write(json.dumps(board_db))
    data.close()

    '''


    async def game_loop(uri, created):
        # Test case
        counter = 0
        board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        if created:
            self = 1
            other = 2
        else:
            self = 2
            other = 1

        async with websockets.connect(uri) as socket:
            while True:
                message = await socket.recv()
                print(message, flush=True)
                time.sleep(1)
                command = message.split(':')

                if (command[0] == 'ID'):
                    print(command[1])
                elif ((command[0] == "GAMESTART" and created) or command[0] == "OPPONENT"):
                    for move in valid_moves(board):
                        if len(command) == 2 and move[1] == int(command[1]):
                            board = update_board_pos(board, move, other)
                            counter += 1
                    print(counter)
                    p_board(board)
                    move = find_a_move(board, self, other)
                    for m in valid_moves(board):
                        if m[1] == move:
                            board = update_board_pos(board, m, self)
                            counter += 1
                            print(counter)
                            p_board(board)
                    await socket.send(f'Play:{move}')


    uri = None
    server = 'ws://' + input('Server IP: ').strip()
    protocol = input('Do you want to join or create a game? (j/c): ').strip().lower()

    if protocol == 'c':
        uri = server + '/create'

    else:
        game_id = input('Game id: ').strip()
        uri = server + '/join/' + game_id

    asyncio.run(game_loop(uri, protocol == 'c'))