import argparse
import numpy as np

from dlgo.encoders.base import get_encoder_by_name
from dlgo import goboard_fast as goboard
from dlgo import mcts
from dlgo.utils import print_board, print_move


def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []  # <1>

    encoder = get_encoder_by_name('oneplane', board_size)  # <2>

    game = goboard.GameState.new_game(board_size)  # <3>

    bot = mcts.MCTSAgent(rounds, temperature)  # <4>

    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game)  # <5>
        if move.is_play:
            boards.append(encoder.encode(game))  # <6>
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)  # <7>

        print_move(game.next_player, move)
        game = game.apply_move(move)  # <8>
        num_moves += 1
        if num_moves > max_moves:  # <9>
            break

    return np.array(boards), np.array(moves)  # <10>


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60,
                        help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')

    args = parser.parse_args()  # <1>
    xs = []
    ys = []

    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)  # <2>
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)  # <3>
    y = np.concatenate(ys)

    np.save(args.board_out, x)  # <4>
    np.save(args.move_out, y)


if __name__ == '__main__':
    main()