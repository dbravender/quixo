from quixo import QuixoGame
from random import randint
game = QuixoGame
state = QuixoGame.initial_state()

for i in range(100):
    game.print_board(state)
    moves = game.get_moves(state)
    index = randint(0, len(moves) - 1)
    state = game.apply_move(state, moves[index])
    if game.get_winner(state):
        break

game.print_board(state)
print(game.get_winner(state))
