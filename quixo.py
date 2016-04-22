import numpy as np


class QuixoMove(object):

    def __init__(self, space, player, roll):
        self.space = space
        self.player = player
        self.roll = roll


class QuixoPlayer(object):

    def __init__(self, game):
        self.game = game


class QuixoGame(object):

    def __init__(self, grid_size=5, num_players=2):
        self.num_players = num_players
        self.grid_size = grid_size
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int)
        self.players = [QuixoPlayer(self) for i in range(self.num_players)]
        boundary_indexes = np.array([(0, i) for i in range(self.grid_size)] +
                                    [(self.grid_size - 1, i) for i in range(self.grid_size)] +
                                    [(i, 0) for i in range(1, self.grid_size - 1)] +
                                    [(i, self.grid_size - 1) for i in range(self.grid_size - 1)])
        self.boundary_xs, self.boundary_ys = boundary_indexes.T
        self.char_map = np.array([' ', 'o', 'x'])
        self.current_player = 1

    def roll_x(self, position, direction):
        def roll():
            self.grid[position] = np.roll(self.grid[position], shift=1)
        return roll

    def roll_y(self, position, direction):
        def roll():
            self.grid[:, position] = np.roll(self.grid[:, position], shift=1)
        return roll

    def state(self):
        return str(self.grid) + str(self.current_player)

    def get_selectable_blocks(self):
        selectable_blocks = np.where(
            np.logical_or(
                self.grid[self.boundary_xs, self.boundary_ys] == 0,
                self.grid[self.boundary_xs,
                          self.boundary_ys] == self.current_player
            )
        )[0]
        return selectable_blocks

    def get_moves(self):
        blocks = self.get_selectable_blocks()
        bxs = self.boundary_xs[blocks]
        bys = self.boundary_ys[blocks]
        
        moves = list()
        for bx, by in zip(bxs, bys):
            moves.extend([
                QuixoMove((bx, by), self.current_player, self.roll_x(bx, 1)),
                QuixoMove((bx, by), self.current_player, self.roll_x(bx, -1)),
                QuixoMove((bx, by), self.current_player, self.roll_y(by, 1)),
                QuixoMove((bx, by), self.current_player, self.roll_y(by, -1))
            ])
        return moves

    def apply_move(self, move):
        self.grid[move.space[0], move.space[1]] = move.player
        move.roll()
        self.current_player *= -1

    def check_for_winner(self):
        return any(abs(np.sum(self.grid, axis=0)) == self.grid_size) or\
            any(abs(np.sum(self.grid, axis=1)) == self.grid_size) or\
            abs(np.sum((self.grid.diagonal()))) == self.grid_size or\
            abs(np.sum((self.grid[::-1].diagonal()))) == self.grid_size

    def determine_winner(self):
        winning_players = list()
        row_sums = np.sum(self.grid, axis=0)
        win_rows = np.where(np.abs(row_sums) == self.grid_size)[0]
        if len(win_rows) > 0:
            winning_players.extend(np.sign(row_sums[win_rows]))
        
        col_sums = np.sum(self.grid, axis=1)
        win_cols = np.where(np.abs(col_sums) == self.grid_size)[0]
        if len(win_cols) > 0:
            winning_players.extend(np.sign(col_sums[win_cols]))

        diag0 = np.sum((self.grid.diagonal()))
        diag1 = np.sum((self.grid[::-1].diagonal()))
        for diag in [diag0, diag1]:
            if abs(diag) == self.grid_size:
                winning_players.append(np.sign(diag))

        winning_players = set(winning_players)
        if len(winning_players) > 1:
            return 0
        else:
            return winning_players.pop()

    def print_game(self):
        print(' ' + ' '.join(map(str, np.arange(self.grid_size))) +
              '\n' + '_' * (self.grid_size * 2 + 2))
        for num_row, row in enumerate(self.grid):
            print(str(num_row) + '|' + '|'.join(self.char_map[row]) + '|')
        print('_' * (self.grid_size * 2 + 2))
