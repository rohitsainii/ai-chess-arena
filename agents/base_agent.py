class ChessAgent:
    def __init__(self, name):
        self.name = name

    def select_move(self, board):
        raise NotImplementedError("Must implement select_move()")
