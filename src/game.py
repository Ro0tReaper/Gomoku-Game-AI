class GomokuGame:
    def __init__(self, size=15):
        self.grid_size = size
        self.game_grid = [[None for _ in range(size)] for _ in range(size)]
        self.active_player = 'B'  # Black always starts
        self.terminated = False
        self.victor = None
        self.history = []
        self.move_count = 0  # Track move count for special opening rules

    def place_stone(self, x, y):
        """Process a move with full validation"""
        # Check game state
        if self.terminated:
            raise GameOverError("Game has already ended")
        
        # Validate coordinates
        try:
            x, y = int(x), int(y)
        except (ValueError, TypeError):
            raise InvalidMoveError("Coordinates must be integers")
            
        if not self._validate_position(x, y):
            raise InvalidMoveError("Invalid position")
            
        # Apply opening rules (example: first move must be center)
        if self.move_count == 0 and (x != self.grid_size//2 or y != self.grid_size//2):
            raise InvalidMoveError("First move must be center point")
            
        # Check for overline (6+ stones) if playing with that rule
        if self._would_create_overline(x, y):
            raise InvalidMoveError("Move creates forbidden overline")
            
        # Place the stone
        self.game_grid[x][y] = self.active_player
        self.history.append((x, y, self.active_player))
        self.move_count += 1
        
        # Check game state
        if self._detect_victory(x, y):
            self.terminated = True
            self.victor = self.active_player
        elif self._check_grid_completion():
            self.terminated = True
        else:
            self._alternate_turn()
            
        return True

    def _would_create_overline(self, x, y):
        """Check if move would create 6+ in a row (forbidden in some variants)"""
        temp_player = self.active_player
        self.game_grid[x][y] = temp_player  # Temporarily place
        
        scan_vectors = [(0, 1), (1, 0), (1, 1), (1, -1)]
        overline = False
        
        for dx, dy in scan_vectors:
            count = 1
            # Check in positive direction
            nx, ny = x + dx, y + dy
            while (0 <= nx < self.grid_size and 
                   0 <= ny < self.grid_size and 
                   self.game_grid[nx][ny] == temp_player):
                count += 1
                nx += dx
                ny += dy
            # Check in negative direction
            nx, ny = x - dx, y - dy
            while (0 <= nx < self.grid_size and 
                   0 <= ny < self.grid_size and 
                   self.game_grid[nx][ny] == temp_player):
                count += 1
                nx -= dx
                ny -= dy
                
            if count > 5:
                overline = True
                break
                
        self.game_grid[x][y] = None  # Remove temporary placement
        return overline

    # ... (keep your existing methods but add input validation)

class InvalidMoveError(Exception):
    pass

class GameOverError(Exception):
    pass
