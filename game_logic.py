# game_logic.py

class GameBoard:
    def __init__(self):
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    def reset(self):
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    def is_valid_move(self, x, y, z):
        return self.board[x][y][z] == 0

    def make_move(self, x, y, z, player):
        # player: 1 for human, 2 for AI
        if self.is_valid_move(x, y, z):
            self.board[x][y][z] = player
            return True
        return False

    def get_board(self):
        return self.board

    def check_win(self, player):
        lines = []

        # Rows, columns and verticals
        for i in range(4):
            for j in range(4):
                # Rows in each layer
                lines.append([(i, j, k) for k in range(4)])
                # Columns in each layer
                lines.append([(i, k, j) for k in range(4)])
                # Verticals
                lines.append([(k, i, j) for k in range(4)])

        # Diagonals in each layer
        for i in range(4):
            lines.append([(i, k, k) for k in range(4)])
            lines.append([(i, k, 3 - k) for k in range(4)])
            lines.append([(k, i, k) for k in range(4)])
            lines.append([(k, i, 3 - k) for k in range(4)])
            lines.append([(k, k, i) for k in range(4)])
            lines.append([(k, 3 - k, i) for k in range(4)])

        # Main space diagonals
        lines.append([(k, k, k) for k in range(4)])
        lines.append([(k, k, 3 - k) for k in range(4)])
        lines.append([(k, 3 - k, k) for k in range(4)])
        lines.append([(3 - k, k, k) for k in range(4)])

        # Check all lines
        for line in lines:
            if all(self.board[x][y][z] == player for x, y, z in line):
                return True
        return False

    def is_draw(self):
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if self.board[x][y][z] == 0:
                        return False
        return True

    # For Flask session (store/load game)
    def to_dict(self):
        return {'board': self.board}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.board = data['board']
        return obj

# Optional: Add any extra methods you need here for AI, etc.
