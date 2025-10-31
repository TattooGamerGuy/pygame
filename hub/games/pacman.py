"""Pac-Man game implementation."""

from typing import List, Tuple, Optional
import pygame
from hub.games.base_game import BaseGame
from hub.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW, BLUE, RED, GRID_SIZE


# Simple maze layout (1 = wall, 0 = path, 2 = dot, 3 = power pellet)
MAZE_LAYOUT = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAZE_WIDTH = len(MAZE_LAYOUT[0])
MAZE_HEIGHT = len(MAZE_LAYOUT)
CELL_SIZE = min(SCREEN_WIDTH // MAZE_WIDTH, (SCREEN_HEIGHT - 100) // MAZE_HEIGHT)
MAZE_X = (SCREEN_WIDTH - MAZE_WIDTH * CELL_SIZE) // 2
MAZE_Y = 50


class Player:
    """Pac-Man player."""
    
    def __init__(self, x: int, y: int):
        """Initialize player."""
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = MAZE_X + x * CELL_SIZE
        self.pixel_y = MAZE_Y + y * CELL_SIZE
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 2  # pixels per frame
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


class Ghost:
    """Ghost enemy."""
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        """Initialize ghost."""
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = MAZE_X + x * CELL_SIZE
        self.pixel_y = MAZE_Y + y * CELL_SIZE
        self.color = color
        self.direction = (0, 0)
        self.speed = 1.5
    
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


class PacManGame(BaseGame):
    """Pac-Man game implementation."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize Pac-Man game."""
        super().__init__(screen, "PacMan")
        self.maze: List[List[int]] = []
        self.player: Optional[Player] = None
        self.ghosts: List[Ghost] = []
        self.total_dots = 0
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Copy maze layout
        self.maze = [row[:] for row in MAZE_LAYOUT]
        
        # Count dots
        self.total_dots = sum(row.count(2) + row.count(3) for row in self.maze)
        
        # Create player at start position
        self.player = Player(13, 23)
        
        # Create ghosts
        self.ghosts = [
            Ghost(13, 11, RED),
            Ghost(14, 11, BLUE),
            Ghost(13, 12, YELLOW),
            Ghost(14, 12, WHITE),
        ]
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        if not self.player:
            return
        
        # Handle input
        if self.input_handler.is_key_just_pressed(pygame.K_UP):
            self.player.set_direction((0, -1))
        elif self.input_handler.is_key_just_pressed(pygame.K_DOWN):
            self.player.set_direction((0, 1))
        elif self.input_handler.is_key_just_pressed(pygame.K_LEFT):
            self.player.set_direction((-1, 0))
        elif self.input_handler.is_key_just_pressed(pygame.K_RIGHT):
            self.player.set_direction((1, 0))
        
        # Update player
        self.player.update(self.maze)
        
        # Check dot collection
        if self.maze[self.player.grid_y][self.player.grid_x] == 2:
            self.maze[self.player.grid_y][self.player.grid_x] = 0
            self.score += 10
            self.total_dots -= 1
        elif self.maze[self.player.grid_y][self.player.grid_x] == 3:
            self.maze[self.player.grid_y][self.player.grid_x] = 0
            self.score += 50
            self.player.power_mode = True
            self.player.power_timer = 10.0
            self.total_dots -= 1
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.player)
            
            # Check collision with player
            if ghost.grid_x == self.player.grid_x and ghost.grid_y == self.player.grid_y:
                if self.player.power_mode:
                    # Eat ghost
                    ghost.grid_x = 13
                    ghost.grid_y = 11
                    ghost.pixel_x = MAZE_X + ghost.grid_x * CELL_SIZE
                    ghost.pixel_y = MAZE_Y + ghost.grid_y * CELL_SIZE
                    self.score += 200
                else:
                    self.end_game()
                    return
        
        # Check win condition
        if self.total_dots == 0:
            self.score += 1000
            self.end_game()
    
    def render_game(self) -> None:
        """Render game objects."""
        # Draw maze
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell_x = MAZE_X + x * CELL_SIZE
                cell_y = MAZE_Y + y * CELL_SIZE
                
                if self.maze[y][x] == 1:
                    # Wall
                    pygame.draw.rect(
                        self.screen,
                        BLUE,
                        (cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                    )
                elif self.maze[y][x] == 2:
                    # Dot
                    center_x = cell_x + CELL_SIZE // 2
                    center_y = cell_y + CELL_SIZE // 2
                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 3)
                elif self.maze[y][x] == 3:
                    # Power pellet
                    center_x = cell_x + CELL_SIZE // 2
                    center_y = cell_y + CELL_SIZE // 2
                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 8)
        
        # Draw player
        if self.player:
            center_x = int(self.player.pixel_x + CELL_SIZE // 2)
            center_y = int(self.player.pixel_y + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), CELL_SIZE // 2 - 2)
        
        # Draw ghosts
        for ghost in self.ghosts:
            center_x = int(ghost.pixel_x + CELL_SIZE // 2)
            center_y = int(ghost.pixel_y + CELL_SIZE // 2)
            color = WHITE if self.player and self.player.power_mode else ghost.color
            pygame.draw.circle(self.screen, color, (center_x, center_y), CELL_SIZE // 2 - 2)

