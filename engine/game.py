import random
import chess
class ChessGame:
    def __init__(self, white_agent, black_agent):
        self.white_agent = white_agent
        self.black_agent = black_agent
        self.move_count = 0

    def play_one_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return
        move = random.choice(legal_moves)
        board.push(move)   # ❌ pushing here

