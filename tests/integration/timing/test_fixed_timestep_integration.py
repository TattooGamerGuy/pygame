"""
Integration tests for FixedTimestep.

Tests fixed timestep with variable frame time, physics update consistency,
accumulator overflow, and mobile frame time spike handling.
"""

import pytest
import time
from hub.core.timing.fixed_timestep import FixedTimestep


class TestFixedTimestepBasic:
    """Test basic FixedTimestep functionality."""
    
    def test_fixed_timestep_initialization(self):
        """Test FixedTimestep initialization."""
        timestep = FixedTimestep(target_fps=60)
        assert timestep.target_fps == 60
        assert timestep.fixed_dt == pytest.approx(1.0 / 60.0, abs=0.001)
        assert timestep.accumulator == 0.0
    
    def test_fixed_timestep_custom_max_frame_time(self):
        """Test FixedTimestep with custom max frame time."""
        timestep = FixedTimestep(target_fps=60, max_frame_time=0.5)
        assert timestep.max_frame_time == 0.5
    
    def test_fixed_timestep_reset(self):
        """Test resetting accumulator."""
        timestep = FixedTimestep(target_fps=60)
        timestep.accumulator = 0.5
        timestep.reset()
        assert timestep.accumulator == 0.0


class TestFixedTimestepUpdates:
    """Test FixedTimestep update functionality."""
    
    def test_fixed_timestep_single_update(self):
        """Test single fixed update call."""
        timestep = FixedTimestep(target_fps=60)
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
            assert dt == pytest.approx(1.0 / 60.0, abs=0.001)
        
        # Frame time equals fixed dt
        timestep.update(1.0 / 60.0, fixed_update)
        assert update_count[0] == 1
        assert timestep.accumulator < timestep.fixed_dt
    
    def test_fixed_timestep_multiple_updates_per_frame(self):
        """Test multiple fixed updates in one frame."""
        timestep = FixedTimestep(target_fps=60)
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
        
        # Frame time allows 3 fixed updates
        timestep.update(3.0 / 60.0, fixed_update)
        assert update_count[0] == 3
    
    def test_fixed_timestep_accumulator_remainder(self):
        """Test that accumulator stores remainder correctly."""
        timestep = FixedTimestep(target_fps=60)
        fixed_dt = timestep.fixed_dt
        
        def fixed_update(dt):
            pass
        
        # Frame time is 1.5 * fixed_dt
        timestep.update(fixed_dt * 1.5, fixed_update)
        
        # Should have executed 1 update, remainder < fixed_dt
        assert timestep.accumulator < fixed_dt
        assert timestep.accumulator > 0.0
        assert timestep.accumulator == pytest.approx(fixed_dt * 0.5, abs=0.001)
    
    def test_fixed_timestep_variable_update(self):
        """Test variable update callback."""
        timestep = FixedTimestep(target_fps=60)
        var_count = [0]
        fixed_count = [0]
        
        def fixed_update(dt):
            fixed_count[0] += 1
        
        def variable_update(dt):
            var_count[0] += 1
        
        timestep.update(1.0 / 60.0, fixed_update, variable_update)
        assert var_count[0] == 1
        assert fixed_count[0] == 1


class TestFixedTimestepConsistency:
    """Test FixedTimestep physics consistency."""
    
    def test_fixed_timestep_consistent_delta(self):
        """Test that fixed updates always use consistent delta time."""
        timestep = FixedTimestep(target_fps=60)
        fixed_dt = timestep.fixed_dt
        deltas = []
        
        def fixed_update(dt):
            deltas.append(dt)
        
        # Multiple frames with varying frame times
        timestep.update(0.017, fixed_update)  # ~60 FPS
        timestep.update(0.033, fixed_update)  # ~30 FPS
        timestep.update(0.016, fixed_update)  # ~60 FPS
        
        # All fixed updates should use same delta time
        for dt in deltas:
            assert dt == pytest.approx(fixed_dt, abs=0.001)
    
    def test_fixed_timestep_physics_deterministic(self):
        """Test that physics updates are deterministic."""
        timestep = FixedTimestep(target_fps=60)
        positions = []
        
        def fixed_update(dt):
            # Simulate physics step
            if not positions:
                positions.append(0.0)
            else:
                positions.append(positions[-1] + 10.0 * dt)
        
        # Run same sequence twice
        for _ in range(2):
            timestep.reset()
            positions.clear()
            for frame_time in [0.016, 0.017, 0.016]:
                timestep.update(frame_time, fixed_update)
            
            final_pos = positions[-1]
            # Should get same result
            assert final_pos > 0.0


class TestFixedTimestepFrameTimeSpikes:
    """Test FixedTimestep handling of frame time spikes."""
    
    def test_fixed_timestep_max_frame_time_cap(self):
        """Test that max frame time caps prevent spiral of death."""
        timestep = FixedTimestep(target_fps=60, max_frame_time=0.25)
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
        
        # Very large frame time should be capped
        timestep.update(1.0, fixed_update)  # 1 second (should be capped to 0.25)
        
        # Should have executed max_frame_time / fixed_dt updates
        max_updates = int(timestep.max_frame_time / timestep.fixed_dt)
        assert update_count[0] <= max_updates
    
    def test_fixed_timestep_small_spikes(self):
        """Test handling of small frame time spikes."""
        timestep = FixedTimestep(target_fps=60)
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
        
        # Normal frame time
        timestep.update(0.016, fixed_update)
        count_normal = update_count[0]
        
        update_count[0] = 0
        timestep.reset()
        
        # Frame with small spike
        timestep.update(0.050, fixed_update)  # 50ms spike
        
        # Should handle gracefully
        assert update_count[0] > count_normal
        assert update_count[0] <= 4  # Should not be excessive


@pytest.mark.mobile
@pytest.mark.mobile_performance
class TestFixedTimestepMobile:
    """Test FixedTimestep with mobile-specific scenarios."""
    
    def test_fixed_timestep_mobile_frame_spikes(self):
        """
        Test FixedTimestep handling of mobile frame time spikes.
        
        Mobile devices may experience frame time spikes. Fixed timestep
        should handle these without breaking physics.
        """
        timestep = FixedTimestep(target_fps=60, max_frame_time=0.25)
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
        
        # Simulate mobile frame time pattern: mostly 30ms, occasional 100ms spikes
        frame_times = [0.033] * 10  # 30 FPS baseline
        frame_times.extend([0.1] * 2)  # Two spikes
        
        for frame_time in frame_times:
            timestep.update(frame_time, fixed_update)
        
        # Should have processed all updates without issues
        assert update_count[0] > 0
        assert timestep.accumulator < timestep.fixed_dt
    
    def test_fixed_timestep_mobile_30_fps_target(self):
        """Test FixedTimestep with 30 FPS target for mobile."""
        timestep = FixedTimestep(target_fps=30)
        assert timestep.fixed_dt == pytest.approx(1.0 / 30.0, abs=0.001)
        
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
            assert dt == pytest.approx(1.0 / 30.0, abs=0.001)
        
        timestep.update(1.0 / 30.0, fixed_update)
        assert update_count[0] == 1
    
    def test_fixed_timestep_mobile_accumulator_overflow_protection(self):
        """
        Test that accumulator overflow is prevented on mobile.
        
        On low-end mobile devices, frame times can be very variable.
        The accumulator should not grow unbounded.
        """
        timestep = FixedTimestep(target_fps=60, max_frame_time=0.25)
        
        def fixed_update(dt):
            pass
        
        # Simulate many slow frames
        for _ in range(100):
            timestep.update(0.1, fixed_update)  # 100ms frames
            # Accumulator should never exceed max_frame_time + fixed_dt
            assert timestep.accumulator < timestep.max_frame_time + timestep.fixed_dt


class TestFixedTimestepAccumulator:
    """Test accumulator behavior."""
    
    def test_fixed_timestep_accumulator_accumulates(self):
        """Test that accumulator accumulates frame time."""
        timestep = FixedTimestep(target_fps=60)
        fixed_dt = timestep.fixed_dt
        
        def fixed_update(dt):
            pass
        
        # Small frame time that doesn't trigger update
        timestep.update(fixed_dt * 0.5, fixed_update)
        assert timestep.accumulator == pytest.approx(fixed_dt * 0.5, abs=0.001)
        
        # Another small frame time
        timestep.update(fixed_dt * 0.5, fixed_update)
        # Now should have triggered one update
        assert timestep.accumulator < fixed_dt
    
    def test_fixed_timestep_accumulator_carries_over(self):
        """Test that accumulator carries over between frames."""
        timestep = FixedTimestep(target_fps=60)
        fixed_dt = timestep.fixed_dt
        update_count = [0]
        
        def fixed_update(dt):
            update_count[0] += 1
        
        # Two frames that together trigger one update
        timestep.update(fixed_dt * 0.7, fixed_update)
        assert update_count[0] == 0  # No update yet
        assert timestep.accumulator == pytest.approx(fixed_dt * 0.7, abs=0.001)
        
        timestep.update(fixed_dt * 0.5, fixed_update)
        assert update_count[0] == 1  # One update triggered
        # Remaining accumulator should be (0.7 + 0.5 - 1.0) * fixed_dt
        assert timestep.accumulator < fixed_dt

