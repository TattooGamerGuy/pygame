"""Main Pong game class."""

from typing import Optional
import pygame
from hub.games.base_game_modular import BaseGameModular
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.core.display import DisplayManager
from hub.events.event_bus import EventBus
from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from hub.games.pong.components import Paddle, Ball
from hub.games.pong.ai import PaddleAI
from hub.games.pong.constants import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED,
    BALL_RADIUS, BALL_SPEED, WIN_SCORE
)


class PongGameModular(BaseGameModular):
    """Modular Pong game implementation."""
    
    def __init__(
        self,
        display_manager: DisplayManager,
        input_service: InputService,
        audio_service: AudioService,
        event_bus: EventBus
    ):
        """Initialize Pong game with dependency injection."""
        super().__init__(display_manager, input_service, audio_service, event_bus, "Pong")
        self.paddle1: Optional[Paddle] = None
        self.paddle2: Optional[Paddle] = None
        self.ball: Optional[Ball] = None
        self.paddle2_ai: Optional[PaddleAI] = None
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Create paddles
        paddle_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle1 = Paddle(50, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.paddle2 = Paddle(
            SCREEN_WIDTH - 50 - PADDLE_WIDTH,
            paddle_y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED
        )
        
        # Create ball
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_SPEED)
        
        # Create AI controller for paddle 2
        self.paddle2_ai = PaddleAI(self.paddle2)
        
        # Reset scores
        self.paddle1.score = 0
        self.paddle2.score = 0
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        if not self.paddle1 or not self.paddle2 or not self.ball:
            return
        
        # Handle input for paddle1 using InputService
        direction1 = 0
        if self.input_service.is_key_pressed(pygame.K_w) or self.input_service.is_key_pressed(pygame.K_UP):
            direction1 = -1
        elif self.input_service.is_key_pressed(pygame.K_s) or self.input_service.is_key_pressed(pygame.K_DOWN):
            direction1 = 1
        
        # Update paddle1
        self.paddle1.update(dt, direction1)
        
        # Update paddle2 with AI
        ai_direction = self.paddle2_ai.get_direction(self.ball.get_y())
        self.paddle2.update(dt, ai_direction)
        
        # Update ball
        result = self.ball.update(dt, self.paddle1, self.paddle2)
        
        if result == 1:
            self.paddle1.score += 1
            self.score = self.paddle1.score
            if self.paddle1.score >= WIN_SCORE:
                self.end_game()
            else:
                self.ball.reset(BALL_SPEED)
        elif result == 2:
            self.paddle2.score += 1
            if self.paddle2.score >= WIN_SCORE:
                self.end_game()
            else:
                self.ball.reset(BALL_SPEED)
    
    def render_game(self) -> None:
        """Render game objects."""
        if not self.paddle1 or not self.paddle2 or not self.ball:
            return
        
        # Draw center line
        pygame.draw.line(
            self.screen,
            WHITE,
            (SCREEN_WIDTH // 2, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT),
            2
        )
        
        # Render paddles
        self.paddle1.render(self.screen)
        self.paddle2.render(self.screen)
        
        # Render ball
        self.ball.render(self.screen)
    
    def render_ui(self) -> None:
        """Render UI including scores."""
        super().render_ui()
        
        if self.font and self.paddle1 and self.paddle2:
            # Player 1 score (left)
            score1_text = self.font.render(str(self.paddle1.score), True, WHITE)
            score1_rect = score1_text.get_rect(
                centerx=SCREEN_WIDTH // 4,
                y=50
            )
            self.screen.blit(score1_text, score1_rect)
            
            # Player 2 score (right)
            score2_text = self.font.render(str(self.paddle2.score), True, WHITE)
            score2_rect = score2_text.get_rect(
                centerx=3 * SCREEN_WIDTH // 4,
                y=50
            )
            self.screen.blit(score2_text, score2_rect)

