"""Physics components for game objects."""

from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class Velocity:
    """Velocity component."""
    x: float = 0.0
    y: float = 0.0
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Initialize velocity."""
        self.x = x
        self.y = y
    
    def apply(self, position: Tuple[float, float], dt: float) -> Tuple[float, float]:
        """
        Apply velocity to position.
        
        Args:
            position: Current position
            dt: Delta time
            
        Returns:
            New position
        """
        return (position[0] + self.x * dt, position[1] + self.y * dt)
    
    def magnitude(self) -> float:
        """Get velocity magnitude."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass
class Acceleration:
    """Acceleration component."""
    x: float = 0.0
    y: float = 0.0
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Initialize acceleration."""
        self.x = x
        self.y = y
    
    def apply(self, velocity: Velocity, dt: float) -> None:
        """
        Apply acceleration to velocity.
        
        Args:
            velocity: Velocity to modify
            dt: Delta time
        """
        velocity.x += self.x * dt
        velocity.y += self.y * dt


@dataclass
class PhysicsComponent:
    """Physics component combining velocity and acceleration."""
    
    velocity: Velocity
    acceleration: Acceleration
    friction: float = 0.0
    max_speed: float = 0.0
    
    def __init__(
        self,
        velocity: Optional[Velocity] = None,
        acceleration: Optional[Acceleration] = None,
        friction: float = 0.0,
        max_speed: float = 0.0
    ):
        """Initialize physics component."""
        self.velocity = velocity or Velocity()
        self.acceleration = acceleration or Acceleration()
        self.friction = friction
        self.max_speed = max_speed
    
    def update(self, dt: float) -> None:
        """
        Update physics.
        
        Args:
            dt: Delta time
        """
        # Apply acceleration
        self.acceleration.apply(self.velocity, dt)
        
        # Apply friction
        if self.friction > 0:
            friction_factor = 1.0 - (self.friction * dt)
            self.velocity.x *= max(0.0, friction_factor)
            self.velocity.y *= max(0.0, friction_factor)
        
        # Limit speed
        if self.max_speed > 0:
            magnitude = self.velocity.magnitude()
            if magnitude > self.max_speed:
                scale = self.max_speed / magnitude
                self.velocity.x *= scale
                self.velocity.y *= scale
    
    def apply_to_position(self, position: Tuple[float, float], dt: float) -> Tuple[float, float]:
        """
        Apply physics to position.
        
        Args:
            position: Current position
            dt: Delta time
            
        Returns:
            New position
        """
        self.update(dt)
        return self.velocity.apply(position, dt)

