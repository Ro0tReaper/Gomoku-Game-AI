class Game:
    def __init__(self, size=15):
        self.grid_size = size
        self.game_grid = [[None for _ in range(size)] for _ in range(size)]
        self.active_player = 'B'
        self.terminated = False
        self.victor = None
        self.history = []

    def restart(self):
        self.game_grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.active_player = 'B'
        self.terminated = False
        self.victor = None
        self.history = []

    def place_stone(self, x, y):
        if self.terminated or not self._validate_position(x, y):
            return False

        self.game_grid[x][y] = self.active_player
        self.history.append((x, y, self.active_player))
        
        if self._detect_victory(x, y):
            self.terminated = True
            self.victor = self.active_player
        elif self._check_grid_completion():
            self.terminated = True
        else:
            self._alternate_turn()
        
        return True

    def _validate_position(self, x, y):
        return (0 <= x < self.grid_size and 
                0 <= y < self.grid_size and 
                self.game_grid[x][y] is None)

    def _alternate_turn(self):
        self.active_player = 'W' if self.active_player == 'B' else 'B'

    def _detect_victory(self, x, y):
        scan_vectors = [(0, 1), (1, 0), (1, 1), (1, -1)]
        stone_color = self.game_grid[x][y]
        
        for dx, dy in scan_vectors:
            connected = 1
            
            nx, ny = x + dx, y + dy
            while (0 <= nx < self.grid_size and 
                   0 <= ny < self.grid_size and 
                   self.game_grid[nx][ny] == stone_color):
                connected += 1
                nx += dx
                ny += dy
            
            nx, ny = x - dx, y - dy
            while (0 <= nx < self.grid_size and 
                   0 <= ny < self.grid_size and 
                   self.game_grid[nx][ny] == stone_color):
                connected += 1
                nx -= dx
                ny -= dy
            
            if connected >= 5:
                return True
        
        return False

    def _check_grid_completion(self):
        for row in self.game_grid:
            if None in row:
                return False
        return True

    def current_configuration(self):
        return [row[:] for row in self.game_grid]

    def available_positions(self):
        positions = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.game_grid[x][y] is None:
                    positions.append((x, y))
        return positions

    def show_grid(self):
        print("  " + " ".join(str(i).rjust(2) for i in range(self.grid_size)))
        for idx, row in enumerate(self.game_grid):
            print(str(idx).rjust(2) + " " + " ".join('.' if cell is None else cell for cell in row))
