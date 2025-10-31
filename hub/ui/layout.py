"""Layout management system for UI widgets."""

from abc import ABC, abstractmethod
from typing import List, Tuple
from hub.ui.base_widget import BaseWidget


class LayoutConstraints:
    """Constraints for widget layout."""
    
    def __init__(
        self,
        min_width: int = 0,
        min_height: int = 0,
        max_width: int = 0,
        max_height: int = 0,
        fill_width: bool = False,
        fill_height: bool = False,
        weight: float = 1.0
    ):
        """
        Initialize layout constraints.
        
        Args:
            min_width: Minimum width
            min_height: Minimum height
            max_width: Maximum width (0 = no limit)
            max_height: Maximum height (0 = no limit)
            fill_width: Whether to fill available width
            fill_height: Whether to fill available height
            weight: Relative weight for space distribution
        """
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.fill_width = fill_width
        self.fill_height = fill_height
        self.weight = weight


class LayoutManager(ABC):
    """Abstract base class for layout managers."""
    
    @abstractmethod
    def update_layout(self, container: BaseWidget, children: List[BaseWidget]) -> None:
        """
        Update layout of children within container.
        
        Args:
            container: Container widget
            children: List of child widgets to layout
        """
        pass


class VerticalLayoutManager(LayoutManager):
    """Layout manager for vertical arrangement."""
    
    def __init__(self, spacing: int = 0):
        """
        Initialize vertical layout manager.
        
        Args:
            spacing: Space between children
        """
        self.spacing = spacing
    
    def update_layout(self, container: BaseWidget, children: List[BaseWidget]) -> None:
        """Arrange children vertically."""
        y_offset = 0
        for child in children:
            if not child.visible:
                continue
            child.x = container.x
            child.y = container.y + y_offset
            y_offset += child.height + self.spacing


class HorizontalLayoutManager(LayoutManager):
    """Layout manager for horizontal arrangement."""
    
    def __init__(self, spacing: int = 0):
        """
        Initialize horizontal layout manager.
        
        Args:
            spacing: Space between children
        """
        self.spacing = spacing
    
    def update_layout(self, container: BaseWidget, children: List[BaseWidget]) -> None:
        """Arrange children horizontally."""
        x_offset = 0
        for child in children:
            if not child.visible:
                continue
            child.x = container.x + x_offset
            child.y = container.y
            x_offset += child.width + self.spacing


class GridLayoutManager(LayoutManager):
    """Layout manager for grid arrangement."""
    
    def __init__(self, columns: int = 1, spacing: int = 0):
        """
        Initialize grid layout manager.
        
        Args:
            columns: Number of columns
            spacing: Space between items
        """
        self.columns = columns
        self.spacing = spacing
    
    def update_layout(self, container: BaseWidget, children: List[BaseWidget]) -> None:
        """Arrange children in a grid."""
        row = 0
        col = 0
        max_width = 0
        
        for child in children:
            if not child.visible:
                continue
            
            child.x = container.x + col * (max_width + self.spacing)
            child.y = container.y + row * (child.height + self.spacing)
            
            max_width = max(max_width, child.width)
            col += 1
            
            if col >= self.columns:
                col = 0
                row += 1

