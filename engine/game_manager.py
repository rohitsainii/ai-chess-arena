import chess
import chess.pgn
import time

class GameManager:
    def __init__(self, white_agent, black_agent):
        self.board = chess.Board()
        self.white = white_agent
        self.black = black_agent
        self.moves = []

    def play(self):
        while not self.board.is_game_over():
            agent = self.white if self.board.turn else self.black
            start = time.time()
            move = agent.select_move(self.board)
            self.board.push(move)
            self.moves.append(move)

        return self.board.result(), self.board
