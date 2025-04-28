from flask import Flask, render_template, request, redirect, url_for, session
from game_logic import GameBoard
from ai import TicTacToeAI

app = Flask(__name__)
app.secret_key = "tic-tac-toe-3d"

# Utility to store/retrieve game state in session
def get_game():
    if 'game' not in session:
        session['game'] = GameBoard().to_dict()
    game = GameBoard.from_dict(session['game'])
    return game

def save_game(game):
    session['game'] = game.to_dict()

@app.route("/", methods=["GET", "POST"])
def index():
    game = get_game()
    ai = TicTacToeAI()
    message = ""
    if request.method == "POST":
        x = int(request.form["x"])
        y = int(request.form["y"])
        z = int(request.form["z"])
        if game.is_valid_move(x, y, z):
            game.make_move(x, y, z, 1)
            if not game.check_win(1) and not game.is_draw():
                ai_move = ai.find_best_move(game, "easy")
                if ai_move:
                    game.make_move(*ai_move, 2)
        save_game(game)
        return redirect(url_for("index"))

    board = game.get_board()
    winner = None
    if game.check_win(1):
        winner = "You win!"
    elif game.check_win(2):
        winner = "AI wins!"
    elif game.is_draw():
        winner = "It's a draw!"

    return render_template(
        "index.html", board=board, winner=winner, game=game
    )

@app.route("/restart")
def restart():
    session.pop('game', None)
    return redirect(url_for("index"))

# --- Add these methods to your GameBoard class in game_logic.py ---
# def to_dict(self):
#     return {"board": self.board, ...}
# @classmethod
# def from_dict(cls, d):
#     inst = cls()
#     inst.board = d["board"]
#     ...
#     return inst

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
