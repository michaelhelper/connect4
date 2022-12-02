#!/usr/bin/env python
import json
import asyncio
import websockets
import copy
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
    n_moves = []
    moves = [None, None, None, None, None, None, None]
    for i in range(5, -1, -1):
        for a in range(7):
            if moves[a] is None and b[i][a] == 0:
                moves[a] = (i, a)
                n_moves.append((i,a))
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

#Updates the board with a move
def update_board_pos(b, move, player):
    b[move[0]][move[1]] = player
    return b


#Asks the user for a move and updates the board based on the given move
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

#Prints the current game board
def p_board(b):
    for row in b:
        for col in row:
            print('{} '.format(col), end='')
        print('\n', end='')
    print()

#Takes two positions and adds them to the board database
def add_to_db(b1, b2, board_db):
    board_db[str(b1)] = b2
    return board_db

#Converts an array board to a binary board
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

#Converts a binary board to an array
def binary_to_board(b):
    board = []
    for i in range(0, 36, 7):
        row = []
        for a in range(7):
            row.append(int(b[0][i + a]))
        board.append(row)
    return board

#Checks if the current board position is in the database. If it is it returns the 'best' move
def check_database(database, position):
    if str(position) in database:
        return database[str(position)]

#!Added
# Checks if the play can win on the next move
def immediate_win(board, player):
    for m in valid_moves(board):
        new_b = update_board_pos(copy.deepcopy(board), m, player)
        if check_for_win(new_b) == player:
            p_board(new_b)
            return m

#!Added
# Checks if the player can win in three moves
def three_move_win(board, player):
    if player == 2:
        o_player = 1
    else:
        o_player = 2
    for m in valid_moves(board):
        new_b = update_board_pos(copy.deepcopy(board), m, player)
        c=0
        for a in valid_moves(new_b):
            new_bb = update_board_pos(copy.deepcopy(new_b), a, o_player)
            if check_for_win(new_bb) != o_player:
                for i in valid_moves(new_bb):
                    new_bbb = update_board_pos(copy.deepcopy(new_bb), i, player)
                    if check_for_win(new_bbb) == player:
                        c += 1
                        break
        if c == len(valid_moves(new_b)):
            return m
    

#print(three_move_win(board, 2))
#Not done yet
def five_move_win(board, player):
    if player == 2:
        o_player = 1
    else:
        o_player = 2
    # Creates first branch of boards
    for m in valid_moves(board):
        c=0
        new_b1 = update_board_pos(copy.deepcopy(board), m, player)
        # Creates second branch of boards
        for a in valid_moves(new_b1):
            new_b2 = update_board_pos(copy.deepcopy(new_b1), a, o_player)
            if check_for_win(new_b2) != o_player:
                # Creates third branch of boards
                for i in valid_moves(new_b2):
                    c2=0
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
        if c == len(valid_moves(new_b1)):
            return m
# Test case Should return 1

board = [[0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 1, 0, 0],
        [0, 0, 0, 1, 2, 0, 0],
        [0, 2, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 2, 2, 0],
        [0, 2, 1, 2, 2, 1, 0]]
print('Move',five_move_win(board, 1))

# Test case Should return 

board = [[0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0],
        [0, 0, 0, 1, 2, 0, 0],
        [0, 0, 2, 1, 1, 0, 0],
        [1, 2, 1, 1, 2, 0, 0],
        [2, 2, 1, 2, 2, 0, 2]]
print('Move',five_move_win(board, 1))

# Calls multiple method to try and find the best move
def find_a_move(board, player, other):
    # Checks for immediate win
    im_win = immediate_win(copy.deepcopy(board), player)
    if im_win:
        return im_win[1]
    print(1)
    # Checks if the other player can win if we don't block
    o_im_win = immediate_win(copy.deepcopy(board), other)
    if o_im_win:
        return o_im_win[1]
    print(2)
    # Checks for three move win
    three_win = three_move_win(copy.deepcopy(board), player)
    if three_win:
        return three_win[1]
    print(3)
    # Checks if the other player can win in 3 moves if we don't block
    o_three_win = three_move_win(copy.deepcopy(board), other)
    if o_three_win:
        return o_three_win[1]

# Test case Should return 3
'''
board = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0],
        [2, 2, 2, 1, 0, 0, 0],
        [2, 2, 2, 1, 0, 0, 0]]
print('Move',find_a_move(board, 2, 1))
'''

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
                command = message.split(':')

                if (command[0] == 'ID'):
                    print(command[1])
                elif ((command[0] == "GAMESTART" and created) or command[0] == "OPPONENT"):
                    for move in valid_moves(board):
                        if move[1] == int(command[1]):
                            board = update_board_pos(board, move, other)
                    p_board(board)
                    move = find_a_move(board, self, other)
                    for m in valid_moves(board):
                        if m[1] == move:
                            board = update_board_pos(board, m, other)
                            p_board(board)
                    await socket.send(f'Play:{move}')



    uri = None
    server = 'ws://' + input('Server IP: ').strip()
    protocol = input('Do you want to join or create a game? (j/c)').strip().lower()
    
    if protocol == 'c':
        uri = server + '/create'

    else:
        game_id = input('Game id: ').strip()
        uri = server + '/join/' + game_id

    asyncio.run(game_loop(uri, protocol == 'c'))