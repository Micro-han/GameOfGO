import numpy as np
from dlgo.encoders.base import Encoder
from dlgo.goboard import Move, Point


# 七平面编码器
# 第一平面：1口气的白子编码为1，其他为0
# 第二平面：2口气的白子编码为1，其他为0、第三平面同理
# 456平面为黑子 对应 123的白子
# 打劫不能落子的点标记为1
class SevenPlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 7

    def name(self):
        return 'sevenplane'

    def encode(self, game_state):
        board_tensor = np.zeros(self.shape())
        base_plane = {game_state.next_player: 0,
                      game_state.next_player.other: 3}
        for row in range(self.board_height):
            for col in range(self.board_width):
                p = Point(row=row + 1, col=col + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    # 将打劫规则编入特征
                    if game_state.does_move_violate_ko(game_state.next_player,
                                                       Move.play(p)):
                        board_tensor[6][row][col] = 1
                else:
                    liberty_plane = min(3, go_string.num_liberties) - 1
                    liberty_plane += base_plane[go_string.color]
                    board_tensor[liberty_plane][row][col] = 1
                    # 将七口多的黑子白子继续编码
        return board_tensor

    def encode_point(self, point):
        return self.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width


def create(board_size):
    return SevenPlaneEncoder(board_size)
