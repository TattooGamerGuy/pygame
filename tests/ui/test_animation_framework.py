"""
Tests for UI Animation Framework (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
These tests will initially fail until the animation framework is implemented.
"""

import pytest
import pygame
from typing import Callable
from hub.ui.animation import Easing, Tween, AnimationManager, AnimationState


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


class TestEasing:
    """Test easing functions."""
    
    def test_easing_linear(self, pygame_init_cleanup):
        """Test linear easing function."""
        # Linear should return value directly proportional to input
        assert Easing.linear(0.0) == pytest.approx(0.0)
        assert Easing.linear(0.5) == pytest.approx(0.5)
        assert Easing.linear(1.0) == pytest.approx(1.0)
    
    def test_easing_ease_in(self, pygame_init_cleanup):
        """Test ease-in easing function."""
        # Ease-in starts slow
        result_0 = Easing.ease_in(0.0)
        result_1 = Easing.ease_in(1.0)
        
        assert result_0 == pytest.approx(0.0)
        assert result_1 == pytest.approx(1.0)
        
        # Midpoint should be less than linear (0.5)
        result_mid = Easing.ease_in(0.5)
        assert result_mid < 0.5
    
    def test_easing_ease_out(self, pygame_init_cleanup):
        """Test ease-out easing function."""
        # Ease-out ends slow
        result_0 = Easing.ease_out(0.0)
        result_1 = Easing.ease_out(1.0)
        
        assert result_0 == pytest.approx(0.0)
        assert result_1 == pytest.approx(1.0)
        
        # Midpoint should be greater than linear (0.5)
        result_mid = Easing.ease_out(0.5)
        assert result_mid > 0.5
    
    def test_easing_ease_in_out(self, pygame_init_cleanup):
        """Test ease-in-out easing function."""
        result_0 = Easing.ease_in_out(0.0)
        result_1 = Easing.ease_in_out(1.0)
        
        assert result_0 == pytest.approx(0.0)
        assert result_1 == pytest.approx(1.0)
        
        # Midpoint should be approximately 0.5
        result_mid = Easing.ease_in_out(0.5)
        assert result_mid == pytest.approx(0.5, abs=0.1)
    
    def test_easing_bounce(self, pygame_init_cleanup):
        """Test bounce easing function."""
        result_0 = Easing.bounce(0.0)
        result_1 = Easing.bounce(1.0)
        
        assert result_0 == pytest.approx(0.0)
        assert result_1 == pytest.approx(1.0)
        
        # Bounce may exceed 1.0 at certain points
        result_08 = Easing.bounce(0.8)
        assert result_08 >= 0.0
    
    def test_easing_elastic(self, pygame_init_cleanup):
        """Test elastic easing function."""
        result_0 = Easing.elastic(0.0)
        result_1 = Easing.elastic(1.0)
        
        assert result_0 == pytest.approx(0.0)
        assert result_1 == pytest.approx(1.0)
        
        # Elastic may exceed 1.0 or go below 0.0 during oscillation
        result_05 = Easing.elastic(0.5)
        assert isinstance(result_05, (int, float))


class TestTween:
    """Test Tween class for animating values."""
    
    def test_tween_initialization(self, pygame_init_cleanup):
        """Test Tween initialization."""
        tween = Tween(
            start_value=0.0,
            end_value=100.0,
            duration=1.0,
            easing=Easing.linear
        )
        
        assert tween.start_value == 0.0
        assert tween.end_value == 100.0
        assert tween.duration == 1.0
        assert tween.easing == Easing.linear
        assert tween.state == AnimationState.PENDING
    
    def test_tween_start(self, pygame_init_cleanup):
        """Test starting a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        
        assert tween.state == AnimationState.RUNNING
        assert tween.current_value == pytest.approx(0.0)
    
    def test_tween_update(self, pygame_init_cleanup):
        """Test updating a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        
        # Update halfway through
        tween.update(0.5)
        assert tween.current_value == pytest.approx(50.0)
        assert tween.state == AnimationState.RUNNING
        
        # Update to completion
        tween.update(0.5)
        assert tween.current_value == pytest.approx(100.0)
        assert tween.state == AnimationState.COMPLETED
    
    def test_tween_completion_callback(self, pygame_init_cleanup):
        """Test tween completion callback."""
        callback_called = [False]
        
        def on_complete():
            callback_called[0] = True
        
        tween = Tween(0.0, 100.0, 1.0, Easing.linear, on_complete=on_complete)
        tween.start()
        tween.update(1.0)
        
        assert callback_called[0]
    
    def test_tween_pause_resume(self, pygame_init_cleanup):
        """Test pausing and resuming a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        tween.update(0.3)
        
        value_before_pause = tween.current_value
        
        tween.pause()
        assert tween.state == AnimationState.PAUSED
        
        # Value should not change when paused
        tween.update(0.2)
        assert tween.current_value == pytest.approx(value_before_pause)
        
        # Resume
        tween.resume()
        assert tween.state == AnimationState.RUNNING
        tween.update(0.3)
        assert tween.current_value > value_before_pause
    
    def test_tween_stop(self, pygame_init_cleanup):
        """Test stopping a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        tween.update(0.5)
        
        tween.stop()
        assert tween.state == AnimationState.STOPPED
    
    def test_tween_reset(self, pygame_init_cleanup):
        """Test resetting a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        tween.update(0.5)
        
        tween.reset()
        assert tween.state == AnimationState.PENDING
        assert tween.current_value == pytest.approx(0.0)
    
    def test_tween_easing_applied(self, pygame_init_cleanup):
        """Test that easing function is applied correctly."""
        tween = Tween(0.0, 100.0, 1.0, Easing.ease_in)
        tween.start()
        tween.update(0.5)
        
        # With ease-in, value at 0.5 should be less than 50 (linear)
        assert tween.current_value < 50.0
        assert tween.current_value > 0.0
    
    def test_tween_reverse(self, pygame_init_cleanup):
        """Test reversing a tween."""
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        tween.update(1.0)  # Complete forward
        
        tween.reverse()
        assert tween.state == AnimationState.RUNNING
        assert tween.start_value == 100.0
        assert tween.end_value == 0.0
        
        tween.update(1.0)
        assert tween.current_value == pytest.approx(0.0)
    
    def test_tween_loop(self, pygame_init_cleanup):
        """Test looping a tween."""
        callback_count = [0]
        
        def on_complete():
            callback_count[0] += 1
        
        tween = Tween(0.0, 100.0, 1.0, Easing.linear, on_complete=on_complete, loop=True)
        tween.start()
        
        # First loop
        tween.update(1.0)
        assert callback_count[0] == 1
        assert tween.state == AnimationState.RUNNING  # Should continue running
        
        # Second loop
        tween.update(1.0)
        assert callback_count[0] == 2


class TestAnimationManager:
    """Test AnimationManager for centralized animation management."""
    
    def test_animation_manager_initialization(self, pygame_init_cleanup):
        """Test AnimationManager initialization."""
        manager = AnimationManager()
        assert len(manager.get_active_animations()) == 0
    
    def test_animation_manager_add_tween(self, pygame_init_cleanup):
        """Test adding a tween to the manager."""
        manager = AnimationManager()
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        
        manager.add(tween)
        
        active = manager.get_active_animations()
        assert len(active) == 1
        assert tween in active
    
    def test_animation_manager_update(self, pygame_init_cleanup):
        """Test updating all animations."""
        manager = AnimationManager()
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        manager.add(tween)
        
        manager.update(0.5)
        assert tween.current_value == pytest.approx(50.0)
        
        manager.update(0.5)
        assert tween.current_value == pytest.approx(100.0)
        assert len(manager.get_active_animations()) == 0  # Completed animations removed
    
    def test_animation_manager_remove_completed(self, pygame_init_cleanup):
        """Test that completed animations are automatically removed."""
        manager = AnimationManager()
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        manager.add(tween)
        
        assert len(manager.get_active_animations()) == 1
        manager.update(1.0)
        assert len(manager.get_active_animations()) == 0
    
    def test_animation_manager_multiple_animations(self, pygame_init_cleanup):
        """Test managing multiple animations simultaneously."""
        manager = AnimationManager()
        
        tween1 = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween1.start()
        manager.add(tween1)
        
        tween2 = Tween(0.0, 200.0, 2.0, Easing.linear)
        tween2.start()
        manager.add(tween2)
        
        assert len(manager.get_active_animations()) == 2
        
        manager.update(1.0)
        assert len(manager.get_active_animations()) == 1  # tween1 completed
        assert tween2.current_value == pytest.approx(100.0)
        
        manager.update(1.0)
        assert len(manager.get_active_animations()) == 0  # tween2 completed
    
    def test_animation_manager_clear(self, pygame_init_cleanup):
        """Test clearing all animations."""
        manager = AnimationManager()
        tween1 = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween2 = Tween(0.0, 200.0, 1.0, Easing.linear)
        manager.add(tween1)
        manager.add(tween2)
        
        assert len(manager.get_active_animations()) == 2
        manager.clear()
        assert len(manager.get_active_animations()) == 0
    
    def test_animation_manager_pause_all(self, pygame_init_cleanup):
        """Test pausing all animations."""
        manager = AnimationManager()
        tween1 = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween2 = Tween(0.0, 200.0, 1.0, Easing.linear)
        tween1.start()
        tween2.start()
        manager.add(tween1)
        manager.add(tween2)
        
        manager.update(0.3)
        value1 = tween1.current_value
        value2 = tween2.current_value
        
        manager.pause_all()
        manager.update(0.2)  # Should not advance
        
        assert tween1.current_value == pytest.approx(value1)
        assert tween2.current_value == pytest.approx(value2)
    
    def test_animation_manager_resume_all(self, pygame_init_cleanup):
        """Test resuming all paused animations."""
        manager = AnimationManager()
        tween = Tween(0.0, 100.0, 1.0, Easing.linear)
        tween.start()
        manager.add(tween)
        
        manager.update(0.3)
        manager.pause_all()
        manager.resume_all()
        
        assert tween.state == AnimationState.RUNNING
        manager.update(0.2)
        assert tween.current_value > 30.0  # Should have advanced


class TestAnimationIntegration:
    """Integration tests for animation system."""
    
    def test_widget_position_animation(self, pygame_init_cleanup):
        """Test animating widget position."""
        # Use a simple object to simulate widget position
        class MockWidget:
            def __init__(self):
                self.x = 0
        
        widget = MockWidget()
        
        manager = AnimationManager()
        
        # Animate X position from 0 to 500
        x_tween = Tween(0.0, 500.0, 1.0, Easing.ease_in_out)
        
        def update_x(value):
            widget.x = int(value)
        
        x_tween.on_update = update_x
        x_tween.start()
        manager.add(x_tween)
        
        manager.update(1.0)
        assert widget.x == 500
    
    def test_widget_fade_animation(self, pygame_init_cleanup):
        """Test animating widget opacity (fade in/out)."""
        # This test defines expected opacity animation behavior
        opacity = 0.0  # Fully transparent
        
        manager = AnimationManager()
        
        fade_tween = Tween(0.0, 1.0, 0.5, Easing.ease_in)
        
        def update_opacity(value):
            nonlocal opacity
            opacity = value
        
        fade_tween.on_update = update_opacity
        fade_tween.start()
        manager.add(fade_tween)
        
        manager.update(0.5)
        assert opacity == pytest.approx(1.0)
    
    def test_sequential_animations(self, pygame_init_cleanup):
        """Test chaining animations sequentially."""
        manager = AnimationManager()
        values = [0.0]
        
        def update_value(value):
            values[0] = value
        
        # First animation
        tween1 = Tween(0.0, 50.0, 0.5, Easing.linear)
        tween1.on_update = update_value
        tween1.start()
        manager.add(tween1)
        
        # Start second animation when first completes
        def start_tween2():
            tween2 = Tween(50.0, 100.0, 0.5, Easing.linear)
            tween2.on_update = update_value
            tween2.start()
            manager.add(tween2)
        
        tween1.on_complete = start_tween2
        
        manager.update(0.5)  # Complete first
        assert values[0] == pytest.approx(50.0)
        
        manager.update(0.5)  # Complete second
        assert values[0] == pytest.approx(100.0)


@pytest.mark.performance
class TestAnimationPerformance:
    """Performance tests for animation system."""
    
    def test_animation_manager_performance(self, pygame_init_cleanup):
        """Test AnimationManager performance with many animations."""
        import time
        
        manager = AnimationManager()
        
        # Create 100 animations
        for i in range(100):
            tween = Tween(0.0, 100.0, 1.0, Easing.linear)
            tween.start()
            manager.add(tween)
        
        start = time.time()
        manager.update(0.016)  # One frame at 60 FPS
        elapsed = time.time() - start
        
        # Should be fast enough for 60 FPS
        assert elapsed < 0.01  # Less than 10ms for 100 animations

