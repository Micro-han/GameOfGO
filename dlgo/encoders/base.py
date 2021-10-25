import importlib

__all__ = [
    'Encoder',
    'get_encoder_by_name',
]


class Encoder:
    def name(self):
        # 编码器名称输出到日志中并存储
        raise NotImplementedError()

    def encode(self, game_state):
        # 围棋棋盘转换为数值
        raise NotImplementedError()

    def encode_point(self, point):
        # 交叉点转换为整数索引
        raise NotImplementedError()

    def decode_point_index(self, index):
        # 索引转换为围棋棋盘的交叉点
        raise NotImplementedError()

    def num_points(self):
        # 交叉点总数
        raise NotImplementedError()

    def shape(self):
        # 棋盘结构编码后的形状
        raise NotImplementedError()


# 根据编码器的名称创建实例
def get_encoder_by_name(name, board_size):
    if isinstance(board_size, int):
        board_size = (board_size, board_size)
    module = importlib.import_module('dlgo.encoders.' + name)
    constructor = getattr(module, 'create')
    return constructor(board_size)

