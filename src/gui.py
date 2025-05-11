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

    # Buttons
    def start_human_vs_ai():
        messagebox.showinfo("Mode Selected", "Human vs AI mode selected.")
        print(f"Mode: {start_human_vs_ai.__name__}")

    def start_ai_vs_ai():
        messagebox.showinfo("Mode Selected", "AI vs AI mode selected.")
        print(f"Mode: {start_ai_vs_ai.__name__}")

    def quit():
        messagebox.showinfo("Qutting", "Cya ;D")
        print("Byee~")
        exit_os(0)


    human_vs_ai_btn = tk.Button(root, text="Human vs AI", font=("Helvetica", 16), width=20, command=start_human_vs_ai)
    ai_vs_ai_btn = tk.Button(root, text="AI vs AI", font=("Helvetica", 16), width=20, command=start_ai_vs_ai)
    exit_btn = tk.Button(root, text="Quit", font=("Helvetica", 16), width=20, command=quit)

    canvas.create_window(400, 250, window=human_vs_ai_btn)
    canvas.create_window(400, 320, window=ai_vs_ai_btn)
    canvas.create_window(400, 400, window=exit_btn)

    root.mainloop()
