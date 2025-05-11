# src/ai.py
from src.game import InvalidMoveError

class MinimaxAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board, player):
        opponent = 'W' if player == 'B' else 'B'
        score = 0
        size = len(board)
        def line_scores(line):
            s = 0
            for i in range(len(line) - 4):
                window = line[i:i+5]
                if opponent in window and player in window:
                    continue
                cnt_p = window.count(player)
                cnt_o = window.count(opponent)
                if cnt_p and not cnt_o:
                    s += 10 ** cnt_p
                elif cnt_o and not cnt_p:
                    s -= 10 ** cnt_o
            return s
        # rows & cols
        for row in board:
            score += line_scores(row)
        for col in zip(*board):
            score += line_scores(col)
        # diagonals TL-BR & TR-BL
        for r in range(size-4):
            score += line_scores([board[r+i][i] for i in range(size-r)])
            score += line_scores([board[i][r+i] for i in range(size-r)])
            score += line_scores([board[r+i][size-1-i] for i in range(size-r)])
            score += line_scores([board[i][size-1-(r+i)] for i in range(size-r)])
        return score

    def minimax(self, game, depth, maximizing):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.get_active_player()), None
        best_move = None
        player = game.get_active_player()
        if maximizing:
            max_eval = -float('inf')
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x, y)
                            eval_score, _ = self.minimax(clone, depth-1, False)
                        except InvalidMoveError:
                            continue
                        if eval_score > max_eval:
                            max_eval, best_move = eval_score, (x, y)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x, y)
                            eval_score, _ = self.minimax(clone, depth-1, True)
                        except InvalidMoveError:
                            continue
                        if eval_score < min_eval:
                            min_eval, best_move = eval_score, (x, y)
            return min_eval, best_move

    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move

class AlphaBetaAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board, player):
        # same heuristic
        return MinimaxAI(self.depth).evaluate(board, player)

    def alphabeta(self, game, depth, alpha, beta, maximizing):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.get_active_player()), None
        best_move = None
        player = game.get_active_player()
        if maximizing:
            value = -float('inf')
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x, y)
                            eval_score, _ = self.alphabeta(clone, depth-1, alpha, beta, False)
                        except InvalidMoveError:
                            continue
                        if eval_score > value:
                            value, best_move = eval_score, (x, y)
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            return value, best_move
            return value, best_move
        else:
            value = float('inf')
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x, y)
                            eval_score, _ = self.alphabeta(clone, depth-1, alpha, beta, True)
                        except InvalidMoveError:
                            continue
                        if eval_score < value:
                            value, best_move = eval_score, (x, y)
                        beta = min(beta, value)
                        if beta <= alpha:
                            return value, best_move
            return value, best_move

    def get_move(self, game):
        _, move = self.alphabeta(game, self.depth, -float('inf'), float('inf'), True)
        return move