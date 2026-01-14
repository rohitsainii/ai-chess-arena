import chess
import math

class MinimaxAgent:
    def __init__(self, base_depth=2):
        self.base_depth = base_depth
        self.name = "Minimax++"

    # -----------------------------
    # Dynamic depth based on game
    # -----------------------------
    def get_depth(self, board):
        piece_count = len(board.piece_map())
        if piece_count > 20:
            return self.base_depth
        elif piece_count > 10:
            return self.base_depth + 1
        else:
            return self.base_depth + 2

    # -----------------------------
    # Evaluation with heuristics
    # -----------------------------
    def evaluate(self, board):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }

        score = 0
        for piece, value in values.items():
            score += len(board.pieces(piece, chess.WHITE)) * value
            score -= len(board.pieces(piece, chess.BLACK)) * value

        # 🔥 CHECK BONUS
        if board.is_check():
            score += -2 if board.turn else 2

        # 🔥 KING SAFETY
        score += self.king_safety(board, chess.WHITE)
        score -= self.king_safety(board, chess.BLACK)

        return score

    def king_safety(self, board, color):
        king_sq = board.king(color)
        if king_sq is None:
            return -100  # lost king (theoretical)

        attackers = board.attackers(not color, king_sq)
        return -0.5 * len(attackers)

    # -----------------------------
    # Minimax
    # -----------------------------
    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)

        if maximizing:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # -----------------------------
    # Unified interface
    # -----------------------------
    def select_move(self, board):
        depth = self.get_depth(board)
        best_move = None
        best_value = -math.inf

        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(board, depth - 1, -math.inf, math.inf, False)
            board.pop()
            if value > best_value:
                best_value = value
                best_move = move

        return best_move
