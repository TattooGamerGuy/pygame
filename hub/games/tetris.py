"""Tetris game implementation."""

import random
from typing import List, Tuple, Optional
import pygame
from hub.games.base_game import BaseGame
from hub.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, CYAN, YELLOW, GREEN, RED, BLUE, MAGENTA, ORANGE


# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X = SCREEN_WIDTH // 2 - (GRID_WIDTH * CELL_SIZE) // 2
GRID_Y = 50


class Tetromino:
    """A Tetris piece."""
    
    def __init__(self, shape_index: int, x: int, y: int):
        """Initialize tetromino."""
        self.shape_index = shape_index
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = SHAPE_COLORS[shape_index]
        self.x = x
        self.y = y
    
    def rotate(self) -> List[List[int]]:
        """Get rotated shape (90 degrees clockwise)."""
        if not self.shape:
            return []
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        return rotated
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """Get list of (grid_x, grid_y) positions occupied by this piece."""
        cells = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    cells.append((self.x + j, self.y + i))
        return cells


class TetrisGame(BaseGame):
    """Tetris game implementation."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize Tetris game."""
        super().__init__(screen, "Tetris")
        self.grid: List[List[Optional[int]]] = []
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.fall_timer = 0.0
        self.fall_interval = 0.5
        self.lines_cleared = 0
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Initialize grid
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Create first piece
        self.spawn_piece()
        
        self.fall_timer = 0.0
        self.lines_cleared = 0
    
    def spawn_piece(self) -> None:
        """Spawn a new piece."""
        shape_index = random.randint(0, len(SHAPES) - 1)
        start_x = GRID_WIDTH // 2 - 1
        self.current_piece = Tetromino(shape_index, start_x, 0)
        
        # Spawn next piece
        next_shape_index = random.randint(0, len(SHAPES) - 1)
        self.next_piece = Tetromino(next_shape_index, 0, 0)
        
        # Check game over
        if self.check_collision(self.current_piece):
            self.end_game()
    
    def check_collision(self, piece: Tetromino, dx: int = 0, dy: int = 0) -> bool:
        """Check if piece collides with walls or other blocks."""
        cells = piece.get_cells()
        for x, y in cells:
            new_x = x + dx
            new_y = y + dy
            
            # Check walls
            if new_x < 0 or new_x >= GRID_WIDTH:
                return True
            if new_y >= GRID_HEIGHT:
                return True
            
            # Check grid
            if new_y >= 0 and self.grid[new_y][new_x] is not None:
                return True
        
        return False
    
    def place_piece(self) -> None:
        """Place current piece into grid and spawn next."""
        if not self.current_piece:
            return
        
        cells = self.current_piece.get_cells()
        for x, y in cells:
            if 0 <= y < GRID_HEIGHT:
                self.grid[y][x] = self.current_piece.shape_index
        
        # Clear lines
        self.clear_lines()
        
        # Spawn next piece
        self.current_piece = None
        self.spawn_piece()
    
    def clear_lines(self) -> None:
        """Clear filled lines and drop pieces above."""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        # Remove lines and shift down
        for y in reversed(lines_to_clear):
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        # Update score
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # Score: 100 * lines^2
            self.score += 100 * len(lines_to_clear) * len(lines_to_clear)
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        if not self.current_piece:
            return
        
        # Handle input
        if self.input_handler.is_key_just_pressed(pygame.K_LEFT):
            if not self.check_collision(self.current_piece, dx=-1):
                self.current_piece.x -= 1
        elif self.input_handler.is_key_just_pressed(pygame.K_RIGHT):
            if not self.check_collision(self.current_piece, dx=1):
                self.current_piece.x += 1
        elif self.input_handler.is_key_just_pressed(pygame.K_UP):
            # Rotate
            rotated_shape = self.current_piece.rotate()
            old_shape = self.current_piece.shape
            self.current_piece.shape = rotated_shape
            if self.check_collision(self.current_piece):
                self.current_piece.shape = old_shape
        elif self.input_handler.is_key_pressed(pygame.K_DOWN):
            # Fast fall
            self.fall_interval = 0.05
        else:
            self.fall_interval = 0.5
        
        # Auto fall
        self.fall_timer += dt
        if self.fall_timer >= self.fall_interval:
            self.fall_timer = 0.0
            if self.check_collision(self.current_piece, dy=1):
                self.place_piece()
            else:
                self.current_piece.y += 1
    
    def render_game(self) -> None:
        """Render game objects."""
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_x = GRID_X + x * CELL_SIZE
                cell_y = GRID_Y + y * CELL_SIZE
                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (cell_x, cell_y, CELL_SIZE, CELL_SIZE),
                    1
                )
                
                # Draw placed blocks
                if self.grid[y][x] is not None:
                    color_index = self.grid[y][x]
                    pygame.draw.rect(
                        self.screen,
                        SHAPE_COLORS[color_index],
                        (cell_x + 1, cell_y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
        
        # Draw current piece
        if self.current_piece:
            cells = self.current_piece.get_cells()
            for x, y in cells:
                if 0 <= y < GRID_HEIGHT:
                    cell_x = GRID_X + x * CELL_SIZE
                    cell_y = GRID_Y + y * CELL_SIZE
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece.color,
                        (cell_x + 1, cell_y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
        
        # Draw next piece preview
        if self.font and self.next_piece:
            preview_label = self.font.render("Next:", True, WHITE)
            self.screen.blit(preview_label, (GRID_X + GRID_WIDTH * CELL_SIZE + 20, GRID_Y))
            
            preview_x = GRID_X + GRID_WIDTH * CELL_SIZE + 20
            preview_y = GRID_Y + 40
            for i, row in enumerate(self.next_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            self.screen,
                            self.next_piece.color,
                            (preview_x + j * CELL_SIZE, preview_y + i * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2)
                        )

