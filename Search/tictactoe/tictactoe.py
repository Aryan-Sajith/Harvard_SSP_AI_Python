"""
Tic Tac Toe Player
"""
import math
import copy

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

    # Checks if board is starting state
    if board == initial_state():
        return X

    # This part works based on x vs o comparison(if equal then it's x's turn, otherwise o's turn)
    x = 0
    o = 0
    for row in board:
        x += row.count(X)
        o += row.count(O)

    if x == o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Creates a list of viable actions and returns
    potential_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                potential_moves.append([row, col])
    return potential_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Creates a copy of board for action considerations
    temp_board = copy.deepcopy(board)

    # This part raises and handles the error and returns a board state for consideration
    try:
        if temp_board[action[0]][action[1]] != EMPTY:
            raise Exception("Invalid action choice!")
        else:
            temp_board[action[0]][action[1]] = player(temp_board)
            return temp_board
    except "Invalid action choice!":
        print('Invalid action chosen.')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checks for horizontal wins
    for row in board:
        x_count = row.count(X)
        o_count = row.count(O)
        if x_count == 3:
            return X
        if o_count == 3:
            return O

    # Checks for vertical wins[ I'm not sure how to iterate the 2-d list since None objects can't be iterated]
    if board[0][0] == O and board[0][1] == O and board[0][2] == O:
        return O
    if board[0][0] == X and board[0][1] == X and board[0][2] == X:
        return X
    if board[1][0] == O and board[1][1] == O and board[1][2] == O:
        return O
    if board[1][0] == X and board[1][1] == X and board[1][2] == X:
        return X
    if board[2][0] == O and board[2][1] == O and board[2][2] == O:
        return O
    if board[2][0] == X and board[2][1] == X and board[2][2] == X:
        return X

    # Checks for diagonal wins
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X

    # Returns none based on no win condition
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # This part establishes if board is full or someone has won(by counting the number of empty spots on the board)
    empty_vals = 0
    for row in board:
        empty_vals += row.count(EMPTY)
    if empty_vals == 0:
        return True
    elif winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Base cases for minimax algo eventually
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    # Establishes current player as a var and defines final action var
    current_agent = player(board)
    best_move = ()

    if current_agent == X:
        reference = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))  # FIXED
            if value > reference:
                reference = value
                best_move = action
    else:
        reference = math.inf
        for action in actions(board):
            value = max_value(result(board, action))  # FIXED
            if value < reference:
                reference = value
                best_move = action
    return best_move


# function maxing helper provided in lecture
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


# function minimizing helper provided in lecture
def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
