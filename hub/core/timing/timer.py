"""Game timers and stopwatches - Modular."""

from typing import Callable, Optional


class Timer:
    """Simple timer for delays, countdowns, and callbacks."""
    
    def __init__(self, duration: float, callback: Optional[Callable[[], None]] = None):
        """
        Initialize timer.
        
        Args:
            duration: Timer duration in seconds
            callback: Optional function to call when timer completes
        """
        self.duration = duration
        self.time_remaining = duration
        self.callback = callback
        self.running = False
        self.loop = False
    
    def start(self, loop: bool = False) -> None:
        """
        Start the timer.
        
        Args:
            loop: Whether to loop the timer
        """
        self.running = True
        self.loop = loop
        self.time_remaining = self.duration
    
    def stop(self) -> None:
        """Stop the timer."""
        self.running = False
    
    def reset(self) -> None:
        """Reset timer to initial duration."""
        self.time_remaining = self.duration
        self.running = False
    
    def update(self, dt: float) -> None:
        """
        Update timer.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.running:
            return
        
        self.time_remaining -= dt
        
        if self.time_remaining <= 0:
            if self.callback:
                self.callback()
            
            if self.loop:
                self.time_remaining = self.duration
            else:
                self.running = False
                self.time_remaining = 0.0
    
    @property
    def finished(self) -> bool:
        """Check if timer has finished."""
        return self.time_remaining <= 0 and not self.running
    
    @property
    def progress(self) -> float:
        """Get timer progress (0.0 to 1.0)."""
        if self.duration <= 0:
            return 1.0
        return max(0.0, min(1.0, 1.0 - (self.time_remaining / self.duration)))


class Stopwatch:
    """Stopwatch for measuring elapsed time."""
    
    def __init__(self):
        """Initialize stopwatch."""
        self.elapsed_time = 0.0
        self.running = False
    
    def start(self) -> None:
        """Start the stopwatch."""
        self.running = True
    
    def stop(self) -> None:
        """Stop the stopwatch."""
        self.running = False
    
    def reset(self) -> None:
        """Reset the stopwatch."""
        self.elapsed_time = 0.0
        self.running = False
    
    def update(self, dt: float) -> None:
        """
        Update stopwatch.
        
        Args:
            dt: Delta time in seconds
        """
        if self.running:
            self.elapsed_time += dt
    
    @property
    def time(self) -> float:
        """Get elapsed time."""
        return self.elapsed_time

