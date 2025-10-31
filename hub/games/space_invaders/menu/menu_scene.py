"""Main menu scene for Space Invaders."""

from typing import Optional
import pygame
from hub.scenes.base_scene import BaseScene
from hub.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, GREEN, RED
from hub.games.space_invaders.components import Enemy
from hub.games.space_invaders.constants import ENEMY_SPACING_X, ENEMY_SPACING_Y


class SpaceInvadersMenuScene(BaseScene):
    """Main menu scene for Space Invaders game."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize the menu scene."""
        super().__init__(screen)
        self.title_font: Optional[pygame.font.Font] = None
        self.subtitle_font: Optional[pygame.font.Font] = None
        self.text_font: Optional[pygame.font.Font] = None
        self.high_score = 0
        self.animation_offset = 0.0
        self.animation_direction = 1
        
        # Preview enemies for animation
        self.preview_enemies: list = []
    
    def init(self) -> None:
        """Initialize menu resources."""
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 96)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.load_high_score()
        self.setup_preview_enemies()
        self.animation_offset = 0.0
        self.animation_direction = 1
    
    def setup_preview_enemies(self) -> None:
        """Setup preview enemy formation for menu animation."""
        self.preview_enemies.clear()
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 - 50
        
        # Create a small formation of enemies (3 rows x 5 columns)
        for row in range(3):
            for col in range(5):
                x = center_x + (col - 2) * ENEMY_SPACING_X - 100
                y = center_y + (row - 1) * ENEMY_SPACING_Y - 100
                enemy = Enemy(x, y, 50)
                self.preview_enemies.append(enemy)
    
    def load_high_score(self) -> None:
        """Load high score from file."""
        try:
            import os
            score_file = os.path.join(os.path.expanduser("~"), ".spaceinvaders_highscore.txt")
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    self.high_score = int(f.read().strip())
        except Exception:
            self.high_score = 0
    
    def get_game_stats(self) -> dict:
        """
        Get game statistics for display.
        
        Returns:
            Dictionary with game stats
        """
        try:
            import os
            score_file = os.path.join(os.path.expanduser("~"), ".spaceinvaders_highscore.txt")
            high_score = 0
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    high_score = int(f.read().strip())
            return {"high_score": high_score}
        except Exception:
            return {"high_score": 0}
    
    def update(self, dt: float) -> None:
        """Update menu animation."""
        # Animate enemies moving left and right
        move_speed = 50  # pixels per second
        self.animation_offset += dt * move_speed * self.animation_direction
        
        if abs(self.animation_offset) > 40:
            self.animation_direction *= -1
        
        # Reset enemy positions periodically for smooth animation
        # (The actual movement is handled in render)
    
    def render(self) -> None:
        """Render the menu screen."""
        # Fill background with space-like gradient
        for y in range(SCREEN_HEIGHT):
            intensity = max(0, min(255, 20 + int(y / SCREEN_HEIGHT * 20)))
            pygame.draw.line(self.screen, (intensity // 4, intensity // 4, intensity // 2), 
                           (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        import random
        random.seed(42)  # Consistent star pattern
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw animated enemy formation
        for enemy in self.preview_enemies:
            # Temporarily offset for animation
            original_x = enemy.x
            enemy.x += self.animation_offset
            enemy.render(self.screen)
            enemy.x = original_x
        
        # Draw title
        if self.title_font:
            title_text = self.title_font.render("SPACE INVADERS", True, GREEN)
            title_rect = title_text.get_rect(centerx=SCREEN_WIDTH // 2, y=80)
            self.screen.blit(title_text, title_rect)
            
            # Draw subtitle
            if self.subtitle_font:
                subtitle_text = self.subtitle_font.render("Defend Earth!", True, YELLOW)
                subtitle_rect = subtitle_text.get_rect(centerx=SCREEN_WIDTH // 2, y=160)
                self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw instructions
        if self.text_font:
            instructions = [
                "CONTROLS:",
                "",
                "Arrow Keys - Move Ship",
                "SPACE - Fire Laser",
                "P - Pause Game",
                "",
                "POINTS:",
                "Top Enemy (Yellow) - 30",
                "Middle Enemy (Cyan) - 20",
                "Bottom Enemy (Red) - 10",
                "UFO Bonus - 50/100/150/300",
                "",
                "Press SPACE or ENTER to Start",
                "ESC - Return to Hub"
            ]
            
            start_y = SCREEN_HEIGHT - 450
            for i, instruction in enumerate(instructions):
                if instruction:
                    if instruction.startswith("CONTROLS") or instruction.startswith("POINTS"):
                        color = YELLOW
                        font = self.text_font
                    elif instruction.startswith("Press") or instruction.startswith("ESC"):
                        color = GREEN
                        font = self.text_font
                    else:
                        color = WHITE
                        font = self.text_font
                    
                    text = font.render(instruction, True, color)
                    text_rect = text.get_rect(centerx=SCREEN_WIDTH // 2, y=start_y + i * 25)
                    self.screen.blit(text, text_rect)
        
        # Draw high score
        if self.subtitle_font and self.high_score > 0:
            score_text = self.subtitle_font.render(f"HIGH SCORE: {self.high_score}", True, RED)
            score_rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 60)
            self.screen.blit(score_text, score_rect)
        
        # Draw blinking "PRESS SPACE" indicator
        import time
        if int(time.time() * 2) % 2 == 0:
            if self.text_font:
                blink_text = self.text_font.render(">>> PRESS SPACE <<<", True, GREEN)
                blink_rect = blink_text.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 120)
                self.screen.blit(blink_text, blink_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events."""
        super().handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.switch_scene("space_invaders")
            elif event.key == pygame.K_ESCAPE:
                self.switch_scene("hub")
