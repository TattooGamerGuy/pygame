"""
Modal/Dialog component for UI.

Supports various dialog types: alerts, confirmations, prompts, and custom modals.
"""

from typing import Optional, List, Callable, Union
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager
from hub.ui.button import Button


class Modal(BaseWidget):
    """Modal dialog widget."""
    
    def __init__(
        self,
        title: str = "",
        content: str = "",
        buttons: Optional[List[str]] = None,
        width: int = 400,
        height: int = 300,
        x: Optional[int] = None,
        y: Optional[int] = None,
        default_button: int = 0,
        show_backdrop: bool = True,
        close_on_backdrop_click: bool = True,
        close_on_escape: bool = True,
        on_confirm: Optional[Callable[[int], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
        is_prompt: bool = False,
        theme=None
    ):
        """
        Initialize modal.
        
        Args:
            title: Modal title
            content: Modal content text
            buttons: List of button labels (empty for no buttons)
            width: Modal width
            height: Modal height
            x: X position (None for centered)
            y: Y position (None for centered)
            default_button: Index of default button (highlighted)
            show_backdrop: Whether to show backdrop overlay
            close_on_backdrop_click: Whether clicking backdrop closes modal
            close_on_escape: Whether Escape key closes modal
            on_confirm: Callback when button clicked (button_index)
            on_close: Callback when modal closes
            is_prompt: Whether modal is a prompt (has text input)
            theme: Optional theme
        """
        # Calculate centered position if not provided
        # In real implementation, would use screen size
        screen_width = 800  # Default
        screen_height = 600  # Default
        
        if x is None:
            x = (screen_width - width) // 2
        if y is None:
            y = (screen_height - height) // 2
        
        super().__init__(x, y, width, height)
        
        self.title = title
        self.content = content
        self.buttons = buttons or []
        self.default_button = default_button
        self.show_backdrop = show_backdrop
        self.close_on_backdrop_click = close_on_backdrop_click
        self.close_on_escape = close_on_escape
        self.on_confirm = on_confirm
        self.on_close = on_close
        self.is_prompt = is_prompt
        self.theme = theme or ThemeManager.get_default_theme()
        
        # State
        self._is_open = False
        self._input_value = "" if is_prompt else None
        self._button_widgets: List[Button] = []
        
        # Initialize font
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
        self._title_font = pygame.font.Font(None, self.theme.font_size + 4)
        
        # Create button widgets (will be created when needed)
        self._buttons_created = False
    
    @property
    def is_open(self) -> bool:
        """Check if modal is open."""
        return self._is_open
    
    @property
    def input_value(self) -> Optional[str]:
        """Get input value (for prompt modals)."""
        return self._input_value
    
    def _create_buttons(self) -> None:
        """Create button widgets."""
        if self._buttons_created:
            return
        
        self._button_widgets = []
        
        if not self.buttons:
            self._buttons_created = True
            return
        
        button_width = 80
        button_height = 30
        button_spacing = 10
        total_width = len(self.buttons) * button_width + (len(self.buttons) - 1) * button_spacing
        start_x = self._rect.centerx - total_width // 2
        
        for i, button_text in enumerate(self.buttons):
            button_x = start_x + i * (button_width + button_spacing)
            button_y = self._rect.bottom - 40
            
            button = Button(
                button_x,
                button_y,
                button_width,
                button_height,
                button_text
            )
            
            # Store button index in button (via callback)
            def make_callback(idx):
                def callback():
                    self.confirm(idx)
                return callback
            
            button.on_click = make_callback(i)
            self._button_widgets.append(button)
        
        self._buttons_created = True
    
    def open(self) -> None:
        """Open modal."""
        if not self._is_open:
            self._is_open = True
            self._create_buttons()  # Ensure buttons are created when opening
    
    def close(self) -> None:
        """Close modal."""
        if self._is_open:
            self._is_open = False
            if self.on_close:
                self.on_close()
    
    def confirm(self, button_index: int) -> None:
        """
        Confirm modal with button index.
        
        Args:
            button_index: Index of clicked button
        """
        was_open = self._is_open
        self.close()
        if was_open and self.on_confirm:
            self.on_confirm(button_index)
    
    def handle_click(self, pos: tuple) -> None:
        """
        Handle mouse click.
        
        Args:
            pos: Click position (x, y)
        """
        if not self._is_open:
            return
        
        # Check if clicking on buttons
        for button in self._button_widgets:
            if button.contains_point(pos):
                # Trigger button click which will call the callback
                if hasattr(button, 'on_click') and button.on_click:
                    button.on_click()
                return
        
        # Check if clicking backdrop
        if self.close_on_backdrop_click and not self.contains_point(pos):
            self.close()
            return
        
        # Click within modal (but not on buttons)
        # For prompt modals, might focus input
        if self.contains_point(pos):
            pass  # Handle internal clicks if needed
    
    def handle_escape(self) -> None:
        """Handle Escape key."""
        if self._is_open and self.close_on_escape:
            self.close()
    
    def handle_enter(self) -> None:
        """Handle Enter key."""
        if self._is_open and self.buttons:
            # Trigger default button
            if 0 <= self.default_button < len(self.buttons):
                self.confirm(self.default_button)
    
    @staticmethod
    def alert(title: str, message: str, on_close: Optional[Callable[[], None]] = None) -> 'Modal':
        """
        Create alert modal.
        
        Args:
            title: Alert title
            message: Alert message
            on_close: Optional close callback
            
        Returns:
            Modal instance
        """
        return Modal(
            title=title,
            content=message,
            buttons=["OK"],
            on_close=on_close
        )
    
    @staticmethod
    def confirm(title: str, message: str, on_confirm: Optional[Callable[[bool], None]] = None) -> 'Modal':
        """
        Create confirmation modal.
        
        Args:
            title: Confirmation title
            message: Confirmation message
            on_confirm: Callback with True for OK, False for Cancel
            
        Returns:
            Modal instance
        """
        def wrapper(button_index: int):
            if on_confirm:
                on_confirm(button_index == 0)  # True for OK, False for Cancel
        
        return Modal(
            title=title,
            content=message,
            buttons=["OK", "Cancel"],
            on_confirm=wrapper
        )
    
    @staticmethod
    def prompt(title: str, message: str, on_confirm: Optional[Callable[[str], None]] = None) -> 'Modal':
        """
        Create prompt modal.
        
        Args:
            title: Prompt title
            message: Prompt message
            on_confirm: Callback with input value
            
        Returns:
            Modal instance
        """
        modal = Modal(
            title=title,
            content=message,
            buttons=["OK", "Cancel"],
            is_prompt=True
        )
        
        if on_confirm:
            original_on_confirm = modal.on_confirm
            def wrapper(button_index: int):
                if button_index == 0:  # OK button
                    on_confirm(modal.input_value or "")
                elif original_on_confirm:
                    original_on_confirm(button_index)
            
            modal.on_confirm = wrapper
        return modal
    
    def _update_widget(self, dt: float, mouse_pos: tuple, mouse_clicked: bool) -> None:
        """Update widget state."""
        if mouse_clicked:
            self.handle_click(mouse_pos)
        
        # Update button widgets
        for button in self._button_widgets:
            button.update(dt, mouse_pos, mouse_clicked)
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render modal."""
        if not self._is_open:
            return
        
        # Draw backdrop
        if self.show_backdrop:
            backdrop = pygame.Surface((surface.get_width(), surface.get_height()))
            backdrop.set_alpha(128)
            backdrop.fill((0, 0, 0))
            surface.blit(backdrop, (0, 0))
        
        # Draw modal background
        pygame.draw.rect(surface, self.theme.background_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw title
        if self.title:
            title_surface = self._title_font.render(self.title, True, self.theme.text_color)
            title_rect = title_surface.get_rect(centerx=self._rect.centerx, top=self._rect.y + 20)
            surface.blit(title_surface, title_rect)
        
        # Draw content
        if self.content:
            content_y = self._rect.y + 60
            # Simple text rendering (could be improved with word wrap)
            content_surface = self._font.render(self.content, True, self.theme.text_color)
            content_rect = content_surface.get_rect(centerx=self._rect.centerx, top=content_y)
            surface.blit(content_surface, content_rect)
        
        # Draw buttons
        for button in self._button_widgets:
            button.render(surface)
        
        # Draw prompt input if needed
        if self.is_prompt and self._input_value is not None:
            # Input rendering would go here
            # For now, just show placeholder
            pass

