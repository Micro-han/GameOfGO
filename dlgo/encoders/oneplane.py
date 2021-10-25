import numpy as np
from dlgo.encoders.base import Encoder
from dlgo.goboard import Point


# 一平面编码器 黑白无
class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):
        return 'oneplane'

    # 对于棋盘上每一个交叉点，如果落下的是 我的 就是1 对面的 就是-1 空就是0
    def encode(self, game_state):
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix

    # 棋盘交叉点转换为整数索引
    def encode_point(self, point):
        return self.board_width * (point.row - 1) + (point.col - 1)

    # 索引转换为围棋棋盘的交叉点
    def decode_point_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    # 交叉点总数
    def num_points(self):
        return self.board_width * self.board_height

    # 棋盘结构编码后的形状
    def shape(self):
        return self.num_planes, self.board_height, self.board_width


# 编码器创建方法
def create(board_size):
    return OnePlaneEncoder(board_size)
