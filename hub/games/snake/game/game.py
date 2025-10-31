"""Main Snake game class."""

import random
from typing import List, Tuple, Optional
import pygame
from hub.games.base_game_modular import BaseGameModular
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.core.display import DisplayManager
from hub.events.event_bus import EventBus
from hub.config.defaults import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, GRID_SIZE
)
from hub.games.snake.constants import (
    INITIAL_MOVE_INTERVAL, MIN_MOVE_INTERVAL,
    SPEED_INCREASE_FACTOR, FOOD_SCORE
)


class SnakeGameModular(BaseGameModular):
    """Modular Snake game implementation."""
    
    def __init__(
        self,
        display_manager: DisplayManager,
        input_service: InputService,
        audio_service: AudioService,
        event_bus: EventBus
    ):
        """Initialize Snake game with dependency injection."""
        super().__init__(display_manager, input_service, audio_service, event_bus, "Snake")
        self.grid_width = SCREEN_WIDTH // GRID_SIZE
        self.grid_height = SCREEN_HEIGHT // GRID_SIZE
        self.snake: List[Tuple[int, int]] = []
        self.direction: Tuple[int, int] = (1, 0)  # (dx, dy)
        self.next_direction: Tuple[int, int] = (1, 0)
        self.food: Optional[Tuple[int, int]] = None
        self.move_timer = 0.0
        self.move_interval = INITIAL_MOVE_INTERVAL
        self.grow_pending = False
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Start snake in center
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.move_timer = 0.0
        self.move_interval = INITIAL_MOVE_INTERVAL
        self.grow_pending = False
        self.spawn_food()
    
    def spawn_food(self) -> None:
        """Spawn food at a random location not occupied by snake."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        # Handle input using InputService
        if self.input_service.is_key_just_pressed(pygame.K_UP):
            if self.direction != (0, 1):  # Can't reverse into itself
                self.next_direction = (0, -1)
        elif self.input_service.is_key_just_pressed(pygame.K_DOWN):
            if self.direction != (0, -1):
                self.next_direction = (0, 1)
        elif self.input_service.is_key_just_pressed(pygame.K_LEFT):
            if self.direction != (1, 0):
                self.next_direction = (-1, 0)
        elif self.input_service.is_key_just_pressed(pygame.K_RIGHT):
            if self.direction != (-1, 0):
                self.next_direction = (1, 0)
        
        # Update move timer
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0.0
            self.direction = self.next_direction
            
            # Calculate new head position
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 0 or new_head[1] >= self.grid_height):
                self.end_game()
                return
            
            # Check self collision
            if new_head in self.snake:
                self.end_game()
                return
            
            # Move snake
            self.snake.insert(0, new_head)
            
            # Check food collision
            if new_head == self.food:
                self.score += FOOD_SCORE
                self.grow_pending = True
                self.spawn_food()
                # Speed up slightly
                self.move_interval = max(MIN_MOVE_INTERVAL, self.move_interval * SPEED_INCREASE_FACTOR)
            else:
                # Remove tail if not growing
                if not self.grow_pending:
                    self.snake.pop()
                else:
                    self.grow_pending = False
    
    def render_game(self) -> None:
        """Render game objects."""
        # Draw food
        if self.food:
            food_x = self.food[0] * GRID_SIZE
            food_y = self.food[1] * GRID_SIZE
            pygame.draw.rect(
                self.screen,
                RED,
                (food_x, food_y, GRID_SIZE, GRID_SIZE)
            )
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            # Head is brighter
            color = GREEN if i == 0 else (0, 200, 0)
            pygame.draw.rect(
                self.screen,
                color,
                (x, y, GRID_SIZE - 1, GRID_SIZE - 1)
            )

