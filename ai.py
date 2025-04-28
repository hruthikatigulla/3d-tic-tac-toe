# ai.py

import copy

class TicTacToeAI:
    def __init__(self, player=2, opponent=1):
        self.player = player      # AI is player 2
        self.opponent = opponent  # Human is player 1

    def get_valid_moves(self, board):
        # Returns all empty positions as (x, y, z) tuples
        moves = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if board[x][y][z] == 0:
                        moves.append((x, y, z))
        return moves

    def evaluate(self, game_board):
        # Simple evaluation: +1000 for AI win, -1000 for Human win, 0 otherwise
        if game_board.check_win(self.player):
            return 1000
        elif game_board.check_win(self.opponent):
            return -1000
        else:
            return 0

    def minimax(self, game_board, depth, alpha, beta, maximizing):
        if game_board.check_win(self.player) or game_board.check_win(self.opponent) or game_board.is_draw() or depth == 0:
            return self.evaluate(game_board), None

        valid_moves = self.get_valid_moves(game_board.get_board())
        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(game_board)
                board_copy.make_move(*move, self.player)
                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(game_board)
                board_copy.make_move(*move, self.opponent)
                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def find_best_move(self, game_board, difficulty):
        # Set depth based on difficulty
        if difficulty == 'easy':
            depth = 2
        elif difficulty == 'difficult':
            depth = 4
        elif difficulty == 'insane':
            depth = 6
        else:
            depth = 2
        _, move = self.minimax(game_board, depth, float('-inf'), float('inf'), True)
        return move
