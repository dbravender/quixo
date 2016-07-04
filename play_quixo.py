from mittmcts import MCTS, Draw
from quixo import QuixoGame
from random import randint


def main():
    state = QuixoGame.initial_state()
    number_of_turns = 0
    while True:
        QuixoGame.print_board(state)
        number_of_turns += 1
        if state.winner:
            QuixoGame.print_board(state)
            print('Number of turns {}'.format(number_of_turns))
            if state.winner is Draw:
                print('Draw!')
            elif state.winner:
                print(state.winner + ' wins')
            break

        if state.current_player > 0:
            _, moves = QuixoGame.get_moves(state)
            index = randint(0, len(moves) - 1)
            move = moves[index]

        else:
            result = (MCTS(QuixoGame, state)
                      .get_simulation_result(50))
            move = result.move
        state = QuixoGame.apply_move(state, move)

if __name__ == '__main__':
    main()
