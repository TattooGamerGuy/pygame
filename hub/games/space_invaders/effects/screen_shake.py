"""Screen shake effect for Space Invaders."""

from typing import Tuple
import random
import math


class ScreenShake:
    """Manages screen shake effects."""
    
    def __init__(self):
        """Initialize screen shake system."""
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.duration = 0.0
        self.timer = 0.0
        self.intensity = 0.0
    
    def shake(self, duration: float = 0.2, intensity: float = 5.0) -> None:
        """
        Trigger a screen shake.
        
        Args:
            duration: How long to shake (seconds)
            intensity: Shake intensity (pixels)
        """
        if self.timer <= 0 or intensity > self.intensity:
            self.duration = duration
            self.timer = duration
            self.intensity = intensity
    
    def update(self, dt: float) -> None:
        """
        Update shake effect.
        
        Args:
            dt: Delta time
        """
        if self.timer > 0:
            self.timer -= dt
            
            # Calculate shake offset with decay
            progress = self.timer / self.duration if self.duration > 0 else 0
            current_intensity = self.intensity * progress
            
            # Random offset based on intensity
            angle = random.uniform(0, 2 * math.pi)
            shake_amount = random.uniform(0, current_intensity)
            self.offset_x = math.cos(angle) * shake_amount
            self.offset_y = math.sin(angle) * shake_amount
            
            if self.timer <= 0:
                self.offset_x = 0.0
                self.offset_y = 0.0
                self.timer = 0.0
                self.intensity = 0.0
    
    def get_offset(self) -> Tuple[float, float]:
        """
        Get current shake offset.
        
        Returns:
            (offset_x, offset_y) tuple
        """
        return (self.offset_x, self.offset_y)
    
    def is_shaking(self) -> bool:
        """Check if currently shaking."""
        return self.timer > 0

