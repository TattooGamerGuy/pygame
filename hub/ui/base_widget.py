"""Base widget class for UI components."""

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
import pygame
from hub.events.event_bus import EventBus


class BaseWidget(ABC):
    """Abstract base class for all UI widgets."""
    
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        event_bus: Optional[EventBus] = None
    ):
        """
        Initialize base widget.
        
        Args:
            x: X position
            y: Y position
            width: Widget width
            height: Widget height
            event_bus: Optional event bus for widget events
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)
        self._visible = True
        self._enabled = True
        self._parent: Optional[BaseWidget] = None
        self._children: List[BaseWidget] = []
        self.event_bus = event_bus
    
    @property
    def x(self) -> int:
        """Get X position."""
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        """Set X position."""
        self._x = value
        self._rect.x = value
    
    @property
    def y(self) -> int:
        """Get Y position."""
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        """Set Y position."""
        self._y = value
        self._rect.y = value
    
    @property
    def width(self) -> int:
        """Get width."""
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        """Set width."""
        self._width = value
        self._rect.width = value
    
    @property
    def height(self) -> int:
        """Get height."""
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        """Set height."""
        self._height = value
        self._rect.height = value
    
    @property
    def rect(self) -> pygame.Rect:
        """Get widget rectangle."""
        return self._rect
    
    @property
    def position(self) -> Tuple[int, int]:
        """Get position as tuple."""
        return (self._x, self._y)
    
    @position.setter
    def position(self, value: Tuple[int, int]) -> None:
        """Set position from tuple."""
        self.x, self.y = value
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get size as tuple."""
        return (self._width, self._height)
    
    @size.setter
    def size(self, value: Tuple[int, int]) -> None:
        """Set size from tuple."""
        self.width, self.height = value
    
    @property
    def visible(self) -> bool:
        """Check if widget is visible."""
        return self._visible
    
    @visible.setter
    def visible(self, value: bool) -> None:
        """Set visibility."""
        self._visible = value
    
    @property
    def enabled(self) -> bool:
        """Check if widget is enabled."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set enabled state."""
        self._enabled = value
    
    def add_child(self, child: 'BaseWidget') -> None:
        """Add a child widget."""
        if child not in self._children:
            self._children.append(child)
            child._parent = self
    
    def remove_child(self, child: 'BaseWidget') -> None:
        """Remove a child widget."""
        if child in self._children:
            self._children.remove(child)
            child._parent = None
    
    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if point is within widget bounds."""
        return self._rect.collidepoint(point)
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> None:
        """
        Update widget state.
        
        Args:
            dt: Delta time
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse was clicked this frame
        """
        if not self._visible or not self._enabled:
            return
        
        self._update_widget(dt, mouse_pos, mouse_clicked)
        
        # Update children
        for child in self._children:
            child.update(dt, mouse_pos, mouse_clicked)
    
    @abstractmethod
    def _update_widget(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> None:
        """Update widget-specific logic. Override in subclasses."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render widget to surface.
        
        Args:
            surface: Surface to render to
        """
        if not self._visible:
            return
        
        self._render_widget(surface)
        
        # Render children
        for child in self._children:
            child.render(surface)
    
    @abstractmethod
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render widget-specific graphics. Override in subclasses."""
        pass

