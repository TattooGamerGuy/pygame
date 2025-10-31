"""Ball component for Pong game."""

import random
import pygame
from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class Ball:
    """Ball component for Pong game."""
    
    def __init__(self, x: int, y: int, radius: int, speed: int):
        """
        Initialize ball.
        
        Args:
            x: Initial X position
            y: Initial Y position
            radius: Ball radius
            speed: Ball speed (pixels per second)
        """
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.speed = speed
        self.velocity_x = self.speed
        self.velocity_y = 0
        # Random initial direction
        if random.random() > 0.5:
            self.velocity_x *= -1
        self.velocity_y = random.uniform(-100, 100)
    
    def update(self, dt: float, paddle1, paddle2) -> int:
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
    
    def reset(self, speed: int) -> None:
        """
        Reset ball to center.
        
        Args:
            speed: Ball speed to reset to
        """
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = speed
        self.velocity_x = self.speed if random.random() > 0.5 else -self.speed
        self.velocity_y = random.uniform(-100, 100)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the ball."""
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def get_y(self) -> float:
        """Get ball Y position."""
        return self.y

