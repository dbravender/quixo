import numpy as np
from collections import namedtuple
from copy import deepcopy


QuixoMove = namedtuple('QuixoMove', ['space', 'player', 'roll'])

boundary_indexes = np.array([(0, i) for i in range(5)] +
                            [(4, i) for i in range(5)] +
                            [(i, 0) for i in range(1, 4)] +
                            [(i, 4) for i in range(1, 4)])

boundary_xs, boundary_ys = boundary_indexes.T

def roll_x(position, direction):
    def roll(board):
        board[position] = np.roll(board[position], shift=1)
    return roll

def roll_y(position, direction):
    def roll(board):
        board[:, position] = np.roll(board[:, position], shift=1)
    return roll

# end unnecessary to compute every time
class QuixoGame(object):

    State = namedtuple('QuixoState', ['board', 'current_player', 'winner'])

    @classmethod
    def initial_state(cls):
        return cls.State(
            board=np.zeros((5, 5), dtype=np.int),
            current_player=1,
            winner=None
            )

    @classmethod
    def apply_move(cls, state, move):
        new_board = deepcopy(state.board)
        new_board[move.space[0], move.space[1]] = move.player
        move.roll(new_board)
        next_player = state.current_player * -1

        winner = cls.determine_winner(new_board) if cls.check_for_winner(new_board) else None

        return cls.State(
            board=new_board,
            current_player=next_player,
            winner=winner
        )


    @staticmethod
    def get_moves(state):
        blocks = np.where(
            np.logical_or(
                state.board[boundary_xs, boundary_ys] == 0,
                state.board[boundary_xs, boundary_ys] == state.current_player
            )
        )[0]

        bxs = boundary_xs[blocks]
        bys = boundary_ys[blocks]

        moves = list()
        for bx, by in zip(bxs, bys):
            moves.extend([
                QuixoMove((bx, by), state.current_player, roll_x(bx, 1)),
                QuixoMove((bx, by), state.current_player, roll_x(bx, -1)),
                QuixoMove((bx, by), state.current_player, roll_y(by, 1)),
                QuixoMove((bx, by), state.current_player, roll_y(by, -1))
            ])
        return moves

    @staticmethod
    def check_for_winner(board):
        return any(abs(np.sum(board, axis=0)) == 5) or\
            any(abs(np.sum(board, axis=1)) == 5) or\
            abs(np.sum((board.diagonal()))) == 5 or\
            abs(np.sum((board[::-1].diagonal()))) == 5

    @staticmethod
    def determine_winner(board):
        winning_players = list()
        row_sums = np.sum(board, axis=0)
        win_rows = np.where(np.abs(row_sums) == 5)[0]
        if len(win_rows) > 0:
            winning_players.extend(np.sign(row_sums[win_rows]))
        
        col_sums = np.sum(board, axis=1)
        win_cols = np.where(np.abs(col_sums) == 5)[0]
        if len(win_cols) > 0:
            winning_players.extend(np.sign(col_sums[win_cols]))

        diag0 = np.sum((board.diagonal()))
        diag1 = np.sum((board[::-1].diagonal()))
        for diag in [diag0, diag1]:
            if abs(diag) == 5:
                winning_players.append(np.sign(diag))

        winning_players = set(winning_players)
        if len(winning_players) > 1:
            return 'Draw'
        else:
            return winning_players.pop()
    
    @staticmethod
    def get_winner(state):
        return state.winner

    @staticmethod
    def print_board(state):
        char_map = np.array([' ', 'o', 'x'])
        print(' ' + ' '.join(map(str, np.arange(5))) +
              '\n' + '_' * (5 * 2 + 2))
        for num_row, row in enumerate(state.board):
            print(str(num_row) + '|' + '|'.join(char_map[row]) + '|')
        print('_' * (5 * 2 + 2))
