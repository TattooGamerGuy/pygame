"""Pytest configuration and fixtures for game tests."""

import pytest
import pygame
from typing import Generator, Tuple, Dict


@pytest.fixture(scope="session")
def pygame_init():
    """Initialize pygame once for all tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_surface():
    """Create a mock pygame surface for rendering tests."""
    pygame.init()
    surface = pygame.Surface((800, 600))
    yield surface
    pygame.quit()


@pytest.fixture
def mock_display():
    """Mock display manager."""
    pygame.init()
    display = pygame.display.set_mode((800, 600))
    yield display
    pygame.quit()


# ============================================================================
# Mobile Device Fixtures
# ============================================================================

@pytest.fixture
def desktop_resolution() -> Tuple[int, int]:
    """Standard desktop resolution."""
    return (1280, 720)


@pytest.fixture
def mobile_resolutions() -> Dict[str, Tuple[int, int]]:
    """
    Mobile device resolution presets for testing.
    
    Covers various mobile devices with different screen sizes and aspect ratios.
    """
    return {
        'iphone_se': (320, 568),      # iPhone SE (first gen) - ~16:9
        'iphone_12': (390, 844),      # iPhone 12/13 - ~19.5:9
        'iphone_12_pro_max': (428, 926),  # iPhone 12/13 Pro Max - ~19.5:9
        'ipad': (768, 1024),          # iPad (portrait) - 4:3
        'android_small': (360, 640),  # Small Android device - ~16:9
        'android_medium': (412, 732),  # Medium Android device - ~16:9
        'android_large': (600, 960),   # Large Android device - ~16:10
    }


@pytest.fixture
def mobile_fps_targets() -> Dict[str, int]:
    """Mobile FPS target configurations for performance testing."""
    return {
        'low_end': 30,      # Low-end devices target 30 FPS
        'mid_range': 45,    # Mid-range devices target 45 FPS
        'high_end': 60,     # High-end devices target 60 FPS
    }


@pytest.fixture
def mobile_memory_limits() -> Dict[str, int]:
    """
    Mobile memory constraint configurations (in MB).
    
    These represent realistic memory constraints for mobile devices.
    """
    return {
        'very_low': 16,    # Very low-end device (16MB limit)
        'low': 32,         # Low-end device (32MB limit)
        'medium': 64,      # Medium device (64MB limit)
        'high': 128,       # High-end device (128MB limit)
    }


# ============================================================================
# Performance Monitoring Fixtures
# ============================================================================

@pytest.fixture
def performance_monitor():
    """
    Performance monitoring fixture for tracking frame times and FPS.
    
    Usage:
        with performance_monitor:
            # Code to monitor
            pass
        assert performance_monitor.avg_frame_time < 0.017  # 60 FPS target
    """
    class PerformanceMonitor:
        def __init__(self):
            self.frame_times = []
            self.fps_samples = []
            
        def record_frame_time(self, frame_time: float):
            """Record a frame time sample."""
            self.frame_times.append(frame_time)
            
        def record_fps(self, fps: float):
            """Record an FPS sample."""
            self.fps_samples.append(fps)
            
        @property
        def avg_frame_time(self) -> float:
            """Get average frame time in seconds."""
            if not self.frame_times:
                return 0.0
            return sum(self.frame_times) / len(self.frame_times)
            
        @property
        def avg_fps(self) -> float:
            """Get average FPS."""
            if not self.fps_samples:
                return 0.0
            return sum(self.fps_samples) / len(self.fps_samples)
            
        @property
        def min_fps(self) -> float:
            """Get minimum FPS recorded."""
            return min(self.fps_samples) if self.fps_samples else 0.0
            
        def reset(self):
            """Reset all recorded data."""
            self.frame_times.clear()
            self.fps_samples.clear()
            
        def __enter__(self):
            self.reset()
            return self
            
        def __exit__(self, *args):
            pass
    
    return PerformanceMonitor()


@pytest.fixture
def memory_tracker():
    """
    Memory tracking fixture for monitoring memory usage.
    
    Usage:
        with memory_tracker:
            # Code to track
            pass
        assert memory_tracker.peak_usage < 32 * 1024 * 1024  # 32MB limit
    """
    import sys
    
    class MemoryTracker:
        def __init__(self):
            self.samples = []
            
        def sample(self):
            """Take a memory usage sample."""
            # Note: This is a simplified memory tracking
            # For accurate tracking, use memory_profiler or similar
            import gc
            gc.collect()
            # Approximate memory usage (this is simplified)
            self.samples.append(sum(sys.getsizeof(obj) for obj in gc.get_objects()[:1000]))
            
        @property
        def peak_usage(self) -> int:
            """Get peak memory usage in bytes."""
            return max(self.samples) if self.samples else 0
            
        @property
        def avg_usage(self) -> float:
            """Get average memory usage in bytes."""
            if not self.samples:
                return 0.0
            return sum(self.samples) / len(self.samples)
            
        def reset(self):
            """Reset all recorded data."""
            self.samples.clear()
            
        def __enter__(self):
            self.reset()
            return self
            
        def __exit__(self, *args):
            pass
    
    return MemoryTracker()


# ============================================================================
# Touch Event Simulation Helpers
# ============================================================================

@pytest.fixture
def touch_event_simulator():
    """
    Touch event simulator for testing touch input.
    
    Usage:
        simulator = touch_event_simulator
        events = simulator.create_tap_event(100, 200)
        # Use events in input handling tests
    """
    class TouchEventSimulator:
        """Helper class for creating touch events."""
        
        @staticmethod
        def create_tap_event(x: int, y: int, finger_id: int = 0) -> pygame.event.Event:
            """Create a touch tap event."""
            # Note: pygame may not support touch events on all platforms
            # This is a placeholder for the pattern
            return pygame.event.Event(
                pygame.FINGERDOWN,
                {"x": x, "y": y, "finger_id": finger_id}
            )
        
        @staticmethod
        def create_touch_down(x: int, y: int, finger_id: int = 0) -> pygame.event.Event:
            """Create a touch down event."""
            return pygame.event.Event(
                pygame.FINGERDOWN,
                {"x": x, "y": y, "finger_id": finger_id}
            )
        
        @staticmethod
        def create_touch_up(x: int, y: int, finger_id: int = 0) -> pygame.event.Event:
            """Create a touch up event."""
            return pygame.event.Event(
                pygame.FINGERUP,
                {"x": x, "y": y, "finger_id": finger_id}
            )
        
        @staticmethod
        def create_touch_motion(x: int, y: int, dx: float, dy: float, finger_id: int = 0) -> pygame.event.Event:
            """Create a touch motion event."""
            return pygame.event.Event(
                pygame.FINGERMOTION,
                {"x": x, "y": y, "dx": dx, "dy": dy, "finger_id": finger_id}
            )
        
        @staticmethod
        def create_multi_touch_events(positions: list) -> list:
            """Create multiple touch events for multi-touch testing."""
            events = []
            for i, (x, y) in enumerate(positions):
                events.append(TouchEventSimulator.create_touch_down(x, y, i))
            return events
    
    return TouchEventSimulator()


# ============================================================================
# Common System Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """
    Initialize and cleanup pygame for each test.
    
    Ensures clean state between tests and proper resource cleanup.
    """
    pygame.init()
    yield
    pygame.quit()

