"""Main Pac-Man game class."""

from typing import List, Optional
import pygame
from hub.games.base_game_modular import BaseGameModular
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.core.display import DisplayManager
from hub.events.event_bus import EventBus
from hub.config.defaults import WHITE, BLACK, YELLOW, BLUE, RED
from hub.games.pacman.components import Player, Ghost
from hub.games.pacman.maze import MAZE_LAYOUT
from hub.games.pacman.constants import (
    MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, MAZE_X, MAZE_Y,
    DOT_SCORE, POWER_PELLET_SCORE, GHOST_SCORE, CLEAR_BONUS, POWER_MODE_DURATION
)


class PacManGameModular(BaseGameModular):
    """Modular Pac-Man game implementation."""
    
    def __init__(
        self,
        display_manager: DisplayManager,
        input_service: InputService,
        audio_service: AudioService,
        event_bus: EventBus
    ):
        """Initialize Pac-Man game with dependency injection."""
        super().__init__(display_manager, input_service, audio_service, event_bus, "PacMan")
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
        
        # Handle input using InputService
        if self.input_service.is_key_just_pressed(pygame.K_UP):
            self.player.set_direction((0, -1))
        elif self.input_service.is_key_just_pressed(pygame.K_DOWN):
            self.player.set_direction((0, 1))
        elif self.input_service.is_key_just_pressed(pygame.K_LEFT):
            self.player.set_direction((-1, 0))
        elif self.input_service.is_key_just_pressed(pygame.K_RIGHT):
            self.player.set_direction((1, 0))
        
        # Update player
        self.player.update(self.maze)
        
        # Check dot collection
        if self.maze[self.player.grid_y][self.player.grid_x] == 2:
            self.maze[self.player.grid_y][self.player.grid_x] = 0
            self.score += DOT_SCORE
            self.total_dots -= 1
        elif self.maze[self.player.grid_y][self.player.grid_x] == 3:
            self.maze[self.player.grid_y][self.player.grid_x] = 0
            self.score += POWER_PELLET_SCORE
            self.player.activate_power_mode(POWER_MODE_DURATION)
            self.total_dots -= 1
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.player)
            
            # Check collision with player
            if ghost.grid_x == self.player.grid_x and ghost.grid_y == self.player.grid_y:
                if self.player.power_mode:
                    # Eat ghost
                    ghost.reset_position(13, 11)
                    self.score += GHOST_SCORE
                else:
                    self.end_game()
                    return
        
        # Check win condition
        if self.total_dots == 0:
            self.score += CLEAR_BONUS
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

