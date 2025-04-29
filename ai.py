import random
import copy

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
            # Purely random
            return random.choice(available_moves)

        elif difficulty == "medium":
            # 80% random, 20% blocking/winning move
            if random.random() < 0.8:
                return random.choice(available_moves)
            else:
                return self.smart_move(game, available_moves)

        elif difficulty == "hard":
            # Always use smart logic (block, win)
            return self.smart_move(game, available_moves)

        # Fallback
        return random.choice(available_moves)

    def smart_move(self, game, available_moves):
        # 1. Try to win
        for move in available_moves:
            temp_game = copy.deepcopy(game)
            temp_game.make_move(*move, 2)  # AI = 2
            if temp_game.check_win(2):
                return move

        # 2. Try to block player's win
        for move in available_moves:
            temp_game = copy.deepcopy(game)
            temp_game.make_move(*move, 1)  # Player = 1
            if temp_game.check_win(1):
                return move

        # 3. Otherwise: prefer center or random
        preferred = [(1,1,1), (2,2,2), (1,2,1), (2,1,2)]
        for move in preferred:
            if move in available_moves:
                return move

        return random.choice(available_moves)
