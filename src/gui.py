# src/gui.py

import tkinter as tk
from src.game import Game
from src.ai import MinimaxAI
from src.ai import AlphaBetaAI


def start_gui():
    root = tk.Tk()
    root.title("Gomoku - AI vs AI")
    game = Game()
    ai1 = MinimaxAI()
    ai2 = AlphaBetaAI()
    current_ai = ai1
    buttons = []

    def update_board():
        for x in range(game.size):
            for y in range(game.size):
                buttons[x][y].config(text=game.board[x][y])
        winner = game.check_winner()
        if winner:
            result_label.config(text=f"{winner} wins!")

    for x in range(game.size):
        row = []
        for y in range(game.size):
            btn = tk.Button(root, text='.', width=2, height=1)
            btn.grid(row=x, column=y)
            row.append(btn)
        buttons.append(row)

    result_label = tk.Label(root, text="")
    result_label.grid(row=game.size, columnspan=game.size)

    def ai_vs_ai():
        nonlocal current_ai
        if not game.is_game_over():
            ai_move = current_ai.get_best_move(game)
            symbol = 'X' if current_ai == ai1 else 'O'
            game.make_move(ai_move[0], ai_move[1], symbol)
            update_board()
            current_ai = ai2 if current_ai == ai1 else ai1
            root.after(500, ai_vs_ai)  # Delay for better visualization

    # Start the AI vs AI loop
    ai_vs_ai()
    root.mainloop()