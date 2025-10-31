"""Pong game implementation."""

import random
from typing import Optional
import pygame
from hub.games.base_game import BaseGame
from hub.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class Paddle:
    """Paddle for Pong game."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize paddle."""
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 400  # pixels per second
        self.score = 0
    
    def update(self, dt: float, direction: int = 0, is_ai: bool = False, ball_y: float = 0) -> None:
        """
        Update paddle position.
        
        Args:
            dt: Delta time
            direction: Direction (-1 up, 1 down, 0 none)
            is_ai: Whether this is an AI paddle
            ball_y: Y position of ball (for AI)
        """
        if is_ai:
            # Simple AI: follow ball
            if self.rect.centery < ball_y - 10:
                direction = 1
            elif self.rect.centery > ball_y + 10:
                direction = -1
            else:
                direction = 0
        
        move_amount = self.speed * dt * direction
        self.rect.y += move_amount
        
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the paddle."""
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    """Ball for Pong game."""
    
    def __init__(self, x: int, y: int, radius: int):
        """Initialize ball."""
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.speed = 400
        self.velocity_x = self.speed
        self.velocity_y = 0
        # Random initial direction
        if random.random() > 0.5:
            self.velocity_x *= -1
        self.velocity_y = random.uniform(-100, 100)
    
    def update(self, dt: float, paddle1: Paddle, paddle2: Paddle) -> int:
        """
        Update ball position and check collisions.
        
        Args:
            dt: Delta time
            paddle1: Left paddle
            paddle2: Right paddle
            
        Returns:
            0 = no point, 1 = left scored, 2 = right scored
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Bounce off top and bottom
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity_y *= -1
        elif self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.velocity_y *= -1
        
        # Check paddle collisions
        ball_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        
        if ball_rect.colliderect(paddle1.rect) and self.velocity_x < 0:
            self.x = paddle1.rect.right + self.radius
            self.velocity_x *= -1.1  # Speed up slightly
            # Adjust angle based on where ball hits paddle
            relative_y = (self.y - paddle1.rect.centery) / (paddle1.rect.height / 2)
            self.velocity_y = relative_y * 200
        
        if ball_rect.colliderect(paddle2.rect) and self.velocity_x > 0:
            self.x = paddle2.rect.left - self.radius
            self.velocity_x *= -1.1
            relative_y = (self.y - paddle2.rect.centery) / (paddle2.rect.height / 2)
            self.velocity_y = relative_y * 200
        
        # Check scoring
        if self.x < 0:
            return 2  # Right player scores
        elif self.x > SCREEN_WIDTH:
            return 1  # Left player scores
        
        return 0
    
    def reset(self) -> None:
        """Reset ball to center."""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 400
        self.velocity_x = self.speed if random.random() > 0.5 else -self.speed
        self.velocity_y = random.uniform(-100, 100)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the ball."""
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)


class PongGame(BaseGame):
    """Pong game implementation."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize Pong game."""
        super().__init__(screen, "Pong")
        self.paddle1: Optional[Paddle] = None
        self.paddle2: Optional[Paddle] = None
        self.ball: Optional[Ball] = None
        self.paddle_width = 15
        self.paddle_height = 100
        self.ball_radius = 10
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Create paddles
        paddle_y = (SCREEN_HEIGHT - self.paddle_height) // 2
        self.paddle1 = Paddle(50, paddle_y, self.paddle_width, self.paddle_height)
        self.paddle2 = Paddle(
            SCREEN_WIDTH - 50 - self.paddle_width,
            paddle_y,
            self.paddle_width,
            self.paddle_height
        )
        
        # Create ball
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.ball_radius)
        
        # Reset scores
        self.paddle1.score = 0
        self.paddle2.score = 0
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        if not self.paddle1 or not self.paddle2 or not self.ball:
            return
        
        # Handle input for paddle1 (left paddle - WASD or arrow keys)
        direction1 = 0
        if self.input_handler.is_key_pressed(pygame.K_w) or self.input_handler.is_key_pressed(pygame.K_UP):
            direction1 = -1
        elif self.input_handler.is_key_pressed(pygame.K_s) or self.input_handler.is_key_pressed(pygame.K_DOWN):
            direction1 = 1
        
        # Update paddles
        self.paddle1.update(dt, direction1)
        self.paddle2.update(dt, 0, is_ai=True, ball_y=self.ball.y)
        
        # Update ball
        result = self.ball.update(dt, self.paddle1, self.paddle2)
        
        if result == 1:
            self.paddle1.score += 1
            self.score = self.paddle1.score
            if self.paddle1.score >= 10:
                self.end_game()
            else:
                self.ball.reset()
        elif result == 2:
            self.paddle2.score += 1
            if self.paddle2.score >= 10:
                self.end_game()
            else:
                self.ball.reset()
    
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

