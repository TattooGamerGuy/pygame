"""Particle system for Space Invaders visual effects."""

from typing import List, Tuple
import random
import math
import pygame
from hub.config.defaults import RED, GREEN, YELLOW, WHITE, BLACK


class Particle:
    """Single particle for effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: float = 0.5, size: int = 2):
        """
        Initialize particle.
        
        Args:
            x: Starting X position
            y: Starting Y position
            vx: X velocity
            vy: Y velocity
            color: Particle color
            lifetime: How long particle lives (seconds)
            size: Particle size in pixels
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.size = size
        self.alpha = 255
    
    def update(self, dt: float) -> bool:
        """
        Update particle.
        
        Args:
            dt: Delta time
            
        Returns:
            True if particle is still alive
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.age += dt
        
        # Fade out over lifetime
        if self.lifetime > 0:
            progress = self.age / self.lifetime
            self.alpha = int(255 * (1.0 - progress))
            
            # Apply gravity/slowdown
            self.vy += 200 * dt  # Gravity
            self.vx *= 0.98  # Air resistance
        
        return self.age < self.lifetime and self.alpha > 0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render particle."""
        if self.alpha > 0:
            # Create temporary surface for alpha blending
            temp_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(temp_surf, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(temp_surf, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    """Manages particle effects."""
    
    def __init__(self):
        """Initialize particle system."""
        self.particles: List[Particle] = []
    
    def add_explosion(self, x: float, y: float, color: Tuple[int, int, int] = RED, 
                     count: int = 15) -> None:
        """
        Add explosion particle effect.
        
        Args:
            x: Explosion center X
            y: Explosion center Y
            color: Base particle color
            count: Number of particles
        """
        for _ in range(count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random color variation
            color_var = (
                min(255, max(0, color[0] + random.randint(-30, 30))),
                min(255, max(0, color[1] + random.randint(-30, 30))),
                min(255, max(0, color[2] + random.randint(-30, 30)))
            )
            
            lifetime = random.uniform(0.3, 0.8)
            size = random.randint(1, 3)
            
            self.particles.append(Particle(x, y, vx, vy, color_var, lifetime, size))
    
    def add_bullet_trail(self, x: float, y: float, is_enemy: bool = False) -> None:
        """
        Add bullet trail particle.
        
        Args:
            x: Bullet X position
            y: Bullet Y position
            is_enemy: Whether enemy bullet
        """
        color = RED if is_enemy else GREEN
        # Small, subtle trail particles
        for _ in range(2):
            vx = random.uniform(-10, 10)
            vy = random.uniform(-5, 5)
            size = 1
            lifetime = random.uniform(0.1, 0.2)
            self.particles.append(Particle(x, y, vx, vy, color, lifetime, size))
    
    def add_hit_spark(self, x: float, y: float) -> None:
        """
        Add spark particles on hit.
        
        Args:
            x: Hit X position
            y: Hit Y position
        """
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 100)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            # Yellow/white sparks
            spark_color = random.choice([YELLOW, WHITE, (255, 200, 100)])
            lifetime = random.uniform(0.2, 0.4)
            size = random.randint(1, 2)
            self.particles.append(Particle(x, y, vx, vy, spark_color, lifetime, size))
    
    def update(self, dt: float) -> None:
        """
        Update all particles.
        
        Args:
            dt: Delta time
        """
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render all particles.
        
        Args:
            surface: Surface to render to
        """
        for particle in self.particles:
            particle.render(surface)
    
    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()

