"""Ghost component for Pac-Man."""

from typing import List, Tuple
from hub.games.pacman.components.player import Player
from hub.games.pacman.constants import (
    MAZE_X, MAZE_Y, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, GHOST_SPEED
)


class Ghost:
    """Ghost enemy component."""
    
    def __init__(self, grid_x: int, grid_y: int, color: Tuple[int, int, int]):
        """
        Initialize ghost.
        
        Args:
            grid_x: Starting grid X position
            grid_y: Starting grid Y position
            color: Ghost color (RGB tuple)
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = MAZE_X + grid_x * CELL_SIZE
        self.pixel_y = MAZE_Y + grid_y * CELL_SIZE
        self.color = color
        self.direction = (0, 0)
        self.speed = GHOST_SPEED
    
    def update(self, maze: List[List[int]], player: Player) -> None:
        """Update ghost position with simple AI."""
        # Simple AI: move towards player
        dx = player.grid_x - self.grid_x
        dy = player.grid_y - self.grid_y
        
        # Choose direction
        if abs(dx) > abs(dy):
            self.direction = (1 if dx > 0 else -1, 0)
        else:
            self.direction = (0, 1 if dy > 0 else -1)
        
        # Check if direction is valid
        next_x = self.grid_x + self.direction[0]
        next_y = self.grid_y + self.direction[1]
        
        if (0 <= next_y < MAZE_HEIGHT and 0 <= next_x < MAZE_WIDTH and 
            maze[next_y][next_x] != 1):
            self.grid_x = next_x
            self.grid_y = next_y
            self.pixel_x = MAZE_X + self.grid_x * CELL_SIZE
            self.pixel_y = MAZE_Y + self.grid_y * CELL_SIZE
    
    def reset_position(self, grid_x: int, grid_y: int) -> None:
        """Reset ghost to position."""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = MAZE_X + self.grid_x * CELL_SIZE
        self.pixel_y = MAZE_Y + self.grid_y * CELL_SIZE

