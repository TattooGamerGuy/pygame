"""Space Invaders game implementation."""

import random
from typing import List, Optional
import pygame
from hub.games.base_game import BaseGame
from hub.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, YELLOW


class Bullet:
    """Bullet for Space Invaders."""
    
    def __init__(self, x: float, y: float, speed: float, is_enemy: bool = False):
        """Initialize bullet."""
        self.x = x
        self.y = y
        self.speed = speed if not is_enemy else -speed
        self.is_enemy = is_enemy
        self.width = 4
        self.height = 10
    
    def update(self, dt: float) -> bool:
        """
        Update bullet position.
        
        Returns:
            True if bullet is still on screen
        """
        self.y += self.speed * dt
        return 0 <= self.y <= SCREEN_HEIGHT
    
    def get_rect(self) -> pygame.Rect:
        """Get bullet rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render bullet."""
        color = RED if self.is_enemy else GREEN
        pygame.draw.rect(surface, color, self.get_rect())


class Enemy:
    """Enemy ship for Space Invaders."""
    
    def __init__(self, x: float, y: float):
        """Initialize enemy."""
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.speed = 50
        self.direction = 1
    
    def update(self, dt: float, direction: int) -> None:
        """Update enemy position."""
        self.x += self.speed * dt * direction
    
    def get_rect(self) -> pygame.Rect:
        """Get enemy rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render enemy."""
        pygame.draw.rect(surface, YELLOW, self.get_rect())


class Player:
    """Player ship for Space Invaders."""
    
    def __init__(self, x: float, y: float):
        """Initialize player."""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 300
    
    def update(self, dt: float, direction: int) -> None:
        """Update player position."""
        self.x += self.speed * dt * direction
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
    
    def get_rect(self) -> pygame.Rect:
        """Get player rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render player."""
        pygame.draw.rect(surface, GREEN, self.get_rect())


class SpaceInvadersGame(BaseGame):
    """Space Invaders game implementation."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize Space Invaders game."""
        super().__init__(screen, "SpaceInvaders")
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.player_bullets: List[Bullet] = []
        self.enemy_bullets: List[Bullet] = []
        self.enemy_direction = 1
        self.enemy_move_timer = 0.0
        self.enemy_move_interval = 1.0
        self.enemy_shoot_timer = 0.0
        self.enemy_shoot_interval = 1.5
        self.enemy_rows = 5
        self.enemy_cols = 10
        self.enemy_spacing_x = 50
        self.enemy_spacing_y = 40
        self.start_y = 100
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state."""
        # Create player
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60)
        
        # Create enemies
        self.enemies.clear()
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):
                x = col * self.enemy_spacing_x + 100
                y = row * self.enemy_spacing_y + self.start_y
                self.enemies.append(Enemy(x, y))
        
        # Clear bullets
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        
        # Reset timers
        self.enemy_move_timer = 0.0
        self.enemy_shoot_timer = 0.0
        self.enemy_direction = 1
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        if not self.player:
            return
        
        # Handle player input
        direction = 0
        if self.input_handler.is_key_pressed(pygame.K_LEFT):
            direction = -1
        elif self.input_handler.is_key_pressed(pygame.K_RIGHT):
            direction = 1
        
        self.player.update(dt, direction)
        
        # Shooting
        if self.input_handler.is_key_just_pressed(pygame.K_SPACE):
            bullet_x = self.player.x + self.player.width // 2 - 2
            bullet_y = self.player.y
            self.player_bullets.append(Bullet(bullet_x, bullet_y, 400))
        
        # Update enemies
        self.enemy_move_timer += dt
        if self.enemy_move_timer >= self.enemy_move_interval:
            self.enemy_move_timer = 0.0
            
            # Check if enemies need to move down and reverse
            need_reverse = False
            for enemy in self.enemies:
                enemy.update(dt, self.enemy_direction)
                if enemy.x <= 0 or enemy.x + enemy.width >= SCREEN_WIDTH:
                    need_reverse = True
            
            if need_reverse:
                self.enemy_direction *= -1
                for enemy in self.enemies:
                    enemy.y += 20
        
        # Enemy shooting
        self.enemy_shoot_timer += dt
        if self.enemy_shoot_timer >= self.enemy_shoot_interval and self.enemies:
            self.enemy_shoot_timer = 0.0
            # Random enemy shoots
            shooter = random.choice(self.enemies)
            bullet_x = shooter.x + shooter.width // 2 - 2
            bullet_y = shooter.y + shooter.height
            self.enemy_bullets.append(Bullet(bullet_x, bullet_y, 200, is_enemy=True))
        
        # Update bullets
        self.player_bullets = [b for b in self.player_bullets if b.update(dt)]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.update(dt)]
        
        # Check collisions
        # Player bullets vs enemies
        for bullet in self.player_bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if bullet_rect.colliderect(enemy.get_rect()):
                    self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
        
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.end_game()
                return
        
        # Enemies reach player
        for enemy in self.enemies:
            if enemy.y + enemy.height >= self.player.y:
                self.end_game()
                return
        
        # Check win condition
        if len(self.enemies) == 0:
            self.score += 1000
            self.end_game()
    
    def render_game(self) -> None:
        """Render game objects."""
        # Render player
        if self.player:
            self.player.render(self.screen)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # Render bullets
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.render(self.screen)

