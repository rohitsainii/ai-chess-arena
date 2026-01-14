import chess
import torch
import torch.nn as nn

class ChessNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        return self.net(x)

def board_to_tensor(board):
    tensor = torch.zeros(12, 8, 8)

    mapping = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    for piece in mapping:
        for sq in board.pieces(piece, chess.WHITE):
            r, c = divmod(sq, 8)
            tensor[mapping[piece], r, c] = 1
        for sq in board.pieces(piece, chess.BLACK):
            r, c = divmod(sq, 8)
            tensor[mapping[piece] + 6, r, c] = 1

    return tensor.view(-1)

class NeuralAgent:
    def __init__(self):
        self.name = "Neural Network"
        self.model = ChessNet()

    def select_move(self, board):
        best_move = None
        best_score = -1e9

        for move in board.legal_moves:
            board.push(move)
            with torch.no_grad():
                score = self.model(board_to_tensor(board))
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
