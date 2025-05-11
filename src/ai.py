# src/ai.py
from src.game import InvalidMoveError

class MinimaxAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board, player):
        opp = 'W' if player=='B' else 'B'
        size = len(board)
        score = 0
        def scan(lines):
            s=0
            for i in range(len(lines)-4):
                w = lines[i:i+5]
                if opp in w and player in w: continue
                cp = w.count(player); co = w.count(opp)
                if cp>0 and co==0: s += 10**cp
                if co>0 and cp==0: s -= 10**co
            return s
        for r in board: score += scan(r)
        for c in zip(*board): score += scan(c)
        for k in range(-size+5, size-4):
            diag1 = [board[i][i-k] for i in range(size) if 0<=i-k<size]
            diag2 = [board[i][size-1-(i-k)] for i in range(size) if 0<=i-k<size]
            score += scan(diag1)+scan(diag2)
        return score

    def minimax(self, game, depth, maximizing):
        if depth==0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.active_player), None
        best = None
        if maximizing:
            v = -1e9
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = game.active_player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x,y)
                            ev,_ = self.minimax(clone, depth-1, False)
                        except InvalidMoveError:
                            continue
                        if ev>v: v, best = ev, (x,y)
            return v, best
        else:
            v = 1e9
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y] is None:
                        try:
                            clone = type(game)(game.grid_size)
                            clone.game_grid = [row[:] for row in game.game_grid]
                            clone.active_player = game.active_player
                            clone.move_count = game.move_count
                            clone.history = game.history[:]
                            clone.place_stone(x,y)
                            ev,_ = self.minimax(clone, depth-1, True)
                        except InvalidMoveError:
                            continue
                        if ev<v: v, best = ev, (x,y)
            return v, best

    def get_move(self, game):
        _,m = self.minimax(game, self.depth, True)
        return m

class AlphaBetaAI(MinimaxAI):
    def minimax(self, game, depth, maximizing, alpha=-1e9, beta=1e9):
        if depth==0 or game.is_game_over():
            return self.evaluate(game.get_grid(), game.active_player), None
        best=None
        if maximizing:
            v=-1e9
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y]==None:
                        try:
                            clone=type(game)(game.grid_size)
                            clone.game_grid=[r[:] for r in game.game_grid]
                            clone.active_player=game.active_player
                            clone.move_count=game.move_count
                            clone.history=game.history[:]
                            clone.place_stone(x,y)
                            ev,_=self.minimax(clone, depth-1, False, alpha, beta)
                        except InvalidMoveError: continue
                        if ev>v: v,best=ev,(x,y)
                        alpha=max(alpha, ev)
                        if beta<=alpha: return v,best
            return v,best
        else:
            v=1e9
            for x in range(game.grid_size):
                for y in range(game.grid_size):
                    if game.game_grid[x][y]==None:
                        try:
                            clone=type(game)(game.grid_size)
                            clone.game_grid=[r[:] for r in game.game_grid]
                            clone.active_player=game.active_player
                            clone.move_count=game.move_count
                            clone.history=game.history[:]
                            clone.place_stone(x,y)
                            ev,_=self.minimax(clone, depth-1, True, alpha, beta)
                        except InvalidMoveError: continue
                        if ev<v: v,best=ev,(x,y)
                        beta=min(beta, ev)
                        if beta<=alpha: return v,best
            return v,best