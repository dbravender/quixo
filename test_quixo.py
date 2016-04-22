from quixo import QuixoGame, QuixoPlayer
from random import randint
game = QuixoGame(num_players=2, grid_size=5)

for i in range(100):
    game.print_game()
    moves = game.get_moves()
    index = randint(0, len(moves) - 1)
    game.apply_move(moves[index])
    if game.check_for_winner():
        break

game.print_game()
print(game.determine_winner())
