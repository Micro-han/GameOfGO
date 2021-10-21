__all__ = [
    'Agent',
]


class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()

    def diagnostics(self):
        return {}
