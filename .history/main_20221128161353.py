import json
import asyncio
import websockets
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

#Prints the current game board
def p_board(b):
    for row in b:
        for col in row:
            print('{} '.format(col), end='')
        print('\n', end='')

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

#Checks if the play can win on the next move
def immediate_win(board, player):
    for m in valid_moves(board):
        if 

if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

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

    user_input = input('Do you want to join or create a game? (j/')

