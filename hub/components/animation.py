"""Animation system for game objects."""

from typing import List, Optional, Tuple
import pygame
from dataclasses import dataclass


@dataclass
class AnimationFrame:
    """Single frame in an animation."""
    
    image: pygame.Surface
    duration: float  # Duration in seconds
    
    def __init__(self, image: pygame.Surface, duration: float):
        """Initialize animation frame."""
        self.image = image
        self.duration = duration


@dataclass
class Animation:
    """Animation sequence."""
    
    frames: List[AnimationFrame]
    loop: bool = True
    speed: float = 1.0
    
    def __init__(self, frames: List[AnimationFrame], loop: bool = True, speed: float = 1.0):
        """Initialize animation."""
        self.frames = frames
        self.loop = loop
        self.speed = speed
    
    @property
    def total_duration(self) -> float:
        """Get total animation duration."""
        return sum(frame.duration for frame in self.frames) / self.speed
    
    def get_frame(self, time: float) -> Optional[pygame.Surface]:
        """
        Get frame at given time.
        
        Args:
            time: Time in animation (seconds)
            
        Returns:
            Frame image or None if out of bounds
        """
        if not self.frames:
            return None
        
        total_duration = self.total_duration
        if not self.loop and time >= total_duration:
            return self.frames[-1].image
        
        # Loop time
        if self.loop:
            time = time % total_duration
        
        # Find frame
        current_time = 0.0
        for frame in self.frames:
            frame_duration = frame.duration / self.speed
            if time < current_time + frame_duration:
                return frame.image
            current_time += frame_duration
        
        return self.frames[-1].image if self.frames else None


@dataclass
class AnimationComponent:
    """Component for managing animations."""
    
    animations: dict
    current_animation: Optional[str] = None
    current_time: float = 0.0
    playing: bool = True
    
    def __init__(self, animations: Optional[dict] = None):
        """Initialize animation component."""
        self.animations = animations or {}
        self.current_animation = None
        self.current_time = 0.0
        self.playing = True
    
    def add_animation(self, name: str, animation: Animation) -> None:
        """Add an animation."""
        self.animations[name] = animation
    
    def play(self, name: str, restart: bool = False) -> None:
        """
        Play an animation.
        
        Args:
            name: Animation name
            restart: Whether to restart if already playing
        """
        if name not in self.animations:
            return
        
        if self.current_animation != name or restart:
            self.current_animation = name
            self.current_time = 0.0
        self.playing = True
    
    def stop(self) -> None:
        """Stop current animation."""
        self.playing = False
    
    def update(self, dt: float) -> None:
        """
        Update animation.
        
        Args:
            dt: Delta time
        """
        if not self.playing or self.current_animation is None:
            return
        
        animation = self.animations.get(self.current_animation)
        if animation:
            self.current_time += dt
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Get current animation frame.
        
        Returns:
            Current frame image or None
        """
        if self.current_animation is None:
            return None
        
        animation = self.animations.get(self.current_animation)
        if animation:
            return animation.get_frame(self.current_time)
        return None

