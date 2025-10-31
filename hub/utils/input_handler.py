"""Input handling abstraction for keyboard and mouse events."""

from typing import Set, Optional
import pygame


class InputHandler:
    """Handles keyboard and mouse input state."""
    
    def __init__(self):
        """Initialize the input handler."""
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        self.mouse_pos: tuple = (0, 0)
        self.mouse_pressed: tuple = (False, False, False)
        self.mouse_just_clicked: tuple = (False, False, False)
        self.mouse_just_released: tuple = (False, False, False)
    
    def update(self, events: list):
        """
        Update input state based on pygame events.
        
        Args:
            events: List of pygame events from pygame.event.get()
        """
        # Reset just-pressed and just-released states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_just_clicked = (False, False, False)
        self.mouse_just_released = (False, False, False)
        
        # Update mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
        
        # Process events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.keys_pressed:
                    self.keys_just_pressed.add(event.key)
                self.keys_pressed.add(event.key)
            
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_just_released.add(event.key)
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_index = event.button - 1  # pygame uses 1-5, we use 0-4
                if button_index < 3:
                    self.mouse_just_clicked = tuple(
                        i == button_index if i < 3 else False
                        for i in range(3)
                    )
            
            elif event.type == pygame.MOUSEBUTTONUP:
                button_index = event.button - 1
                if button_index < 3:
                    self.mouse_just_released = tuple(
                        i == button_index if i < 3 else False
                        for i in range(3)
                    )
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed."""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame."""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame."""
        return key in self.keys_just_released
    
    def get_mouse_pos(self) -> tuple:
        """Get current mouse position."""
        return self.mouse_pos
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is currently pressed (0=left, 1=middle, 2=right)."""
        if 0 <= button < 3:
            return self.mouse_pressed[button]
        return False
    
    def is_mouse_button_clicked(self, button: int) -> bool:
        """Check if a mouse button was just clicked this frame."""
        if 0 <= button < 3:
            return self.mouse_just_clicked[button]
        return False
    
    def is_mouse_button_released(self, button: int) -> bool:
        """Check if a mouse button was just released this frame."""
        if 0 <= button < 3:
            return self.mouse_just_released[button]
        return False

