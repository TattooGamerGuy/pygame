"""Central input coordinator - Modular."""

from typing import Dict, Set
import pygame
from hub.core.input.keyboard import Keyboard
from hub.core.input.mouse import Mouse
from hub.core.input.joystick import Joystick


class InputManager:
    """Central coordinator for all input devices."""
    
    def __init__(self):
        """Initialize input manager."""
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.joystick = Joystick()
        self._enabled = True
    
    def initialize(self) -> None:
        """Initialize all input devices."""
        self.joystick.initialize()
    
    def cleanup(self) -> None:
        """Cleanup input resources."""
        self.joystick.cleanup()
    
    def update(self, events: list) -> None:
        """
        Update all input devices with current events.
        
        Args:
            events: List of pygame events from current frame
        """
        if not self._enabled:
            return
        
        self.keyboard.update(events)
        self.mouse.update(events)
        self.joystick.update(events)
    
    def enable(self) -> None:
        """Enable input processing."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable input processing."""
        self._enabled = False
        self.keyboard.clear()
        self.mouse.clear()
    
    @property
    def enabled(self) -> bool:
        """Check if input is enabled."""
        return self._enabled

