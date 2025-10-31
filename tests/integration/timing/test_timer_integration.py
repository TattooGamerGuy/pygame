"""
Integration tests for Timer and Stopwatch.

Tests timer countdown, callbacks, loops, and multiple timers.
"""

import pytest
import time
from hub.core.timing.timer import Timer, Stopwatch


class TestTimerBasic:
    """Test basic Timer functionality."""
    
    def test_timer_initialization(self):
        """Test Timer initialization."""
        timer = Timer(duration=5.0)
        assert timer.duration == 5.0
        assert timer.time_remaining == 5.0
        assert not timer.running
        assert not timer.loop
    
    def test_timer_with_callback(self):
        """Test Timer with callback function."""
        callback_called = [False]
        
        def callback():
            callback_called[0] = True
        
        timer = Timer(duration=1.0, callback=callback)
        assert timer.callback is not None
    
    def test_timer_start(self):
        """Test starting a timer."""
        timer = Timer(duration=5.0)
        timer.start()
        assert timer.running
        assert timer.time_remaining == 5.0
    
    def test_timer_start_with_loop(self):
        """Test starting a timer with loop."""
        timer = Timer(duration=5.0)
        timer.start(loop=True)
        assert timer.running
        assert timer.loop
    
    def test_timer_stop(self):
        """Test stopping a timer."""
        timer = Timer(duration=5.0)
        timer.start()
        timer.stop()
        assert not timer.running
    
    def test_timer_reset(self):
        """Test resetting a timer."""
        timer = Timer(duration=5.0)
        timer.start()
        timer.update(2.0)
        timer.reset()
        assert not timer.running
        assert timer.time_remaining == 5.0


class TestTimerCountdown:
    """Test timer countdown functionality."""
    
    def test_timer_countdown(self):
        """Test timer counts down correctly."""
        timer = Timer(duration=10.0)
        timer.start()
        
        timer.update(2.0)
        assert timer.time_remaining == 8.0
        
        timer.update(3.0)
        assert timer.time_remaining == 5.0
    
    def test_timer_finishes(self):
        """Test timer finishes correctly."""
        timer = Timer(duration=5.0)
        timer.start()
        
        timer.update(5.0)
        assert timer.finished
        assert timer.time_remaining <= 0.0
        assert not timer.running
    
    def test_timer_doesnt_update_when_stopped(self):
        """Test timer doesn't update when stopped."""
        timer = Timer(duration=10.0)
        timer.start()
        timer.stop()
        
        initial_remaining = timer.time_remaining
        timer.update(5.0)
        assert timer.time_remaining == initial_remaining


class TestTimerCallbacks:
    """Test timer callback functionality."""
    
    def test_timer_callback_executes(self):
        """Test that timer callback executes when timer finishes."""
        callback_called = [False]
        
        def callback():
            callback_called[0] = True
        
        timer = Timer(duration=1.0, callback=callback)
        timer.start()
        
        timer.update(1.0)
        assert callback_called[0]
    
    def test_timer_callback_not_called_before_finish(self):
        """Test callback is not called before timer finishes."""
        callback_called = [False]
        
        def callback():
            callback_called[0] = True
        
        timer = Timer(duration=5.0, callback=callback)
        timer.start()
        
        timer.update(2.0)
        assert not callback_called[0]
        
        timer.update(5.0)  # Finish timer
        assert callback_called[0]
    
    def test_timer_callback_with_loop(self):
        """Test callback with looping timer."""
        callback_count = [0]
        
        def callback():
            callback_count[0] += 1
        
        timer = Timer(duration=1.0, callback=callback)
        timer.start(loop=True)
        
        # First loop
        timer.update(1.0)
        assert callback_count[0] == 1
        assert timer.running  # Should still be running
        
        # Second loop
        timer.update(1.0)
        assert callback_count[0] == 2
        assert timer.running


class TestTimerLooping:
    """Test timer looping functionality."""
    
    def test_timer_loops(self):
        """Test timer loops correctly."""
        timer = Timer(duration=2.0)
        timer.start(loop=True)
        
        # Complete first cycle
        timer.update(2.0)
        assert timer.running
        assert timer.time_remaining == 2.0
        
        # Complete second cycle
        timer.update(2.0)
        assert timer.running
        assert timer.time_remaining == 2.0
    
    def test_timer_progress(self):
        """Test timer progress property."""
        timer = Timer(duration=10.0)
        timer.start()
        
        assert timer.progress == 0.0
        
        timer.update(5.0)
        assert timer.progress == pytest.approx(0.5, abs=0.01)
        
        timer.update(5.0)
        assert timer.progress == pytest.approx(1.0, abs=0.01)


class TestTimerMultiple:
    """Test multiple timers."""
    
    def test_multiple_timers_independent(self):
        """Test that multiple timers are independent."""
        timer1 = Timer(duration=5.0)
        timer2 = Timer(duration=10.0)
        
        timer1.start()
        timer2.start()
        
        timer1.update(5.0)
        assert timer1.finished
        assert not timer2.finished
        
        timer2.update(5.0)
        assert timer2.finished
    
    def test_multiple_timers_same_duration(self):
        """Test multiple timers with same duration."""
        timer1 = Timer(duration=5.0)
        timer2 = Timer(duration=5.0)
        
        timer1.start()
        timer2.start()
        
        # Update both
        timer1.update(2.0)
        timer2.update(2.0)
        
        assert timer1.time_remaining == timer2.time_remaining


class TestStopwatch:
    """Test Stopwatch functionality."""
    
    def test_stopwatch_initialization(self):
        """Test Stopwatch initialization."""
        stopwatch = Stopwatch()
        assert stopwatch.elapsed_time == 0.0
        assert not stopwatch.running
    
    def test_stopwatch_start(self):
        """Test starting stopwatch."""
        stopwatch = Stopwatch()
        stopwatch.start()
        assert stopwatch.running
    
    def test_stopwatch_stop(self):
        """Test stopping stopwatch."""
        stopwatch = Stopwatch()
        stopwatch.start()
        stopwatch.stop()
        assert not stopwatch.running
    
    def test_stopwatch_elapsed_time(self):
        """Test stopwatch elapsed time accumulation."""
        stopwatch = Stopwatch()
        stopwatch.start()
        
        stopwatch.update(2.0)
        assert stopwatch.time == 2.0
        
        stopwatch.update(3.0)
        assert stopwatch.time == 5.0
    
    def test_stopwatch_doesnt_update_when_stopped(self):
        """Test stopwatch doesn't accumulate when stopped."""
        stopwatch = Stopwatch()
        stopwatch.start()
        stopwatch.update(5.0)
        stopwatch.stop()
        
        initial_time = stopwatch.time
        stopwatch.update(10.0)
        assert stopwatch.time == initial_time
    
    def test_stopwatch_reset(self):
        """Test resetting stopwatch."""
        stopwatch = Stopwatch()
        stopwatch.start()
        stopwatch.update(10.0)
        stopwatch.reset()
        
        assert stopwatch.elapsed_time == 0.0
        assert not stopwatch.running

