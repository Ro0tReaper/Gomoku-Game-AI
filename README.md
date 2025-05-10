# Gomoku (Five in a Row) Game Solver

This repository contains a fully functional **Gomoku (Five in a Row) Game Solver**, developed as part of an AI project for Spring 2025. The game includes user-vs-AI and AI-vs-AI modes, utilizing algorithms like **Minimax** and **Alpha-Beta Pruning** for optimal gameplay.

## 📋 Project Overview

Gomoku, also known as **Five in a Row**, is a strategy board game where the goal is to place five of your pieces in a horizontal, vertical, or diagonal line. This project aims to simulate the game using efficient AI techniques to evaluate the best possible moves.

### Features

* **Interactive Game Board**: Play on a customizable grid (15x15 or 19x19).
* **AI Algorithms**: Includes both Minimax and Alpha-Beta Pruning.
* **User vs AI** and **AI vs AI** modes.
* **Formatted Move Output** for easy debugging.
* Optional **Graphical User Interface (GUI)** for a more engaging experience.

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Basic command-line knowledge

### Installation

Clone the repository:

```bash
$ git clone https://github.com/your-username/gomoku-game-solver.git
$ cd gomoku-game-solver
```

Install required packages:

```bash
$ pip install -r requirements.txt
```

### Run the Game

To start the game:

```bash
$ python gomoku.py
```

## 🧠 How It Works

The game uses the following components:

* **Game State Representation**: Handles board creation and state management.
* **Move Generation**: Validates player moves and checks for game-ending conditions.
* **Minimax Algorithm**: AI algorithm for decision making.
* **Alpha-Beta Pruning**: Optimization to speed up AI move calculations.

## 📂 Project Structure

```
📦gomoku-game-solver
 ┣ 📂src
 ┃ ┣ 📜game.py
 ┃ ┣ 📜ai.py
 ┃ ┗ 📜gui.py (optional)
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜LICENSE
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for major changes.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Contact

For any inquiries, please reach out to **Your Name** at [youremail@example.com](mailto:youremail@example.com).

## ⭐ Acknowledgments

Special thanks to the AI course instructors for their guidance and support.

---

Happy Coding! 🚀
