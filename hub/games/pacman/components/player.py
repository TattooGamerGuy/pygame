"""Player component for Pac-Man."""

from typing import List, Tuple
import pygame
from hub.games.pacman.constants import (
    MAZE_X, MAZE_Y, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT,
    PLAYER_SPEED, POWER_MODE_DURATION
)


class Player:
    """Pac-Man player component."""
    
    def __init__(self, grid_x: int, grid_y: int):
        """
        Initialize player.
        
        Args:
            grid_x: Starting grid X position
            grid_y: Starting grid Y position
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = MAZE_X + grid_x * CELL_SIZE
        self.pixel_y = MAZE_Y + grid_y * CELL_SIZE
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = PLAYER_SPEED
        self.power_mode = False
        self.power_timer = 0.0
    
    def update(self, maze: List[List[int]]) -> None:
        """Update player position."""
        # Try to change direction
        if self.can_move(maze, self.next_direction):
            self.direction = self.next_direction
        
        # Move in current direction
        if self.can_move(maze, self.direction):
            move_x = self.direction[0] * self.speed
            move_y = self.direction[1] * self.speed
            self.pixel_x += move_x
            self.pixel_y += move_y
            
            # Update grid position
            new_grid_x = int((self.pixel_x - MAZE_X) // CELL_SIZE)
            new_grid_y = int((self.pixel_y - MAZE_Y) // CELL_SIZE)
            
            if new_grid_x != self.grid_x or new_grid_y != self.grid_y:
                self.grid_x = new_grid_x
                self.grid_y = new_grid_y
                # Wrap around (tunnel)
                if self.grid_x < 0:
                    self.grid_x = MAZE_WIDTH - 1
                    self.pixel_x = MAZE_X + self.grid_x * CELL_SIZE
                elif self.grid_x >= MAZE_WIDTH:
                    self.grid_x = 0
                    self.pixel_x = MAZE_X + self.grid_x * CELL_SIZE
        else:
            # Snap to grid
            target_x = MAZE_X + self.grid_x * CELL_SIZE
            target_y = MAZE_Y + self.grid_y * CELL_SIZE
            if abs(self.pixel_x - target_x) < self.speed:
                self.pixel_x = target_x
            else:
                self.pixel_x += self.speed if self.pixel_x < target_x else -self.speed
            
            if abs(self.pixel_y - target_y) < self.speed:
                self.pixel_y = target_y
            else:
                self.pixel_y += self.speed if self.pixel_y < target_y else -self.speed
        
        # Update power mode
        if self.power_mode:
            self.power_timer -= 0.016  # ~60fps
            if self.power_timer <= 0:
                self.power_mode = False
    
    def can_move(self, maze: List[List[int]], direction: Tuple[int, int]) -> bool:
        """Check if player can move in direction."""
        next_x = self.grid_x + direction[0]
        next_y = self.grid_y + direction[1]
        
        # Wrap around
        if next_x < 0:
            next_x = MAZE_WIDTH - 1
        elif next_x >= MAZE_WIDTH:
            next_x = 0
        
        if 0 <= next_y < MAZE_HEIGHT and 0 <= next_x < MAZE_WIDTH:
            return maze[next_y][next_x] != 1
        return False
    
    def set_direction(self, direction: Tuple[int, int]) -> None:
        """Set next direction."""
        self.next_direction = direction
    
    def activate_power_mode(self, duration: float = POWER_MODE_DURATION) -> None:
        """Activate power mode."""
        self.power_mode = True
        self.power_timer = duration

