"""
Tic Tac Toe Player
"""

import math
import copy
from pydoc import TextDoc

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    oneDBoard = flatten(board)
    if oneDBoard.count(X) == oneDBoard.count(O):
        return X
    else:
        return O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    emptySquares = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                emptySquares.add((i,j))
    return emptySquares



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (x,y) = action
    if board[x][y] != EMPTY:
        raise IllegalMoveError
    else:
        resultBoard = copy.deepcopy(board)
        resultBoard[x][y] = player(board)
        return resultBoard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if playerWon(board,X): return X
    if playerWon(board,O): return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None) or (flatten(board).count(EMPTY) == 0): return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # Behold this pinnacle of style, but alas the course's automatic grader
    # runs an older version of python.

    # match winner(board):
    #     case "X":
    #         return 1
    #     case "O":
    #         return -1
    #     case None:
    #         return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return None

    bestAction = None
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        value = -math.inf
        for action in actions(board):
            aVal = minVal(result(board, action), alpha, beta)
            if aVal > value:
                bestAction = action
                value = aVal

    elif player(board) == O:
        value = math.inf
        for action in actions(board):
            aVal = maxVal(result(board, action), alpha, beta)
            if aVal < value:
                bestAction = action
                value = aVal
    
    return bestAction

def maxVal(board, alpha, beta):
    if terminal(board): return utility(board)

    v = -math.inf
    for action in actions(board):
        actionVal = minVal(result(board, action), alpha, beta)
        v = max(v, actionVal)
        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def minVal(board, alpha, beta):
    if terminal(board): return utility(board)

    v = math.inf
    for action in actions(board):
        actionVal = maxVal(result(board,action), alpha, beta)
        v = min(v, actionVal)
        if v <= alpha: return v
        beta = min(beta, v)
    return v

def flatten(nested, oneD = None):
    """
    Returns a one dimensional list containing all the values of a nested input.
    """
    if oneD == None:
        oneD = []
    for item in nested:
        if type(item) == type([]):
            flatten(item, oneD)
        else:
            oneD.append(item)
    return oneD

def playerWon(board, player):
    """
    Returns true if player won the game. False otherwise.
    """
    condition = 3 * [player]
    # Check rows
    for row in board:
        if row == condition:
            return True
    # Check columnss
    for column in transpose(board):
        if column == condition:
            return True
    # CHeck diagonals
    if ([board[0][0], board[1][1], board[2][2]] == condition) or \
        ([board[2][0], board[1][1], board[0][2]] == condition):
        return True
    return False

def transpose(board):
    """
    Return a copy of the board, rows and columns swapped.
    """
    tBoard = copy.deepcopy(board)
    for i in range(3):
        for j in range(3):
            tBoard[i][j] = board[j][i]
    return tBoard



class IllegalMoveError(Exception):
    """Raised when attempting an illegal move."""
    pass