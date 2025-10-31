"""
Integration tests for EventBus.

Tests event subscription/publishing, multiple subscribers, unsubscription,
cleanup, and event type handling.
"""

import pytest
from hub.core.events.event_bus import EventBus


@pytest.fixture
def event_bus():
    """Create an EventBus instance for testing."""
    return EventBus()


class TestEventBusSubscription:
    """Test event subscription functionality."""
    
    def test_event_bus_subscribe(self, event_bus):
        """Test subscribing to an event type."""
        callback_called = [False]
        
        def callback(data):
            callback_called[0] = True
        
        event_bus.subscribe("test_event", callback)
        event_bus.publish("test_event")
        
        assert callback_called[0]
    
    def test_event_bus_multiple_subscribers(self, event_bus):
        """Test multiple subscribers to same event."""
        callback1_called = [False]
        callback2_called = [False]
        
        def callback1(data):
            callback1_called[0] = True
        
        def callback2(data):
            callback2_called[0] = True
        
        event_bus.subscribe("test_event", callback1)
        event_bus.subscribe("test_event", callback2)
        
        event_bus.publish("test_event")
        
        assert callback1_called[0]
        assert callback2_called[0]
    
    def test_event_bus_different_event_types(self, event_bus):
        """Test subscribers to different event types."""
        callback1_called = [False]
        callback2_called = [False]
        
        def callback1(data):
            callback1_called[0] = True
        
        def callback2(data):
            callback2_called[0] = True
        
        event_bus.subscribe("event1", callback1)
        event_bus.subscribe("event2", callback2)
        
        event_bus.publish("event1")
        assert callback1_called[0]
        assert not callback2_called[0]
        
        event_bus.publish("event2")
        assert callback2_called[0]


class TestEventBusPublishing:
    """Test event publishing functionality."""
    
    def test_event_bus_publish_with_data(self, event_bus):
        """Test publishing event with data."""
        received_data = [None]
        
        def callback(data):
            received_data[0] = data
        
        event_bus.subscribe("test_event", callback)
        event_bus.publish("test_event", {"key": "value"})
        
        assert received_data[0] == {"key": "value"}
    
    def test_event_bus_publish_without_data(self, event_bus):
        """Test publishing event without data."""
        callback_called = [False]
        
        def callback(data):
            callback_called[0] = True
            assert data is None
        
        event_bus.subscribe("test_event", callback)
        event_bus.publish("test_event")
        
        assert callback_called[0]
    
    def test_event_bus_publish_multiple_times(self, event_bus):
        """Test publishing same event multiple times."""
        call_count = [0]
        
        def callback(data):
            call_count[0] += 1
        
        event_bus.subscribe("test_event", callback)
        
        event_bus.publish("test_event")
        event_bus.publish("test_event")
        event_bus.publish("test_event")
        
        assert call_count[0] == 3


class TestEventBusUnsubscription:
    """Test event unsubscription functionality."""
    
    def test_event_bus_unsubscribe(self, event_bus):
        """Test unsubscribing from an event."""
        callback_called = [False]
        
        def callback(data):
            callback_called[0] = True
        
        event_bus.subscribe("test_event", callback)
        event_bus.unsubscribe("test_event", callback)
        
        event_bus.publish("test_event")
        assert not callback_called[0]
    
    def test_event_bus_unsubscribe_partial(self, event_bus):
        """Test unsubscribing one of multiple callbacks."""
        callback1_called = [False]
        callback2_called = [False]
        
        def callback1(data):
            callback1_called[0] = True
        
        def callback2(data):
            callback2_called[0] = True
        
        event_bus.subscribe("test_event", callback1)
        event_bus.subscribe("test_event", callback2)
        event_bus.unsubscribe("test_event", callback1)
        
        event_bus.publish("test_event")
        assert not callback1_called[0]
        assert callback2_called[0]
    
    def test_event_bus_unsubscribe_nonexistent(self, event_bus):
        """Test unsubscribing from non-existent subscription."""
        def callback(data):
            pass
        
        # Should not raise error
        event_bus.unsubscribe("nonexistent_event", callback)
        event_bus.unsubscribe("test_event", callback)


class TestEventBusCleanup:
    """Test event bus cleanup functionality."""
    
    def test_event_bus_clear(self, event_bus):
        """Test clearing all subscribers."""
        callback_called = [False]
        
        def callback(data):
            callback_called[0] = True
        
        event_bus.subscribe("event1", callback)
        event_bus.subscribe("event2", callback)
        
        event_bus.clear()
        
        event_bus.publish("event1")
        event_bus.publish("event2")
        
        assert not callback_called[0]


class TestEventBusErrorHandling:
    """Test event bus error handling."""
    
    def test_event_bus_callback_error_handling(self, event_bus):
        """Test that callback errors don't break event bus."""
        callback1_called = [False]
        callback2_called = [False]
        
        def callback1(data):
            raise ValueError("Callback error")
        
        def callback2(data):
            callback2_called[0] = True
        
        event_bus.subscribe("test_event", callback1)
        event_bus.subscribe("test_event", callback2)
        
        # Should not raise error, callback2 should still be called
        event_bus.publish("test_event")
        assert callback2_called[0]
    
    def test_event_bus_multiple_errors(self, event_bus):
        """Test handling multiple callback errors."""
        def callback1(data):
            raise ValueError("Error 1")
        
        def callback2(data):
            raise ValueError("Error 2")
        
        def callback3(data):
            pass  # This should still execute
        
        callback3_called = [False]
        
        def callback3_wrapper(data):
            callback3_called[0] = True
        
        event_bus.subscribe("test_event", callback1)
        event_bus.subscribe("test_event", callback2)
        event_bus.subscribe("test_event", callback3_wrapper)
        
        # Should handle all errors gracefully
        event_bus.publish("test_event")
        assert callback3_called[0]


class TestEventBusComplexScenarios:
    """Test complex event bus scenarios."""
    
    def test_event_bus_nested_events(self, event_bus):
        """Test publishing events from within callbacks."""
        outer_called = [False]
        inner_called = [False]
        
        def inner_callback(data):
            inner_called[0] = True
        
        def outer_callback(data):
            outer_called[0] = True
            event_bus.publish("inner_event")
        
        event_bus.subscribe("outer_event", outer_callback)
        event_bus.subscribe("inner_event", inner_callback)
        
        event_bus.publish("outer_event")
        
        assert outer_called[0]
        assert inner_called[0]
    
    def test_event_bus_many_subscribers(self, event_bus):
        """Test event bus with many subscribers."""
        call_count = [0]
        
        def create_callback(index):
            def callback(data):
                call_count[0] += 1
            return callback
        
        # Subscribe 100 callbacks
        for i in range(100):
            event_bus.subscribe("test_event", create_callback(i))
        
        event_bus.publish("test_event")
        assert call_count[0] == 100
    
    def test_event_bus_re_subscribe(self, event_bus):
        """Test subscribing same callback multiple times."""
        call_count = [0]
        
        def callback(data):
            call_count[0] += 1
        
        # Subscribe same callback multiple times
        event_bus.subscribe("test_event", callback)
        event_bus.subscribe("test_event", callback)
        event_bus.subscribe("test_event", callback)
        
        event_bus.publish("test_event")
        # Should be called multiple times
        assert call_count[0] == 3

