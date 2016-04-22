from six.moves import input

from mittmcts import MCTS, Draw
from quixo import QuixoGame


def main():
    state = QuixoGame.initial_state()
    number_of_turns = 0
    while True:
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
            result = (MCTS(QuixoGame, state)
                      .get_simulation_result(1))
        else:
            result = (MCTS(QuixoGame, state)
                      .get_simulation_result(100))

        state = QuixoGame.apply_move(state, result.move)

if __name__ == '__main__':
    main()
