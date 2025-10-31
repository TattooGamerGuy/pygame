"""Fixed timestep physics loop - Modular."""

from typing import Callable, Optional


class FixedTimestep:
    """Manages fixed timestep update loop for physics."""
    
    def __init__(self, target_fps: int = 60, max_frame_time: float = 0.25):
        """
        Initialize fixed timestep.
        
        Args:
            target_fps: Target physics update rate
            max_frame_time: Maximum frame time to prevent spiral of death
        """
        self.target_fps = target_fps
        self.fixed_dt = 1.0 / target_fps
        self.max_frame_time = max_frame_time
        self.accumulator = 0.0
    
    def update(
        self,
        frame_time: float,
        fixed_update: Callable[[float], None],
        variable_update: Optional[Callable[[float], None]] = None
    ) -> None:
        """
        Update fixed timestep loop.
        
        Args:
            frame_time: Current frame delta time
            fixed_update: Function to call for fixed updates
            variable_update: Optional function for variable timestep updates
        """
        frame_time = min(frame_time, self.max_frame_time)
        self.accumulator += frame_time
        
        # Run variable update (rendering, etc.)
        if variable_update:
            variable_update(frame_time)
        
        # Run fixed updates (physics, etc.)
        while self.accumulator >= self.fixed_dt:
            fixed_update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
    
    def reset(self) -> None:
        """Reset accumulator."""
        self.accumulator = 0.0
    
    @property
    def fixed_delta_time(self) -> float:
        """Get fixed timestep delta time."""
        return self.fixed_dt

