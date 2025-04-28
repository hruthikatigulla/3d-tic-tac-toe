import tkinter as tk
from tkinter import messagebox
from game_logic import GameBoard
from ai import TicTacToeAI
from playsound import playsound
import threading

# For 3D animation
import matplotlib.pyplot as plt

LAYER_COLORS = ["#e0f7fa", "#ffe0b2", "#e1bee7", "#c8e6c9"]
WIN_COLOR = "#ffd600"
PLAYER_COLOR = "#43a047"
AI_COLOR = "#e53935"

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Tic Tac Toe - Unique Edition")
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("easy")
        self.turn_var = tk.StringVar()
        self.turn_var.set("Your turn (X)")

        self.game = GameBoard()
        self.ai = TicTacToeAI()
        self.buttons = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.current_player = 1  # 1 = human, 2 = AI

        self.layer_frames = []
        self.winning_cells = []
        self.pulse_step = 0
        self.create_widgets()
        self.update_board()

        # Animate turn label
        self.flash_on = True
        self.animate_turn_label()

    def create_widgets(self):
        # Top controls (difficulty and turn indicator)
        top_frame = tk.Frame(self.root, bg="#f5f5f5")
        top_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        tk.Label(top_frame, text="Select Difficulty:", bg="#f5f5f5", font=("Segoe UI", 13)).pack(side="left", padx=(16, 2))
        difficulty_dropdown = tk.OptionMenu(top_frame, self.difficulty_var, "easy", "difficult", "insane")
        difficulty_dropdown.config(font=("Segoe UI", 13))
        difficulty_dropdown.pack(side="left", padx=(0, 18))
        self.turn_label = tk.Label(top_frame, textvariable=self.turn_var, font=("Segoe UI", 16, "bold"), fg="blue", bg="#f5f5f5")
        self.turn_label.pack(side="left")

        # Horizontal layers (more padding, bigger font/buttons)
        layers_frame = tk.Frame(self.root, bg="#f5f5f5")
        layers_frame.grid(row=1, column=0, columnspan=4, padx=18, pady=8)
        self.layer_frames = []
        for z in range(4):
            frame = tk.LabelFrame(
                layers_frame, text=f"Layer {z+1} (z={z})",
                padx=8, pady=8,
                bg=LAYER_COLORS[z],
                font=("Segoe UI", 13, "bold"),
                labelanchor="n",
                relief="ridge",
                borderwidth=2
            )
            # Arrange layers horizontally (columns 0 to 3)
            frame.grid(row=0, column=z, padx=16, pady=8, sticky="nsew")
            self.layer_frames.append(frame)
            for x in range(4):
                for y in range(4):
                    btn = tk.Button(
                        frame, text="", width=5, height=2,
                        font=("Segoe UI", 18, "bold"),
                        bg="white", bd=2, relief="groove", activebackground="#b3e5fc",
                        command=lambda x=x, y=y, z=z: self.cell_click(x, y, z)
                    )
                    btn.grid(row=x, column=y, padx=3, pady=3)
                    btn.bind("<Enter>", lambda e, bx=x, by=y, bz=z: self.on_enter(bx, by, bz))
                    btn.bind("<Leave>", lambda e, bx=x, by=y, bz=z: self.on_leave(bx, by, bz))

                    self.buttons[x][y][z] = btn

        # Restart button (centered below layers, bigger)
        self.restart_btn = tk.Button(
            self.root, text="Restart Game", font=("Segoe UI", 13, "bold"),
            command=self.restart, bg="#9fa8da", fg="black", activebackground="#7986cb"
        )
        self.restart_btn.grid(row=2, column=0, columnspan=4, pady=(10, 18), ipadx=12)

    def on_enter(self, x, y, z):
        if self.game.is_valid_move(x, y, z):
            self.buttons[x][y][z].config(bg="#b3e5fc")

    def on_leave(self, x, y, z):
        if self.game.is_valid_move(x, y, z):
            self.buttons[x][y][z].config(bg="white")

    def play_sound(self, filename):
        threading.Thread(target=playsound, args=(filename,), daemon=True).start()

    def play_move_sound(self):
        self.play_sound('move.wav')

    def play_win_sound(self):
        self.play_sound('win.wav')

    def cell_click(self, x, y, z):
        if self.current_player != 1 or not self.game.is_valid_move(x, y, z):
            return
        self.game.make_move(x, y, z, 1)
        self.play_move_sound()
        self.update_board()
        if self.game.check_win(1):
            self.turn_var.set("You win! 🎉")
            self.winning_cells = self.find_winning_cells(1)
            self.highlight_winning_cells()
            self.play_win_sound()
            self.show_3d_win_animation()
            self.play_again_popup("You win! 🎉")
            return
        elif self.game.is_draw():
            self.turn_var.set("Draw! 🤝")
            self.play_win_sound()
            self.play_again_popup("It's a draw!")
            return
        self.current_player = 2
        self.turn_var.set("AI's turn (O)")
        self.root.after(600, self.ai_move)

    def ai_move(self):
        move = self.ai.find_best_move(self.game, self.difficulty_var.get())
        if move:
            self.game.make_move(*move, 2)
            self.play_move_sound()
        self.update_board()
        if self.game.check_win(2):
            self.turn_var.set("AI wins! 🤖")
            self.winning_cells = self.find_winning_cells(2)
            self.highlight_winning_cells()
            self.play_win_sound()
            self.show_3d_win_animation()
            self.play_again_popup("AI wins! 🤖")
        elif self.game.is_draw():
            self.turn_var.set("Draw! 🤝")
            self.play_win_sound()
            self.play_again_popup("It's a draw!")
        else:
            self.current_player = 1
            self.turn_var.set("Your turn (X)")

    def update_board(self):
        board = self.game.get_board()
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    val = board[x][y][z]
                    if val == 1:
                        text = "X"
                        color = PLAYER_COLOR
                    elif val == 2:
                        text = "O"
                        color = AI_COLOR
                    else:
                        text = ""
                        color = "white"
                    self.buttons[x][y][z].config(
                        text=text,
                        fg=color,
                        bg="white" if (x, y, z) not in self.winning_cells else WIN_COLOR,
                        state="normal" if val == 0 else "disabled"
                    )

    def highlight_winning_cells(self):
        self.pulse_step = 0
        self.pulse_winning_cells()

    def pulse_winning_cells(self):
        color_cycle = ["#ffd600", "#fff9c4", "#ffe082", "#ffd600"]
        color = color_cycle[self.pulse_step % len(color_cycle)]
        for x, y, z in self.winning_cells:
            self.buttons[x][y][z].config(bg=color)
        self.pulse_step += 1
        if self.winning_cells:
            self.root.after(200, self.pulse_winning_cells)

    def disable_all(self):
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    self.buttons[x][y][z].config(state="disabled")

    def restart(self):
        self.game.reset()
        self.update_board()
        self.current_player = 1
        self.turn_var.set("Your turn (X)")
        self.winning_cells = []

    def play_again_popup(self, message):
        self.disable_all()
        if messagebox.askyesno("Game Over", f"{message}\n\nDo you want to play again?"):
            self.restart()
        else:
            self.turn_var.set("Game Over - Close window to exit")

    def animate_turn_label(self):
        if self.turn_var.get().startswith("Your turn"):
            self.flash_on = not self.flash_on
            self.turn_label.config(fg="#1a237e" if self.flash_on else "#1976d2")
        elif self.turn_var.get().startswith("AI's turn"):
            self.flash_on = not self.flash_on
            self.turn_label.config(fg="#b71c1c" if self.flash_on else "#e53935")
        else:
            self.turn_label.config(fg="black")
        self.root.after(400, self.animate_turn_label)

    def find_winning_cells(self, player):
        board = self.game.get_board()
        lines = []
        for i in range(4):
            for j in range(4):
                lines.append([(i, j, k) for k in range(4)])
                lines.append([(i, k, j) for k in range(4)])
                lines.append([(k, i, j) for k in range(4)])
        for i in range(4):
            lines.append([(i, k, k) for k in range(4)])
            lines.append([(i, k, 3 - k) for k in range(4)])
            lines.append([(k, i, k) for k in range(4)])
            lines.append([(k, i, 3 - k) for k in range(4)])
            lines.append([(k, k, i) for k in range(4)])
            lines.append([(k, 3 - k, i) for k in range(4)])
        lines.append([(k, k, k) for k in range(4)])
        lines.append([(k, k, 3 - k) for k in range(4)])
        lines.append([(k, 3 - k, k) for k in range(4)])
        lines.append([(3 - k, k, k) for k in range(4)])
        for line in lines:
            if all(board[x][y][z] == player for x, y, z in line):
                return line
        return []

    def show_3d_win_animation(self):
        """Shows a 3D cube animation with the winning line highlighted."""
        if not self.winning_cells:
            return
        board = self.game.get_board()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Plot all pieces
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if board[x][y][z] == 1:
                        ax.scatter(x, y, z, c=PLAYER_COLOR, marker='x', s=120, label='X' if (x, y, z)==self.winning_cells[0] else "")
                    elif board[x][y][z] == 2:
                        ax.scatter(x, y, z, c=AI_COLOR, marker='o', s=120, label='O' if (x, y, z)==self.winning_cells[0] else "")
        # Highlight winning line
        xs, ys, zs = zip(*self.winning_cells)
        ax.plot(xs, ys, zs, color='gold', linewidth=6, alpha=0.6)
        ax.set_title('Winning Line Highlighted!', fontsize=14)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_zticks(range(4))
        ax.view_init(30, 60)
        plt.tight_layout()
        plt.show()

# Main program to start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
