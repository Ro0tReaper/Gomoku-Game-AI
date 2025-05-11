# src/game.py
class InvalidMoveError(Exception):
    pass

class GameOverError(Exception):
    pass

class Game:
    def __init__(self, size=15):
        self.grid_size = size
        self.game_grid = [[None]*size for _ in range(size)]
        self.active_player = 'B'
        self.terminated = False
        self.victor = None
        self.history = []
        self.move_count = 0

    def place_stone(self, x, y):
        if self.terminated:
            raise GameOverError("Game has already ended")
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            raise InvalidMoveError("Out of bounds")
        if self.game_grid[x][y] is not None:
            raise InvalidMoveError("Cell occupied")

        # first-move rule
        if self.move_count == 0:
            center = self.grid_size // 2
            if (x, y) != (center, center):
                raise InvalidMoveError("First move must be center")

        # no overline
        if self._would_create_overline(x, y):
            raise InvalidMoveError("Forbidden overline")

        self.game_grid[x][y] = self.active_player
        self.history.append((x, y, self.active_player))
        self.move_count += 1

        if self._detect_victory(x, y):
            self.terminated = True
            self.victor = self.active_player
        elif self._check_full():
            self.terminated = True
        else:
            self.active_player = 'W' if self.active_player=='B' else 'B'
        return True

    def _detect_victory(self, x, y):
        dirs = [(1,0),(0,1),(1,1),(1,-1)]
        p = self.game_grid[x][y]
        for dx, dy in dirs:
            cnt = 1
            for s in (1,-1):
                nx, ny = x+dx*s, y+dy*s
                while 0<=nx<self.grid_size and 0<=ny<self.grid_size and self.game_grid[nx][ny]==p:
                    cnt +=1; nx+=dx*s; ny+=dy*s
            if cnt>=5:
                return True
        return False

    def _would_create_overline(self, x, y):
        p = self.active_player
        self.game_grid[x][y] = p
        over = False
        dirs = [(1,0),(0,1),(1,1),(1,-1)]
        for dx, dy in dirs:
            cnt = 1
            for s in (1,-1):
                nx, ny = x+dx*s, y+dy*s
                while 0<=nx<self.grid_size and 0<=ny<self.grid_size and self.game_grid[nx][ny]==p:
                    cnt +=1; nx+=dx*s; ny+=dy*s
            if cnt>5:
                over = True; break
        self.game_grid[x][y] = None
        return over

    def _check_full(self):
        return all(cell is not None for row in self.game_grid for cell in row)

    def is_game_over(self):
        return self.terminated

    def get_winner(self):
        return self.victor

    def get_grid(self):
        from copy import deepcopy
        return deepcopy(self.game_grid)