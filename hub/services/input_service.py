"""Input handling service."""

from typing import Set, Tuple
import pygame
from hub.events.event_bus import EventBus
from hub.events.events import QuitEvent


class InputService:
    """Centralized input handling service."""
    
    def __init__(self, event_bus: EventBus):
        """
        Initialize input service.
        
        Args:
            event_bus: Event bus for publishing input events
        """
        self.event_bus = event_bus
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_pressed: Tuple[bool, bool, bool] = (False, False, False)
        self.mouse_just_clicked: Tuple[bool, bool, bool] = (False, False, False)
    
    def update(self, events: list) -> None:
        """
        Update input state from pygame events.
        
        Args:
            events: List of pygame events
        """
        # Reset just-pressed/clicked states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_just_clicked = (False, False, False)
        
        # Update mouse state
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
        
        # Process events
        for event in events:
            if event.type == pygame.QUIT:
                self.event_bus.publish(QuitEvent())
            
            elif event.type == pygame.KEYDOWN:
                if event.key not in self.keys_pressed:
                    self.keys_just_pressed.add(event.key)
                self.keys_pressed.add(event.key)
            
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_just_released.add(event.key)
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_index = event.button - 1
                if 0 <= button_index < 3:
                    self.mouse_just_clicked = tuple(
                        i == button_index if i < 3 else False
                        for i in range(3)
                    )
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is currently pressed."""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if key was just pressed this frame."""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if key was just released this frame."""
        return key in self.keys_just_released
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return self.mouse_pos
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if mouse button is pressed (0=left, 1=middle, 2=right)."""
        if 0 <= button < 3:
            return self.mouse_pressed[button]
        return False
    
    def is_mouse_button_clicked(self, button: int) -> bool:
        """Check if mouse button was just clicked this frame."""
        if 0 <= button < 3:
            return self.mouse_just_clicked[button]
        return False

