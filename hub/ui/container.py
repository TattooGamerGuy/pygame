"""Container widgets for layout management."""

from typing import List, Optional, Tuple
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.layout import LayoutManager, LayoutConstraints


class Container(BaseWidget):
    """Base container widget for grouping other widgets."""
    
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        layout_manager: Optional[LayoutManager] = None
    ):
        """
        Initialize container.
        
        Args:
            x: X position
            y: Y position
            width: Container width
            height: Container height
            layout_manager: Optional layout manager
        """
        super().__init__(x, y, width, height)
        self.layout_manager = layout_manager or LayoutManager()
        self._background_color: Optional[Tuple[int, int, int]] = None
        self._padding = (0, 0, 0, 0)  # top, right, bottom, left
    
    def _update_widget(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> None:
        """Update container and layout."""
        # Layout manager handles child positioning if present
        if self.layout_manager:
            self.layout_manager.update_layout(self, self._children)
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render container background."""
        if self._background_color:
            pygame.draw.rect(surface, self._background_color, self._rect)
    
    @property
    def background_color(self) -> Optional[Tuple[int, int, int]]:
        """Get background color."""
        return self._background_color
    
    @background_color.setter
    def background_color(self, value: Optional[Tuple[int, int, int]]) -> None:
        """Set background color."""
        self._background_color = value
    
    @property
    def padding(self) -> Tuple[int, int, int, int]:
        """Get padding (top, right, bottom, left)."""
        return self._padding
    
    @padding.setter
    def padding(self, value: Tuple[int, int, int, int]) -> None:
        """Set padding."""
        self._padding = value


class VContainer(Container):
    """Vertical container - arranges children vertically."""
    
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, spacing: int = 0):
        """Initialize vertical container."""
        from hub.ui.layout import VerticalLayoutManager
        layout = VerticalLayoutManager(spacing=spacing)
        super().__init__(x, y, width, height, layout)


class HContainer(Container):
    """Horizontal container - arranges children horizontally."""
    
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, spacing: int = 0):
        """Initialize horizontal container."""
        from hub.ui.layout import HorizontalLayoutManager
        layout = HorizontalLayoutManager(spacing=spacing)
        super().__init__(x, y, width, height, layout)


class GridContainer(Container):
    """Grid container - arranges children in a grid."""
    
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        columns: int = 1,
        spacing: int = 0
    ):
        """Initialize grid container."""
        from hub.ui.layout import GridLayoutManager
        layout = GridLayoutManager(columns=columns, spacing=spacing)
        super().__init__(x, y, width, height, layout)

