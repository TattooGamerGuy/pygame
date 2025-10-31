"""
UI Animation Framework.

Provides tweening, easing functions, and animation management for smooth UI animations.
"""

from enum import Enum
from typing import Callable, List, Optional
import math


class AnimationState(Enum):
    """Animation state enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"


class Easing:
    """Easing functions for smooth animations."""
    
    @staticmethod
    def linear(t: float) -> float:
        """
        Linear easing (no easing).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        """
        Ease-in easing (starts slow, ends fast).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        """
        Ease-out easing (starts fast, ends slow).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        return t * (2.0 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """
        Ease-in-out easing (starts slow, fast middle, ends slow).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        if t < 0.5:
            return 2.0 * t * t
        return -1.0 + (4.0 - 2.0 * t) * t
    
    @staticmethod
    def bounce(t: float) -> float:
        """
        Bounce easing (bounces at the end).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        if t < 1.0 / 2.75:
            return 7.5625 * t * t
        elif t < 2.0 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def elastic(t: float) -> float:
        """
        Elastic easing (oscillates).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased value
        """
        if t == 0.0:
            return 0.0
        if t == 1.0:
            return 1.0
        
        p = 0.3
        s = p / 4.0
        
        return math.pow(2.0, -10.0 * t) * math.sin((t - s) * (2.0 * math.pi) / p) + 1.0


class Tween:
    """Tween animation for animating values over time."""
    
    def __init__(
        self,
        start_value: float,
        end_value: float,
        duration: float,
        easing: Callable[[float], float] = Easing.linear,
        on_complete: Optional[Callable[[], None]] = None,
        on_update: Optional[Callable[[float], None]] = None,
        loop: bool = False
    ):
        """
        Initialize tween.
        
        Args:
            start_value: Starting value
            start_value: Starting value
            end_value: Ending value
            duration: Duration in seconds
            easing: Easing function
            on_complete: Callback when animation completes
            on_update: Callback on each update with current value
            loop: Whether to loop the animation
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing = easing
        self.on_complete = on_complete
        self.on_update = on_update
        self.loop = loop
        
        self._state = AnimationState.PENDING
        self._elapsed_time = 0.0
        self._current_value = start_value
        self._is_paused = False
        self._pause_time = 0.0
    
    @property
    def state(self) -> AnimationState:
        """Get current animation state."""
        return self._state
    
    @property
    def current_value(self) -> float:
        """Get current animated value."""
        return self._current_value
    
    def start(self) -> None:
        """Start the animation."""
        if self._state == AnimationState.COMPLETED and not self.loop:
            self.reset()
        
        self._state = AnimationState.RUNNING
        self._elapsed_time = 0.0
        self._is_paused = False
        self._current_value = self.start_value
    
    def update(self, dt: float) -> None:
        """
        Update the animation.
        
        Args:
            dt: Delta time in seconds
        """
        if self._state != AnimationState.RUNNING:
            return
        
        if self._is_paused:
            return
        
        self._elapsed_time += dt
        
        if self._elapsed_time >= self.duration:
            # Animation complete
            self._current_value = self.end_value
            
            if self.on_update:
                self.on_update(self._current_value)
            
            if self.loop:
                # Reset for loop
                self._elapsed_time = 0.0
                self._current_value = self.start_value
                if self.on_complete:
                    self.on_complete()
            else:
                self._state = AnimationState.COMPLETED
                if self.on_complete:
                    self.on_complete()
        else:
            # Calculate current value
            progress = self._elapsed_time / self.duration
            eased_progress = self.easing(progress)
            self._current_value = self.start_value + (self.end_value - self.start_value) * eased_progress
            
            if self.on_update:
                self.on_update(self._current_value)
    
    def pause(self) -> None:
        """Pause the animation."""
        if self._state == AnimationState.RUNNING:
            self._is_paused = True
            self._state = AnimationState.PAUSED
    
    def resume(self) -> None:
        """Resume the animation."""
        if self._state == AnimationState.PAUSED:
            self._is_paused = False
            self._state = AnimationState.RUNNING
    
    def stop(self) -> None:
        """Stop the animation."""
        self._state = AnimationState.STOPPED
        self._is_paused = False
    
    def reset(self) -> None:
        """Reset the animation to initial state."""
        self._state = AnimationState.PENDING
        self._elapsed_time = 0.0
        self._current_value = self.start_value
        self._is_paused = False
    
    def reverse(self) -> None:
        """Reverse the animation direction."""
        # Swap start and end values
        self.start_value, self.end_value = self.end_value, self.start_value
        self._elapsed_time = 0.0
        
        if self._state != AnimationState.RUNNING:
            self.start()


class AnimationManager:
    """Manages multiple animations centrally."""
    
    def __init__(self):
        """Initialize animation manager."""
        self._animations: List[Tween] = []
        self._paused = False
    
    def add(self, animation: Tween) -> None:
        """
        Add an animation to the manager.
        
        Args:
            animation: Tween to manage
        """
        if animation not in self._animations:
            self._animations.append(animation)
    
    def remove(self, animation: Tween) -> None:
        """
        Remove an animation from the manager.
        
        Args:
            animation: Tween to remove
        """
        if animation in self._animations:
            self._animations.remove(animation)
    
    def update(self, dt: float) -> None:
        """
        Update all managed animations.
        
        Args:
            dt: Delta time in seconds
        """
        if self._paused:
            return
        
        # Update all animations
        for animation in list(self._animations):  # Copy list to avoid modification during iteration
            animation.update(dt)
            
            # Remove completed animations (unless looping)
            if animation.state == AnimationState.COMPLETED and not animation.loop:
                self._animations.remove(animation)
    
    def get_active_animations(self) -> List[Tween]:
        """
        Get all animations being managed (including pending, running, paused).
        
        Returns:
            List of all managed animations
        """
        return list(self._animations)
    
    def clear(self) -> None:
        """Clear all animations."""
        self._animations.clear()
    
    def pause_all(self) -> None:
        """Pause all animations."""
        self._paused = True
        for animation in self._animations:
            animation.pause()
    
    def resume_all(self) -> None:
        """Resume all paused animations."""
        self._paused = False
        for animation in self._animations:
            if animation.state == AnimationState.PAUSED:
                animation.resume()

