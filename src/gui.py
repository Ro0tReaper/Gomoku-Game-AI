import tkinter as tk
from os import _exit as exit_os
from tkinter import messagebox
from PIL import Image, ImageTk
from src.game import Game
from src.ai import MinimaxAI, AlphaBetaAI


def start_gui():
    root = tk.Tk()
    root.title("Gomoku Game")
    root.geometry("800x600")
    root.resizable(False, False)

    # Load and set background image
    try:
        bg_image = Image.open("assets/image.png").resize((800, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Background image not found: {e}")
        exit_os(1)

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Title
    canvas.create_text(400, 100, text="Gomoku Game", font=("Helvetica", 36, "bold"), fill="white")

    # Human vs AI Mode
    def start_human_vs_ai():
        user_color = messagebox.askquestion("Choose Color", "Do you want to play as Black? (Yes for Black, No for White)")
        user_color = "black" if user_color == "yes" else "white"
        ai_color = "white" if user_color == "black" else "black"
        root.withdraw()  # Hide the main menu
        game_window = tk.Toplevel()
        game_window.title("Gomoku - Human vs AI Mode")
        game_window.geometry("800x600")
        game_window.resizable(False, False)

        # Game setup
        game = Game()
        current_player = user_color
        buttons = []

        def handle_click(x, y, button):
            nonlocal current_player, user_color, ai_color
            if game.make_move(x, y, current_player[0].upper()):
                piece_image = Image.open(f"assets/{user_color}.jpeg").resize((30, 30))
                photo = ImageTk.PhotoImage(piece_image)
                button.config(image=photo, width=30, height=30)
                button.image = photo  # Keep a reference to avoid garbage collection
                current_player = "white" if current_player == "black" else "black"

        # Create 15x15 grid
        for x in range(15):
            row = []
            for y in range(15):
                btn = tk.Button(game_window, width=2, height=1, command=lambda x=x, y=y, b=None: handle_click(x, y, b))
                btn.grid(row=x, column=y, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)

        # Add title label
        title_label = tk.Label(game_window, text="Human vs AI Mode", font=("Helvetica", 24, "bold"))
        title_label.grid(row=15, columnspan=15, pady=20)

        # Exit button
        quit_btn = tk.Button(game_window, text="Quit to Menu", font=("Helvetica", 14), command=lambda: (game_window.destroy(), root.deiconify()))
        quit_btn.grid(row=16, columnspan=15, pady=10)

        game_window.mainloop()


    # AI vs AI Mode
    def start_ai_vs_ai():
        root.withdraw()  # Hide the main menu
        game_window = tk.Toplevel()
        game_window.title("Gomoku - AI vs AI Mode")
        game_window.geometry("800x600")
        game_window.resizable(False, False)

        # Create 15x15 grid
        for x in range(15):
            for y in range(15):
                lbl = tk.Label(game_window, width=2, height=1, bg="lightgrey", relief="solid")
                lbl.grid(row=x, column=y, padx=1, pady=1)

        # Add title label
        title_label = tk.Label(game_window, text="AI vs AI Mode", font=("Helvetica", 24, "bold"))
        title_label.grid(row=15, columnspan=15, pady=20)

        # Exit button
        quit_btn = tk.Button(game_window, text="Quit to Menu", font=("Helvetica", 14), command=lambda: (game_window.destroy(), root.deiconify()))
        quit_btn.grid(row=16, columnspan=15, pady=10)

        game_window.mainloop()


    # Main Menu Buttons
    human_vs_ai_btn = tk.Button(root, text="Human vs AI", font=("Helvetica", 16), width=20, command=start_human_vs_ai)
    ai_vs_ai_btn = tk.Button(root, text="AI vs AI", font=("Helvetica", 16), width=20, command=start_ai_vs_ai)
    exit_btn = tk.Button(root, text="Quit", font=("Helvetica", 16), width=20, command=lambda: (messagebox.showinfo("Quitting", "Cya ;D"), exit_os(0)))

    canvas.create_window(400, 250, window=human_vs_ai_btn)
    canvas.create_window(400, 320, window=ai_vs_ai_btn)
    canvas.create_window(400, 400, window=exit_btn)

    root.mainloop()
