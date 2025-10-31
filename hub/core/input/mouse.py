"""Mouse state and events - Modular."""

from typing import Tuple, Set
import pygame


class Mouse:
    """Manages mouse input state."""
    
    def __init__(self):
        """Initialize mouse handler."""
        self._position: Tuple[int, int] = (0, 0)
        self._pressed_buttons: Set[int] = set()
        self._just_pressed_buttons: Set[int] = set()
        self._just_released_buttons: Set[int] = set()
        self._wheel_x = 0
        self._wheel_y = 0
    
    def update(self, events: list) -> None:
        """
        Update mouse state from events.
        
        Args:
            events: List of pygame events
        """
        # Clear frame-specific states
        self._just_pressed_buttons.clear()
        self._just_released_buttons.clear()
        self._wheel_x = 0
        self._wheel_y = 0
        
        was_pressed = self._pressed_buttons.copy()
        current_pressed = set(pygame.mouse.get_pressed())
        
        # Detect button changes
        self._just_pressed_buttons = current_pressed - was_pressed
        self._just_released_buttons = was_pressed - current_pressed
        self._pressed_buttons = current_pressed
        
        # Update position
        self._position = pygame.mouse.get_pos()
        
        # Handle wheel events
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self._wheel_x += event.x
                self._wheel_y += event.y
    
    @property
    def position(self) -> Tuple[int, int]:
        """Get mouse position."""
        return self._position
    
    @property
    def x(self) -> int:
        """Get mouse X position."""
        return self._position[0]
    
    @property
    def y(self) -> int:
        """Get mouse Y position."""
        return self._position[1]
    
    def is_pressed(self, button: int) -> bool:
        """
        Check if mouse button is currently pressed.
        
        Args:
            button: pygame mouse button constant (1=left, 2=middle, 3=right)
            
        Returns:
            True if button is pressed
        """
        return button in self._pressed_buttons
    
    def is_just_pressed(self, button: int) -> bool:
        """
        Check if mouse button was just pressed this frame.
        
        Args:
            button: pygame mouse button constant
            
        Returns:
            True if button was just pressed
        """
        return button in self._just_pressed_buttons
    
    def is_just_released(self, button: int) -> bool:
        """
        Check if mouse button was just released this frame.
        
        Args:
            button: pygame mouse button constant
            
        Returns:
            True if button was just released
        """
        return button in self._just_released_buttons
    
    @property
    def wheel_x(self) -> int:
        """Get mouse wheel X movement this frame."""
        return self._wheel_x
    
    @property
    def wheel_y(self) -> int:
        """Get mouse wheel Y movement this frame."""
        return self._wheel_y
    
    def clear(self) -> None:
        """Clear all mouse state."""
        self._pressed_buttons.clear()
        self._just_pressed_buttons.clear()
        self._just_released_buttons.clear()
        self._wheel_x = 0
        self._wheel_y = 0

