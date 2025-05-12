# src/ai.py
from src.game import InvalidMoveError

class MinimaxAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board, player):
        opp = 'W' if player == 'B' else 'B'
        size = len(board)
        score = 0
        def scan(lines):
            s = 0
            for i in range(len(lines) - 4):
                w = lines[i:i+5]
                if opp in w and player in w:
                    continue
                cp = w.count(player)
                co = w.count(opp)
                if cp > 0 and co == 0:
                    s += 10 ** cp
                if co > 0 and cp == 0:
                    s -= 10 ** co
            return s

        for r in board:
            score += scan(r)
        for c in zip(*board):
            score += scan(c)
        for k in range(-size + 5, size -4):
            diag1 = [board[i][i-k] for i in range(size) if 0 <= i-k < size]
            diag2 = [board[i][size-1-(i-k)] for i in range(size) if 0 <= i-k < size]
            score += scan(diag1) + scan(diag2)
        return score

    def get_candidate_moves(self, game):
        radius = 2
        moves = set()
        if not game.history:
            center = game.grid_size // 2
            return [(center, center)]
        for x, y, _ in game.history:
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < game.grid_size and 0 <= ny < game.grid_size:
                        if game.game_grid[nx][ny] is None:
                            moves.add((nx, ny))
        return list(moves)

    def minimax(self, game, depth, maximizing):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.active_player), None
        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for x, y in self.get_candidate_moves(game):
                try:
                    clone = type(game)(game.grid_size)
                    clone.game_grid = [row[:] for row in game.game_grid]
                    clone.active_player = game.active_player
                    clone.move_count = game.move_count
                    clone.history = game.history[:]
                    clone.place_stone(x, y)
                    eval_score, _ = self.minimax(clone, depth - 1, False)
                except InvalidMoveError:
                    continue
                if eval_score > max_eval:
                    max_eval, best_move = eval_score, (x, y)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for x, y in self.get_candidate_moves(game):
                try:
                    clone = type(game)(game.grid_size)
                    clone.game_grid = [row[:] for row in game.game_grid]
                    clone.active_player = game.active_player
                    clone.move_count = game.move_count
                    clone.history = game.history[:]
                    clone.place_stone(x, y)
                    eval_score, _ = self.minimax(clone, depth - 1, True)
                except InvalidMoveError:
                    continue
                if eval_score < min_eval:
                    min_eval, best_move = eval_score, (x, y)
            return min_eval, best_move

    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move

class AlphaBetaAI(MinimaxAI):
    def minimax(self, game, depth, maximizing, alpha=-float('inf'), beta=float('inf')):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.active_player), None
        best_move = None
        if maximizing:
            value = -float('inf')
            for x, y in self.get_candidate_moves(game):
                try:
                    clone = type(game)(game.grid_size)
                    clone.game_grid = [row[:] for row in game.game_grid]
                    clone.active_player = game.active_player
                    clone.move_count = game.move_count
                    clone.history = game.history[:]
                    clone.place_stone(x, y)
                    eval_score, _ = self.minimax(clone, depth - 1, False, alpha, beta)
                except InvalidMoveError:
                    continue
                if eval_score > value:
                    value, best_move = eval_score, (x, y)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = float('inf')
            for x, y in self.get_candidate_moves(game):
                try:
                    clone = type(game)(game.grid_size)
                    clone.game_grid = [row[:] for row in game.game_grid]
                    clone.active_player = game.active_player
                    clone.move_count = game.move_count
                    clone.history = game.history[:]
                    clone.place_stone(x, y)
                    eval_score, _ = self.minimax(clone, depth - 1, True, alpha, beta)
                except InvalidMoveError:
                    continue
                if eval_score < value:
                    value, best_move = eval_score, (x, y)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_move

    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move