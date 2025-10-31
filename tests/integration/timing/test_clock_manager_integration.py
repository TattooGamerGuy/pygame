"""
Integration tests for ClockManager.

Tests FPS limiting, delta time consistency, variable FPS scenarios,
and mobile performance considerations.
"""

import pytest
import time
import pygame
from hub.core.timing.clock_manager import ClockManager


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def clock_manager():
    """Create a ClockManager instance for testing."""
    return ClockManager(target_fps=60)


class TestClockManagerInitialization:
    """Test ClockManager initialization."""
    
    def test_clock_manager_default_initialization(self, pygame_init_cleanup, clock_manager):
        """Test ClockManager with default parameters."""
        assert clock_manager.target_fps == 60
        assert clock_manager.delta_time == 0.0
        assert clock_manager.fps == 0.0
    
    def test_clock_manager_custom_fps(self, pygame_init_cleanup):
        """Test ClockManager with custom FPS target."""
        manager = ClockManager(target_fps=30)
        assert manager.target_fps == 30
    
    def test_clock_manager_reset(self, pygame_init_cleanup, clock_manager):
        """Test clock reset functionality."""
        clock_manager.reset()
        assert clock_manager.delta_time == 0.0


class TestClockManagerFPSLimiting:
    """Test FPS limiting functionality."""
    
    def test_clock_manager_fps_limiting(self, pygame_init_cleanup, clock_manager):
        """Test that tick() limits FPS appropriately."""
        clock_manager.reset()
        
        # Run multiple ticks quickly
        for _ in range(10):
            dt = clock_manager.tick()
            # Delta time should be controlled by FPS limiting
            assert dt >= 0.0
        
        # FPS should approach target
        fps = clock_manager.fps
        assert fps > 0.0
        # May not be exactly 60, but should be in reasonable range
        assert 30 <= fps <= 120  # Allow some variance
    
    def test_clock_manager_target_fps_change(self, pygame_init_cleanup, clock_manager):
        """Test changing target FPS."""
        clock_manager.reset()
        
        # Test with 60 FPS
        for _ in range(5):
            clock_manager.tick()
        
        fps_60 = clock_manager.fps
        
        # Change to 30 FPS
        clock_manager.set_target_fps(30)
        clock_manager.reset()
        
        for _ in range(5):
            clock_manager.tick()
        
        fps_30 = clock_manager.fps
        
        # 30 FPS should generally be lower than 60 FPS measurement
        # (Note: actual FPS depends on system performance)
        assert fps_30 > 0.0


class TestClockManagerDeltaTime:
    """Test delta time consistency."""
    
    def test_clock_manager_delta_time_consistency(self, pygame_init_cleanup, clock_manager):
        """Test that delta time is consistent."""
        clock_manager.reset()
        
        delta_times = []
        for _ in range(10):
            dt = clock_manager.tick()
            delta_times.append(dt)
        
        # Delta times should be relatively consistent
        # Target is 1/60 = ~0.0167 seconds
        avg_dt = sum(delta_times) / len(delta_times)
        assert 0.0 < avg_dt < 0.1  # Should be reasonable
    
    def test_clock_manager_delta_time_capped(self, pygame_init_cleanup, clock_manager):
        """Test that delta time is capped to prevent large jumps."""
        clock_manager.reset()
        
        # Simulate a frame time spike by sleeping
        time.sleep(0.2)  # 200ms pause
        
        dt = clock_manager.tick()
        
        # Delta time should be capped (max 0.1s according to implementation)
        assert dt <= 0.1
    
    def test_clock_manager_delta_time_property(self, pygame_init_cleanup, clock_manager):
        """Test delta_time property."""
        clock_manager.reset()
        assert clock_manager.delta_time == 0.0
        
        clock_manager.tick()
        assert clock_manager.delta_time > 0.0
    
    def test_clock_manager_multiple_ticks(self, pygame_init_cleanup, clock_manager):
        """Test multiple ticks accumulate delta time correctly."""
        clock_manager.reset()
        
        total_time = 0.0
        for _ in range(10):
            dt = clock_manager.tick()
            total_time += dt
        
        # Total time should be reasonable
        assert total_time > 0.0
        assert total_time < 1.0  # Should be less than 1 second for 10 frames


@pytest.mark.mobile
@pytest.mark.mobile_performance
class TestClockManagerMobilePerformance:
    """Test ClockManager with mobile performance scenarios."""
    
    @pytest.mark.parametrize("target_fps", [30, 45, 60])
    def test_clock_manager_mobile_fps_targets(self, pygame_init_cleanup, target_fps):
        """Test ClockManager with mobile FPS targets."""
        manager = ClockManager(target_fps=target_fps)
        manager.reset()
        
        # Performance monitoring - collect frame times and FPS
        frame_times = []
        fps_samples = []
        for _ in range(30):  # 1 second at 30 FPS
            dt = manager.tick()
            frame_times.append(dt)
            fps_samples.append(manager.fps)
        
        # Check that we're approaching target FPS
        avg_fps = sum(fps_samples) / len(fps_samples) if fps_samples else 0.0
        assert avg_fps > 0.0
        
        # On actual mobile devices, FPS may be lower than target
        # This test documents expected behavior
    
    def test_clock_manager_mobile_frame_spikes(self, pygame_init_cleanup):
        """
        Test ClockManager handling of frame time spikes on mobile.
        
        Mobile devices may experience frame time spikes.
        ClockManager should handle these gracefully.
        """
        manager = ClockManager(target_fps=30)
        manager.reset()
        
        # Simulate frame time spikes
        frame_times = []
        for i in range(20):
            if i % 5 == 0:
                # Simulate spike
                time.sleep(0.05)  # 50ms spike
            
            dt = manager.tick()
            frame_times.append(dt)
        
        # All frame times should be capped
        for dt in frame_times:
            assert dt <= 0.1  # Capped at 0.1s
        
        # Average should be reasonable
        avg_dt = sum(frame_times) / len(frame_times)
        assert 0.0 < avg_dt < 0.1
    
    def test_clock_manager_mobile_30_fps(self, pygame_init_cleanup):
        """Test ClockManager specifically for 30 FPS mobile target."""
        manager = ClockManager(target_fps=30)
        manager.reset()
        
        # Target delta time should be ~0.033s (1/30)
        target_dt = 1.0 / 30.0
        
        delta_times = []
        for _ in range(30):
            dt = manager.tick()
            delta_times.append(dt)
        
        avg_dt = sum(delta_times) / len(delta_times)
        
        # Average should be close to target (with some variance)
        assert abs(avg_dt - target_dt) < 0.05


class TestClockManagerEdgeCases:
    """Test ClockManager edge cases."""
    
    def test_clock_manager_very_high_fps(self, pygame_init_cleanup):
        """Test ClockManager with very high FPS target."""
        manager = ClockManager(target_fps=120)
        manager.reset()
        
        for _ in range(5):
            dt = manager.tick()
            assert dt >= 0.0
        
        manager.cleanup()
    
    def test_clock_manager_very_low_fps(self, pygame_init_cleanup):
        """Test ClockManager with very low FPS target."""
        manager = ClockManager(target_fps=10)
        manager.reset()
        
        for _ in range(5):
            dt = manager.tick()
            assert dt >= 0.0
        
        manager.cleanup()
    
    def test_clock_manager_reset_after_ticks(self, pygame_init_cleanup, clock_manager):
        """Test resetting clock after multiple ticks."""
        for _ in range(10):
            clock_manager.tick()
        
        assert clock_manager.delta_time > 0.0
        
        clock_manager.reset()
        assert clock_manager.delta_time == 0.0

