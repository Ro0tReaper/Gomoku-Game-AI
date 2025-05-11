# src/gui.py
import tkinter as tk
from os import _exit as exit_os
from tkinter import messagebox
from PIL import Image, ImageTk
from src.game import Game
from src.ai import MinimaxAI, AlphaBetaAI

BOARD_SIZE = 15

# === Main Menu and Mode Launchers ===
def start_gui():
    global root
    root = tk.Tk()
    root.title("Gomoku Game")
    root.geometry("800x600")
    root.resizable(False, False)

    # Background
    try:
        bg_image = Image.open("assets/image.png").resize((800,600))
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Background image not found: {e}")
        exit_os(1)

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Title
    canvas.create_text(400, 100, text="Gomoku Game", font=("Helvetica",36,"bold"), fill="white")

    # Buttons
    human_btn = tk.Button(root, text="Human vs AI", font=("Helvetica",16), width=20, command=start_human_vs_ai)
    ai_btn    = tk.Button(root, text="AI vs AI", font=("Helvetica",16), width=20, command=start_ai_vs_ai)
    exit_btn  = tk.Button(root, text="Quit", font=("Helvetica",16), width=20,
                          command=lambda: (messagebox.showinfo("Quitting","Bye!"), exit_os(0)))
    canvas.create_window(400, 250, window=human_btn)
    canvas.create_window(400, 320, window=ai_btn)
    canvas.create_window(400, 400, window=exit_btn)

    root.mainloop()

# === Human vs AI ===
def start_human_vs_ai():
    root.withdraw()
    game = Game(size=BOARD_SIZE)
    ai = AlphaBetaAI(depth=2)

    win = tk.Toplevel()
    win.title("Gomoku - Human vs AI Mode")
    win.geometry("800x600")
    win.resizable(False, False)

    # Choose color
    ans = messagebox.askquestion("Choose Color", "Play as Black? (Yes=Black, No=White)")
    human = 'B' if ans=='yes' else 'W'
    human_img = ImageTk.PhotoImage(
        Image.open(f"assets/{'black' if human=='B' else 'white'}.jpeg").resize((20,20))
    )
    ai_player = 'W' if human=='B' else 'B'
    ai_img = ImageTk.PhotoImage(
        Image.open(f"assets/{'black' if ai_player=='B' else 'white'}.jpeg").resize((20,20))
    )

    # Background
    try:
        bg = ImageTk.PhotoImage(Image.open("assets/humanvsai.jpeg").resize((800,600)))
        lbl = tk.Label(win, image=bg)
        lbl.image = bg
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("Error", str(e)); exit_os(1)

    tk.Label(win, text="Human vs AI Mode", font=("Helvetica",24,"bold"), fg="white", bg="black").place(
        relx=0.5, rely=0.05, anchor="center")

    frame = tk.Frame(win, bg="black")
    frame.place(relx=0.5, rely=0.55, anchor="center")

    buttons = {}
    def click(x,y):
        if game.is_game_over(): return
        try:
            game.place_stone(x,y)
            btn = buttons[(x,y)]; btn.config(image=human_img); btn.image=human_img
            print("Human:", (x,y))
            if game.is_game_over():
                messagebox.showinfo("Game Over","Human wins!"); return
            mv = ai.get_move(game)
            if mv:
                game.place_stone(*mv)
                btn2 = buttons[mv]; btn2.config(image=ai_img); btn2.image=ai_img
                print("AI:", mv)
                if game.is_game_over():
                    messagebox.showinfo("Game Over","AI wins!")
        except Exception as e:
            messagebox.showwarning("Invalid Move", str(e))

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            b = tk.Button(frame, width=2, height=1, command=lambda x=i, y=j: click(x,y))
            b.grid(row=i, column=j, padx=2, pady=2)
            buttons[(i,j)] = b

    tk.Button(win, text="Quit to Menu", font=("Helvetica",14),
              command=lambda: (win.destroy(), root.deiconify())).place(
        relx=0.5, rely=0.9, anchor="center")
    win.mainloop()

# === AI vs AI (stub) ===
def start_ai_vs_ai():
    root.withdraw()
    game = Game(size=BOARD_SIZE)
    # You can implement this later
    messagebox.showinfo("Coming Soon","AI vs AI mode is under construction.")
    root.deiconify()

if __name__ == '__main__':
    start_gui()