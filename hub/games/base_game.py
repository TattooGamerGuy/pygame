"""Base game class with common functionality for all games."""

from abc import abstractmethod
from typing import Optional
import pygame
from hub.scenes.base_scene import BaseScene
from hub.utils.constants import SCREEN_SIZE, BLACK
from hub.utils.input_handler import InputHandler


class BaseGame(BaseScene):
    """Base class for all games with common functionality."""
    
    def __init__(self, screen: pygame.Surface, game_name: str):
        """
        Initialize the base game.
        
        Args:
            screen: The pygame Surface to render to
            game_name: Name of the game for display
        """
        super().__init__(screen)
        self.game_name = game_name
        self.score: int = 0
        self.high_score: int = 0
        self.paused: bool = False
        self.game_over: bool = False
        self.input_handler = InputHandler()
        self.font: Optional[pygame.font.Font] = None
        
    def init(self) -> None:
        """Initialize game-specific resources."""
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.load_high_score()
        
    def update(self, dt: float) -> None:
        """
        Update game logic.
        
        Args:
            dt: Delta time in seconds
        """
        if self.paused or self.game_over:
            return
        
        self.update_game(dt)
    
    @abstractmethod
    def update_game(self, dt: float) -> None:
        """
        Update game-specific logic. Override in subclasses.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    def render(self) -> None:
        """Render the game and UI overlay."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Render game-specific content
        self.render_game()
        
        # Render UI overlay
        self.render_ui()
        
        # Render pause/game over overlays
        if self.paused:
            self.render_pause_overlay()
        if self.game_over:
            self.render_game_over_overlay()
    
    @abstractmethod
    def render_game(self) -> None:
        """Render game-specific content. Override in subclasses."""
        pass
    
    def render_ui(self) -> None:
        """Render UI elements like score."""
        if self.font:
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            if self.high_score > 0:
                high_score_text = self.font.render(f"High: {self.high_score}", True, (255, 255, 255))
                self.screen.blit(high_score_text, (10, 50))
    
    def render_pause_overlay(self) -> None:
        """Render pause overlay."""
        if self.font:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED - Press P to resume", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(pause_text, text_rect)
    
    def render_game_over_overlay(self) -> None:
        """Render game over overlay."""
        if self.font:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(192)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = pygame.font.Font(None, 48).render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press R to restart or ESC to return to hub", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
            self.screen.blit(restart_text, restart_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        super().handle_event(event)
        
        # Update input handler
        if event.type in (pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            self.input_handler.update([event])
        
        # Handle pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
            
            # Handle restart
            if event.key == pygame.K_r and self.game_over:
                self.restart()
            
            # Return to hub on ESC during game over
            if event.key == pygame.K_ESCAPE and self.game_over:
                self.switch_scene("hub")
    
    def pause(self) -> None:
        """Pause the game."""
        self.paused = True
    
    def unpause(self) -> None:
        """Unpause the game."""
        self.paused = False
    
    def end_game(self) -> None:
        """End the game and check for high score."""
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def restart(self) -> None:
        """Restart the game."""
        self.score = 0
        self.paused = False
        self.game_over = False
        self.reset_game_state()
    
    @abstractmethod
    def reset_game_state(self) -> None:
        """Reset game-specific state. Override in subclasses."""
        pass
    
    def load_high_score(self) -> None:
        """Load high score from file. Override if needed."""
        try:
            import os
            score_file = os.path.join(os.path.expanduser("~"), f".{self.game_name.lower()}_highscore.txt")
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    self.high_score = int(f.read().strip())
        except Exception:
            pass  # Ignore errors, start with 0
    
    def save_high_score(self) -> None:
        """Save high score to file. Override if needed."""
        try:
            import os
            score_file = os.path.join(os.path.expanduser("~"), f".{self.game_name.lower()}_highscore.txt")
            with open(score_file, 'w') as f:
                f.write(str(self.high_score))
        except Exception:
            pass  # Ignore errors

