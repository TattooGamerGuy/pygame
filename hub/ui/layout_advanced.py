"""
Advanced layout system for UI components.

Supports flexbox, grid, auto-layout, and responsive layouts.
"""

from typing import List, Optional, Dict, Tuple, Any, Callable
from dataclasses import dataclass
from hub.ui.animation import Tween, Easing, AnimationState


@dataclass
class LayoutConstraints:
    """Layout constraints for auto-layout."""
    anchor_x: Optional[str] = None  # "left", "center", "right"
    anchor_y: Optional[str] = None  # "top", "center", "bottom"
    margin: int = 0
    margin_left: Optional[int] = None
    margin_right: Optional[int] = None
    margin_top: Optional[int] = None
    margin_bottom: Optional[int] = None
    percent_x: Optional[float] = None  # 0-100
    percent_y: Optional[float] = None  # 0-100
    width: Optional[int] = None
    height: Optional[int] = None
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None


class FlexLayout:
    """CSS Flexbox-like layout system."""
    
    def __init__(
        self,
        direction: str = "row",
        justify_content: str = "flex-start",
        align_items: str = "stretch",
        flex_wrap: str = "nowrap",
        spacing: int = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: int = 0,
        breakpoint: Optional[int] = None,
        animate: bool = False,
        animation_duration: float = 0.3
    ):
        """
        Initialize flex layout.
        
        Args:
            direction: "row" or "column"
            justify_content: "flex-start", "flex-end", "center", "space-between", "space-around"
            align_items: "stretch", "flex-start", "flex-end", "center"
            flex_wrap: "nowrap" or "wrap"
            spacing: Space between items
            width: Container width
            height: Container height
            padding: Container padding
            breakpoint: Resolution breakpoint for responsive switching
            animate: Whether to animate layout changes
            animation_duration: Animation duration in seconds
        """
        self.direction = direction
        self.justify_content = justify_content
        self.align_items = align_items
        self.flex_wrap = flex_wrap
        self.spacing = spacing
        self.width = width
        self.height = height
        self.padding = padding
        self.breakpoint = breakpoint
        self.animate = animate
        self.animation_duration = animation_duration
        
        self._animation_tweens: List[Tween] = []
        self._is_animating = False
    
    def layout(self, widgets: List[Any]) -> None:
        """
        Layout widgets using flexbox.
        
        Args:
            widgets: List of widgets with x, y, width, height attributes
        """
        if not widgets:
            return
        
        if self.flex_wrap == "wrap":
            self._layout_wrapped(widgets)
        else:
            self._layout_single_line(widgets)
    
    def _layout_single_line(self, widgets: List[Any]) -> None:
        """Layout widgets in single line."""
        if self.direction == "row":
            self._layout_row(widgets)
        else:
            self._layout_column(widgets)
    
    def _layout_row(self, widgets: List[Any]) -> None:
        """Layout widgets in row."""
        x = self.padding
        y = self.padding
        
        # Calculate total width
        total_width = sum(w.width for w in widgets) + self.spacing * (len(widgets) - 1)
        
        # Apply justify-content
        if self.justify_content == "flex-start":
            x = self.padding
        elif self.justify_content == "flex-end":
            if self.width:
                x = self.width - total_width - self.padding
        elif self.justify_content == "center":
            if self.width:
                x = (self.width - total_width) // 2
        elif self.justify_content == "space-between":
            if self.width and len(widgets) > 1:
                available_space = self.width - 2 * self.padding - total_width
                spacing = available_space // (len(widgets) - 1) if len(widgets) > 1 else 0
            else:
                spacing = self.spacing
        elif self.justify_content == "space-around":
            if self.width and len(widgets) > 0:
                available_space = self.width - 2 * self.padding - total_width
                spacing = available_space // (len(widgets) + 1) if len(widgets) > 0 else 0
                x = self.padding + spacing
            else:
                spacing = self.spacing
        else:
            spacing = self.spacing
        
        # Position widgets
        for i, widget in enumerate(widgets):
            if i > 0:
                if self.justify_content == "space-between":
                    x = widgets[i-1].x + widgets[i-1].width + spacing
                elif self.justify_content == "space-around":
                    x += spacing
                else:
                    x += widgets[i-1].width + spacing
            
            # Apply align-items
            if self.align_items == "flex-start" or self.align_items == "stretch":
                widget_y = self.padding
            elif self.align_items == "flex-end":
                if self.height:
                    widget_y = self.height - widget.height - self.padding
                else:
                    widget_y = self.padding
            elif self.align_items == "center":
                if self.height:
                    widget_y = (self.height - widget.height) // 2
                else:
                    widget_y = self.padding
            else:
                widget_y = self.padding
            
            self._set_widget_position(widget, x, widget_y)
    
    def _layout_column(self, widgets: List[Any]) -> None:
        """Layout widgets in column."""
        x = self.padding
        y = self.padding
        
        # Calculate total height
        total_height = sum(w.height for w in widgets) + self.spacing * (len(widgets) - 1)
        
        # Apply justify-content
        if self.justify_content == "flex-start":
            y = self.padding
        elif self.justify_content == "flex-end":
            if self.height:
                y = self.height - total_height - self.padding
        elif self.justify_content == "center":
            if self.height:
                y = (self.height - total_height) // 2
        elif self.justify_content == "space-between":
            if self.height and len(widgets) > 1:
                available_space = self.height - 2 * self.padding - total_height
                spacing = available_space // (len(widgets) - 1) if len(widgets) > 1 else 0
            else:
                spacing = self.spacing
        elif self.justify_content == "space-around":
            if self.height and len(widgets) > 0:
                available_space = self.height - 2 * self.padding - total_height
                spacing = available_space // (len(widgets) + 1) if len(widgets) > 0 else 0
                y = self.padding + spacing
            else:
                spacing = self.spacing
        else:
            spacing = self.spacing
        
        # Position widgets
        current_y = y
        for i, widget in enumerate(widgets):
            if i > 0:
                if self.justify_content == "space-between":
                    current_y = widgets[i-1].y + widgets[i-1].height + spacing
                elif self.justify_content == "space-around":
                    current_y += spacing
                else:
                    current_y = widgets[i-1].y + widgets[i-1].height + spacing
            
            # Apply align-items
            if self.align_items == "flex-start" or self.align_items == "stretch":
                widget_x = self.padding
            elif self.align_items == "flex-end":
                if self.width:
                    widget_x = self.width - widget.width - self.padding
                else:
                    widget_x = self.padding
            elif self.align_items == "center":
                if self.width:
                    widget_x = (self.width - widget.width) // 2
                else:
                    widget_x = self.padding
            else:
                widget_x = self.padding
            
            self._set_widget_position(widget, widget_x, current_y)
            if i == 0:
                current_y = y  # Reset for first widget position tracking
    
    def _layout_wrapped(self, widgets: List[Any]) -> None:
        """Layout widgets with wrapping."""
        if self.direction == "row":
            self._layout_wrapped_row(widgets)
        else:
            self._layout_wrapped_column(widgets)
    
    def _layout_wrapped_row(self, widgets: List[Any]) -> None:
        """Layout widgets in wrapped row."""
        x = self.padding
        y = self.padding
        max_height = 0
        
        for widget in widgets:
            if self.width and x + widget.width > self.width - self.padding:
                # Wrap to next line
                y += max_height + self.spacing
                x = self.padding
                max_height = widget.height
            else:
                max_height = max(max_height, widget.height)
            
            self._set_widget_position(widget, x, y)
            x += widget.width + self.spacing
    
    def _layout_wrapped_column(self, widgets: List[Any]) -> None:
        """Layout widgets in wrapped column."""
        x = self.padding
        y = self.padding
        max_width = 0
        
        for widget in widgets:
            if self.height and y + widget.height > self.height - self.padding:
                # Wrap to next column
                x += max_width + self.spacing
                y = self.padding
                max_width = widget.width
            else:
                max_width = max(max_width, widget.width)
            
            self._set_widget_position(widget, x, y)
            y += widget.height + self.spacing
    
    def _set_widget_position(self, widget: Any, x: float, y: float) -> None:
        """Set widget position, with animation if enabled."""
        if self.animate and (hasattr(widget, 'x') and hasattr(widget, 'y')):
            # Animate position change
            start_x = widget.x
            start_y = widget.y
            
            def update_x(val):
                widget.x = int(val)
            
            def update_y(val):
                widget.y = int(val)
            
            tween_x = Tween(
                start_value=float(start_x),
                end_value=x,
                duration=self.animation_duration,
                easing=Easing.ease_out,
                on_update=update_x
            )
            
            tween_y = Tween(
                start_value=float(start_y),
                end_value=y,
                duration=self.animation_duration,
                easing=Easing.ease_out,
                on_update=update_y
            )
            
            tween_x.start()
            tween_y.start()
            
            self._animation_tweens.extend([tween_x, tween_y])
            self._is_animating = True
        else:
            widget.x = int(x)
            widget.y = int(y)
    
    def update_animation(self, dt: float) -> None:
        """Update layout animations."""
        if not self._is_animating:
            return
        
        active_tweens = []
        for tween in self._animation_tweens:
            if tween.state == AnimationState.RUNNING:
                tween.update(dt)
                active_tweens.append(tween)
        
        self._animation_tweens = active_tweens
        self._is_animating = len(active_tweens) > 0
    
    @property
    def is_animating(self) -> bool:
        """Check if layout is animating."""
        return self._is_animating
    
    def update_for_resolution(self, width: int, height: int) -> None:
        """
        Update layout for resolution (responsive).
        
        Args:
            width: Screen width
            height: Screen height
        """
        if self.breakpoint:
            # Auto-switch direction based on breakpoint
            if width < self.breakpoint:
                self.direction = "column"
            else:
                self.direction = "row"
        
        if isinstance(self.spacing, str) and self.spacing == "adaptive":
            # Adaptive spacing based on resolution
            base_spacing = 10
            scale = min(width / 1920.0, 1.0)
            self.spacing = int(base_spacing * scale)


class GridLayout:
    """CSS Grid-like layout system."""
    
    def __init__(
        self,
        rows: Optional[int] = None,
        cols: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        spacing: int = 0,
        padding: int = 0
    ):
        """
        Initialize grid layout.
        
        Args:
            rows: Number of rows (None for auto)
            cols: Number of columns (None for auto)
            width: Container width
            height: Container height
            spacing: Space between grid cells
            padding: Container padding
        """
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.spacing = spacing
        self.padding = padding
    
    def layout(self, widgets: List[Any]) -> None:
        """
        Layout widgets in grid.
        
        Args:
            widgets: List of widgets
        """
        if not widgets:
            return
        
        # Auto-calculate rows or cols if not specified
        if self.rows is None and self.cols:
            self.rows = (len(widgets) + self.cols - 1) // self.cols
        elif self.cols is None and self.rows:
            self.cols = (len(widgets) + self.rows - 1) // self.rows
        elif self.rows is None and self.cols is None:
            # Default to square grid
            import math
            self.cols = int(math.ceil(math.sqrt(len(widgets))))
            self.rows = (len(widgets) + self.cols - 1) // self.cols
        
        # Calculate cell size
        if self.width and self.height:
            available_width = self.width - 2 * self.padding - self.spacing * (self.cols - 1)
            available_height = self.height - 2 * self.padding - self.spacing * (self.rows - 1)
            cell_width = available_width // self.cols
            cell_height = available_height // self.rows
        else:
            # Use widget sizes
            if widgets:
                cell_width = max(w.width for w in widgets) + self.spacing
                cell_height = max(w.height for w in widgets) + self.spacing
            else:
                return
        
        # Position widgets
        for i, widget in enumerate(widgets):
            row = i // self.cols
            col = i % self.cols
            
            x = self.padding + col * (cell_width + self.spacing)
            y = self.padding + row * (cell_height + self.spacing)
            
            widget.x = int(x)
            widget.y = int(y)


class AutoLayout:
    """Constraint-based auto-layout system."""
    
    def __init__(self, width: int, height: int):
        """
        Initialize auto layout.
        
        Args:
            width: Container width
            height: Container height
        """
        self.width = width
        self.height = height
    
    def apply_constraints(self, widgets: List[Any], constraints: List[LayoutConstraints]) -> None:
        """
        Apply constraints to widgets.
        
        Args:
            widgets: List of widgets
            constraints: List of constraints (one per widget)
        """
        for widget, constraint in zip(widgets, constraints):
            self._apply_constraint(widget, constraint)
    
    def _apply_constraint(self, widget: Any, constraint: LayoutConstraints) -> None:
        """Apply single constraint to widget."""
        # Apply width/height constraints
        if constraint.width is not None:
            widget.width = constraint.width
        if constraint.height is not None:
            widget.height = constraint.height
        
        # Apply min/max constraints
        if constraint.min_width is not None:
            widget.width = max(widget.width, constraint.min_width)
        if constraint.max_width is not None:
            widget.width = min(widget.width, constraint.max_width)
        if constraint.min_height is not None:
            widget.height = max(widget.height, constraint.min_height)
        if constraint.max_height is not None:
            widget.height = min(widget.height, constraint.max_height)
        
        # Calculate position based on anchors
        x = 0
        y = 0
        
        if constraint.anchor_x == "left":
            x = constraint.margin_left or constraint.margin
        elif constraint.anchor_x == "center":
            x = (self.width - widget.width) // 2
        elif constraint.anchor_x == "right":
            x = self.width - widget.width - (constraint.margin_right or constraint.margin)
        
        if constraint.anchor_y == "top":
            y = constraint.margin_top or constraint.margin
        elif constraint.anchor_y == "center":
            y = (self.height - widget.height) // 2
        elif constraint.anchor_y == "bottom":
            y = self.height - widget.height - (constraint.margin_bottom or constraint.margin)
        
        # Apply percentage positioning
        if constraint.percent_x is not None:
            x = int(self.width * constraint.percent_x / 100.0 - widget.width / 2.0)
        if constraint.percent_y is not None:
            y = int(self.height * constraint.percent_y / 100.0 - widget.height / 2.0)
        
        widget.x = int(x)
        widget.y = int(y)

