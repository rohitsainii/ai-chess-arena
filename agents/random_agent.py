import random

class RandomAgent:
    def get_move(self, board):
        return random.choice(list(board.legal_moves))
