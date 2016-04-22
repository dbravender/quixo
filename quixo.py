import numpy as np
from collections import namedtuple


class QuixoMove(object):

    def __init__(self, space, player, roll):
        self.space = space
        self.player = player
        self.roll = roll

class QuixoGame(object):

    State = namedtuple('QuixoState', ['board', 'current_player', 'winner'])

    def __init__(self, board_size=5, num_players=2):
        self.num_players = num_players
        self.board_size = board_size
        self.board = np.zeros((self.board_size, self.board_size), dtype=np.int)
        boundary_indexes = np.array([(0, i) for i in range(self.board_size)] +
                                    [(self.board_size - 1, i) for i in range(self.board_size)] +
                                    [(i, 0) for i in range(1, self.board_size - 1)] +
                                    [(i, self.board_size - 1) for i in range(self.board_size - 1)])
        self.boundary_xs, self.boundary_ys = boundary_indexes.T
        self.char_map = np.array([' ', 'o', 'x'])
        self.current_player = 1


        return QuixoGame()

    @classmethod
    def initial_state(state):
        state.board[:] = 0
        state.current_player = 1

    @classmethod
    def apply_move(cls, state, move):
        new_game = QuixoGame(self.board_size, self.num_players)
        new_game.board[:] = self.board[:]
        new_game.current_player = self.current_player * -1
        new_game.board[move.space[0], move.space[1]] = move.player
        move.roll(new_game)
        return new_game

    @staticmethod
    def roll_x(state, position, direction):
        def roll(state):
            state.board[position] = np.roll(state.board[position], shift=1)
        return roll

    @staticmethod
    def roll_y(state, position, direction):
        def roll(state):
            state.board[:, position] = np.roll(state.board[:, position], shift=1)
        return roll

    @staticmethod
    def state(state):
        return str(state.board) + str(state.current_player)

    @staticmethod
    def get_selectable_blocks(state):
        selectable_blocks = np.where(
            np.logical_or(
                state.board[state.boundary_xs, state.boundary_ys] == 0,
                state.board[state.boundary_xs,
                          state.boundary_ys] == state.current_player
            )
        )[0]
        return selectable_blocks

    @staticmethod
    def get_moves(state):
        blocks = state.get_selectable_blocks()
        bxs = state.boundary_xs[blocks]
        bys = state.boundary_ys[blocks]
        
        moves = list()
        for bx, by in zip(bxs, bys):
            moves.extend([
                QuixoMove((bx, by), state.current_player, state.roll_x(bx, 1)),
                QuixoMove((bx, by), state.current_player, state.roll_x(bx, -1)),
                QuixoMove((bx, by), state.current_player, state.roll_y(by, 1)),
                QuixoMove((bx, by), state.current_player, state.roll_y(by, -1))
            ])
        return moves

    @staticmethod
    def check_for_winner(state):
        return any(abs(np.sum(state.board, axis=0)) == state.board_size) or\
            any(abs(np.sum(state.board, axis=1)) == state.board_size) or\
            abs(np.sum((state.board.diagonal()))) == state.board_size or\
            abs(np.sum((state.board[::-1].diagonal()))) == state.board_size

    @staticmethod
    def get_winner(state):
        winning_players = list()
        row_sums = np.sum(state.board, axis=0)
        win_rows = np.where(np.abs(row_sums) == state.board_size)[0]
        if len(win_rows) > 0:
            winning_players.extend(np.sign(row_sums[win_rows]))
        
        col_sums = np.sum(state.board, axis=1)
        win_cols = np.where(np.abs(col_sums) == state.board_size)[0]
        if len(win_cols) > 0:
            winning_players.extend(np.sign(col_sums[win_cols]))

        diag0 = np.sum((state.board.diagonal()))
        diag1 = np.sum((state.board[::-1].diagonal()))
        for diag in [diag0, diag1]:
            if abs(diag) == state.board_size:
                winning_players.append(np.sign(diag))

        winning_players = set(winning_players)
        if len(winning_players) > 1:
            return 0
        else:
            return winning_players.pop()

    @staticmethod
    def print_game(state):
        print(' ' + ' '.join(map(str, np.arange(state.board_size))) +
              '\n' + '_' * (state.board_size * 2 + 2))
        for num_row, row in enumerate(state.board):
            print(str(num_row) + '|' + '|'.join(state.char_map[row]) + '|')
        print('_' * (state.board_size * 2 + 2))
