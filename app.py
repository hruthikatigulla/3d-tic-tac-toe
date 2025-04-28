from flask import Flask, render_template, request, redirect, url_for, session
from game_logic import GameBoard
from ai import TicTacToeAI

app = Flask(__name__)
app.secret_key = "tic-tac-toe-3d"

def get_game():
    if 'game' not in session:
        session['game'] = GameBoard().to_dict()
    return GameBoard.from_dict(session['game'])

def save_game(game):
    session['game'] = game.to_dict()

@app.route("/", methods=["GET", "POST"])
def index():
    game = get_game()
    ai = TicTacToeAI()
    message = ""
    difficulty = session.get("difficulty", "easy")

    if request.method == "POST":
        # Handle difficulty change
        if "difficulty" in request.form:
            difficulty = request.form["difficulty"]
            session["difficulty"] = difficulty
            # Don't process a move when changing difficulty
            return redirect(url_for("index"))

        # Handle player move
        x = int(request.form["x"])
        y = int(request.form["y"])
        z = int(request.form["z"])
        if game.is_valid_move(x, y, z):
            game.make_move(x, y, z, 1)
            save_game(game)
            if not game.get_winner() and not game.is_full():
                ai_move = ai.get_best_move(game, difficulty)
                if ai_move:
                    game.make_move(*ai_move, 2)
                    save_game(game)

    winner = game.get_winner()
    return render_template(
        "index.html",
        game=game,
        winner=winner,
        difficulty=difficulty
    )

@app.route("/restart")
def restart():
    session.pop('game', None)
    return redirect(url_for("index"))

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
