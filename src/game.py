import copy

class Game:
    def __init__(self, size=15):
        self.grid_size = size
        self.game_grid = [[None for _ in range(size)] for _ in range(size)]
        self.active_player = 'B'  # Black always starts
        self.terminated = False
        self.victor = None
        self.history = []
        self.move_count = 0

    def place_stone(self, x, y):
        if self.terminated:
            raise GameOverError("Game has already ended")
        x, y = int(x), int(y)
        if not self._validate_position(x, y):
            raise InvalidMoveError("Invalid position or already occupied")
        # first move must be center
        if self.move_count == 0 and (x != self.grid_size // 2 or y != self.grid_size // 2):
            raise InvalidMoveError("First move must be center")
        # no overline rule
        if self._would_create_overline(x, y):
            raise InvalidMoveError("Forbidden overline")
        self.game_grid[x][y] = self.active_player
        self.history.append((x, y, self.active_player))
        self.move_count += 1
        if self._detect_victory(x, y):
            self.terminated = True
            self.victor = self.active_player
        elif self._check_grid_completion():
            self.terminated = True
        else:
            self._switch_turn()
        return True

    def ai_move(self, x, y):
        # same validation for AI
        return self.place_stone(x, y)

    def _validate_position(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size and self.game_grid[x][y] is None

    def _detect_victory(self, x, y):
        # unchanged
        player = self.active_player
        dirs = [(0,1),(1,0),(1,1),(1,-1)]
        for dx, dy in dirs:
            cnt = 1
            for sign in (1, -1):
                nx, ny = x + dx*sign, y + dy*sign
                while 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.game_grid[nx][ny] == player:
                    cnt += 1
                    nx += dx*sign
                    ny += dy*sign
            if cnt >= 5:
                return True
        return False

    def _would_create_overline(self, x, y):
        # unchanged
        self.game_grid[x][y] = self.active_player
        dirs = [(0,1),(1,0),(1,1),(1,-1)]
        overline = False
        for dx, dy in dirs:
            cnt = 1
            for sign in (1, -1):
                nx, ny = x + dx*sign, y + dy*sign
                while 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.game_grid[nx][ny] == self.active_player:
                    cnt += 1
                    nx += dx*sign
                    ny += dy*sign
            if cnt > 5:
                overline = True
                break
        self.game_grid[x][y] = None
        return overline

    def _check_grid_completion(self):
        return all(cell is not None for row in self.game_grid for cell in row)

    def _switch_turn(self):
        self.active_player = 'W' if self.active_player == 'B' else 'B'

    def get_active_player(self):
        return self.active_player

    def is_game_over(self):
        return self.terminated

    def get_winner(self):
        return self.victor

    def get_grid(self):
        # return a copy to prevent external mutation
        return copy.deepcopy(self.game_grid)

class InvalidMoveError(Exception):
    pass

class GameOverError(Exception):
    pass