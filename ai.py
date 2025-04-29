import random

class TicTacToeAI:
    def get_best_move(self, game, difficulty="easy"):
        available_moves = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] == 0:
                        available_moves.append((x, y, z))

        if not available_moves:
            return None

        if difficulty == "easy":
            # Completely random move
            return random.choice(available_moves)

        elif difficulty == "medium":
            # 70% random, 30% smarter move (prefers center)
            if random.random() < 0.7:
                return random.choice(available_moves)
            else:
                if (1, 1, 1) in available_moves:
                    return (1, 1, 1)
                if (2, 2, 2) in available_moves:
                    return (2, 2, 2)
                return random.choice(available_moves)

        elif difficulty == "hard":
            # Prefer center or strategic moves first
            preferred_moves = [(1,1,1), (2,2,2), (1,2,1), (2,1,2)]
            for move in preferred_moves:
                if move in available_moves:
                    return move
            # Otherwise, pick random
            return random.choice(available_moves)

        else:
            # Fallback: random move
            return random.choice(available_moves)
