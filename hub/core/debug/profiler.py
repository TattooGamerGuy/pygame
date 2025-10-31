"""Performance profiling - Modular."""

from typing import Dict, List
import time
import gc


class Profiler:
    """Performance profiler for FPS, frame time, and memory."""
    
    def __init__(self):
        """Initialize profiler."""
        self.frame_times: List[float] = []
        self.max_samples = 60
        self._frame_start = 0.0
        self._current_frame_time = 0.0
        self._fps = 0.0
        self._memory_usage = 0.0
    
    def start_frame(self) -> None:
        """Start profiling a frame."""
        self._frame_start = time.perf_counter()
    
    def end_frame(self) -> None:
        """End profiling a frame."""
        frame_time = time.perf_counter() - self._frame_start
        self._current_frame_time = frame_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
        
        # Calculate FPS
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self._fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        # Memory usage
        gc.collect()
        # Simple memory estimation (not precise)
        self._memory_usage = len(gc.get_objects())
    
    @property
    def fps(self) -> float:
        """Get current FPS."""
        return self._fps
    
    @property
    def frame_time(self) -> float:
        """Get current frame time in seconds."""
        return self._current_frame_time
    
    @property
    def frame_time_ms(self) -> float:
        """Get current frame time in milliseconds."""
        return self._current_frame_time * 1000.0
    
    @property
    def avg_frame_time(self) -> float:
        """Get average frame time in seconds."""
        if len(self.frame_times) == 0:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times)
    
    @property
    def memory_usage(self) -> int:
        """Get approximate memory usage (object count)."""
        return self._memory_usage
    
    def reset(self) -> None:
        """Reset profiling data."""
        self.frame_times.clear()
        self._fps = 0.0
        self._memory_usage = 0.0

