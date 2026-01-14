import chess
import random
import math

class MCTSAgent:
    def __init__(self, simulations=200):
        self.simulations = simulations
        self.name = "MCTS"

    def rollout(self, board):
        rollout_board = board.copy()
        while not rollout_board.is_game_over():
            move = random.choice(list(rollout_board.legal_moves))
            rollout_board.push(move)
        result = rollout_board.result()
        if result == "1-0":
            return 1
        elif result == "0-1":
            return -1
        return 0

    def select_move(self, board):
        moves = list(board.legal_moves)
        if not moves:
            return None

        scores = {m: 0 for m in moves}

        for move in moves:
            for _ in range(self.simulations // len(moves)):
                board.push(move)
                score = self.rollout(board)
                board.pop()
                scores[move] += score

        return max(scores, key=scores.get)
