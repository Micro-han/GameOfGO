import enum
from collections import namedtuple


class Player(enum.Enum):
    # 表示棋手类
    black = 1
    white = 2

    @property
    def other(self):
        # 轮流落子
        return Player.black if self == Player.white else Player.white


class Point(namedtuple('Point', 'row col')):
    # 表示交叉点的具体坐标
    # Point.row 和 Point.col 代替Point[0]、Point[1]
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
