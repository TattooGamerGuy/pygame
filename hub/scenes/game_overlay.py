"""UI components for game overlays and menus."""

from typing import Optional, Callable
import pygame
from hub.utils.constants import BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, WHITE, BLACK


class Button:
    """A clickable button with hover effects."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        callback: Optional[Callable[[], None]] = None,
        color: tuple = BUTTON_COLOR,
        hover_color: tuple = BUTTON_HOVER_COLOR,
        text_color: tuple = BUTTON_TEXT_COLOR
    ):
        """
        Initialize a button.
        
        Args:
            x: X position of button
            y: Y position of button
            width: Button width
            height: Button height
            text: Button text
            font: Font to use for text
            callback: Function to call when clicked
            color: Normal button color
            hover_color: Hover button color
            text_color: Text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> bool:
        """
        Update button state.
        
        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse button was clicked this frame
            
        Returns:
            True if button was clicked
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and mouse_clicked and self.callback:
            self.callback()
            return True
        return False
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the button.
        
        Args:
            surface: Surface to render to
        """
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        # Center text
        self.text_rect.center = self.rect.center
        surface.blit(self.text_surface, self.text_rect)


def render_text_centered(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    y: int,
    color: tuple = WHITE
) -> None:
    """
    Render text centered horizontally.
    
    Args:
        surface: Surface to render to
        text: Text to render
        font: Font to use
        y: Y position
        color: Text color
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)

