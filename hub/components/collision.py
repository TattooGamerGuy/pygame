"""Collision detection components and utilities."""

from typing import List, Tuple, Optional, Callable
import pygame
from dataclasses import dataclass


@dataclass
class CollisionComponent:
    """Component for collision detection."""
    
    rect: pygame.Rect
    collision_layer: int = 0
    collision_mask: int = 0xFFFF
    on_collision: Optional[Callable[['CollisionComponent'], None]] = None
    
    def __init__(
        self,
        rect: pygame.Rect,
        collision_layer: int = 0,
        collision_mask: int = 0xFFFF,
        on_collision: Optional[Callable[['CollisionComponent'], None]] = None
    ):
        """Initialize collision component."""
        self.rect = rect
        self.collision_layer = collision_layer
        self.collision_mask = collision_mask
        self.on_collision = on_collision
    
    def collides_with(self, other: 'CollisionComponent') -> bool:
        """
        Check if this collides with another component.
        
        Args:
            other: Other collision component
            
        Returns:
            True if collision detected
        """
        # Check layer/mask
        if not (self.collision_mask & (1 << other.collision_layer)):
            return False
        if not (other.collision_mask & (1 << self.collision_layer)):
            return False
        
        # Check rectangle collision
        return self.rect.colliderect(other.rect)
    
    def get_collision_point(self, other: 'CollisionComponent') -> Optional[Tuple[float, float]]:
        """
        Get collision point if colliding.
        
        Args:
            other: Other collision component
            
        Returns:
            Collision point or None
        """
        if not self.collides_with(other):
            return None
        
        # Return center of intersection
        intersection = self.rect.clip(other.rect)
        return (intersection.centerx, intersection.centery)


class CollisionDetector:
    """Utility for detecting collisions between multiple objects."""
    
    def __init__(self):
        """Initialize collision detector."""
        self.components: List[CollisionComponent] = []
    
    def add(self, component: CollisionComponent) -> None:
        """Add a collision component."""
        if component not in self.components:
            self.components.append(component)
    
    def remove(self, component: CollisionComponent) -> None:
        """Remove a collision component."""
        if component in self.components:
            self.components.remove(component)
    
    def check_all(self) -> List[Tuple[CollisionComponent, CollisionComponent]]:
        """
        Check all collisions.
        
        Returns:
            List of colliding component pairs
        """
        collisions = []
        for i, comp1 in enumerate(self.components):
            for comp2 in self.components[i + 1:]:
                if comp1.collides_with(comp2):
                    collisions.append((comp1, comp2))
                    # Trigger callbacks
                    if comp1.on_collision:
                        comp1.on_collision(comp2)
                    if comp2.on_collision:
                        comp2.on_collision(comp1)
        return collisions
    
    def check_one(self, component: CollisionComponent) -> List[CollisionComponent]:
        """
        Check collisions for one component.
        
        Args:
            component: Component to check
            
        Returns:
            List of colliding components
        """
        collisions = []
        for other in self.components:
            if other != component and component.collides_with(other):
                collisions.append(other)
                if component.on_collision:
                    component.on_collision(other)
        return collisions

