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
        root.withdraw()  # Hide the main menu
        game_window = tk.Toplevel()
        game_window.title("Gomoku - Human vs AI Mode")
        game_window.geometry("800x600")
        game_window.resizable(False, False)

        # Ask the player to choose a color
        user_color = messagebox.askquestion("Choose Color", "Do you want to play as Black? (Yes for Black, No for White)")
        user_color = "black" if user_color == "yes" else "white"
        piece_image = ImageTk.PhotoImage(Image.open(f"assets/{user_color}.jpeg").resize((30, 30)))

        # Load background image
        try:
            bg_image = Image.open("assets/humanvsai.jpeg").resize((800, 600))
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(game_window, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = bg_photo  # Prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Background image not found: {e}")
            exit_os(1)

        # Add centered title
        title_label = tk.Label(game_window, text="Human vs AI Mode", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create grid
        grid_frame = tk.Frame(game_window, bg="black")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        for x in range(15):
            for y in range(15):
                btn = tk.Button(grid_frame, width=2, height=1)

                # Set the click behavior to set the player piece
                def on_click(btn: tk.Button = btn):
                 
                    btn.config(image=piece_image, width=20, height=20)
                    btn.image = piece_image  # Keep a reference to avoid garbage collection

                btn.config(command=on_click)
                btn.grid(row=x, column=y, padx=2, pady=2)

        # Exit button
        quit_btn = tk.Button(game_window, text="Quit to Menu", font=("Helvetica", 14), command=lambda: (game_window.destroy(), root.deiconify()))
        quit_btn.place(relx=0.5, rely=0.9, anchor="center")

        game_window.mainloop()

        root.withdraw()  # Hide the main menu
        game_window = tk.Toplevel()
        game_window.title("Gomoku - Human vs AI Mode")
        game_window.geometry("800x600")
        game_window.resizable(False, False)

        # Load background image
        try:
            bg_image = Image.open("assets/humanvsai.jpeg").resize((800, 600))
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(game_window, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = bg_photo  # Prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Background image not found: {e}")
            exit_os(1)

        # Add centered title
        title_label = tk.Label(game_window, text="Human vs AI Mode", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create grid
        grid_frame = tk.Frame(game_window, bg="black")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        for x in range(15):
            for y in range(15):
                btn = tk.Button(grid_frame, width=2, height=1)
                btn.grid(row=x, column=y, padx=2, pady=2)

        # Exit button
        quit_btn = tk.Button(game_window, text="Quit to Menu", font=("Helvetica", 14), command=lambda: (game_window.destroy(), root.deiconify()))
        quit_btn.place(relx=0.5, rely=0.9, anchor="center")

        game_window.mainloop()


    # AI vs AI Mode
    def start_ai_vs_ai():
        root.withdraw()  # Hide the main menu
        game_window = tk.Toplevel()
        game_window.title("Gomoku - AI vs AI Mode")
        game_window.geometry("800x600")
        game_window.resizable(False, False)

        # Load background image
        try:
            bg_image = Image.open("assets/aivsai.jpg").resize((800, 600))
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(game_window, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = bg_photo  # Prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Background image not found: {e}")
            exit_os(1)

        # Add centered title
        title_label = tk.Label(game_window, text="AI vs AI Mode", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create grid
        grid_frame = tk.Frame(game_window, bg="black")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        for x in range(15):
            for y in range(15):
                lbl = tk.Label(grid_frame, width=2, height=1, bg="lightgrey", relief="solid")
                lbl.grid(row=x, column=y, padx=2, pady=2)

        # Exit button
        quit_btn = tk.Button(game_window, text="Quit to Menu", font=("Helvetica", 14), command=lambda: (game_window.destroy(), root.deiconify()))
        quit_btn.place(relx=0.5, rely=0.9, anchor="center")

        game_window.mainloop()


    # Main Menu Buttons
    human_vs_ai_btn = tk.Button(root, text="Human vs AI", font=("Helvetica", 16), width=20, command=start_human_vs_ai)
    ai_vs_ai_btn = tk.Button(root, text="AI vs AI", font=("Helvetica", 16), width=20, command=start_ai_vs_ai)
    exit_btn = tk.Button(root, text="Quit", font=("Helvetica", 16), width=20, command=lambda: (messagebox.showinfo("Quitting", "Cya ;D"), exit_os(0)))

    canvas.create_window(400, 250, window=human_vs_ai_btn)
    canvas.create_window(400, 320, window=ai_vs_ai_btn)
    canvas.create_window(400, 400, window=exit_btn)

    root.mainloop()
