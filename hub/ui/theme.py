"""Enhanced theming system for UI components."""

import json
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, Optional, List, Callable
from hub.ui.animation import Tween, Easing, AnimationState


@dataclass
class Theme:
    """UI theme definition."""
    name: str
    background_color: Tuple[int, int, int] = (100, 100, 100)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    hover_color: Tuple[int, int, int] = (150, 150, 150)
    active_color: Tuple[int, int, int] = (200, 200, 200)
    disabled_color: Tuple[int, int, int] = (50, 50, 50)
    border_color: Tuple[int, int, int] = (0, 0, 0)
    border_width: int = 2
    font_size: int = 24
    font_family: Optional[str] = None
    font_fallback: Optional[List[str]] = None
    
    def __post_init__(self):
        """Post-initialization validation."""
        # Clamp color values to 0-255
        self.background_color = self._clamp_color(self.background_color)
        self.text_color = self._clamp_color(self.text_color)
        self.hover_color = self._clamp_color(self.hover_color)
        self.active_color = self._clamp_color(self.active_color)
        self.disabled_color = self._clamp_color(self.disabled_color)
        self.border_color = self._clamp_color(self.border_color)
        
        # Ensure font size is reasonable
        self.font_size = max(8, self.font_size)
        
        # Initialize font fallback if not provided
        if self.font_fallback is None:
            self.font_fallback = []
    
    def _clamp_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Clamp color values to 0-255."""
        return tuple(max(0, min(255, c)) for c in color)
    
    def get_color_palette(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Get theme color palette.
        
        Returns:
            Dictionary of color names to RGB tuples
        """
        return {
            "background": self.background_color,
            "text": self.text_color,
            "hover": self.hover_color,
            "active": self.active_color,
            "disabled": self.disabled_color,
            "border": self.border_color
        }
    
    def set_color(self, color_name: str, color: Tuple[int, int, int]) -> None:
        """
        Set theme color.
        
        Args:
            color_name: Name of color to set (with or without _color suffix)
            color: RGB color tuple
        """
        color = self._clamp_color(color)
        
        # Handle both "background" and "background_color" formats
        if not color_name.endswith("_color"):
            color_name = f"{color_name}_color"
        
        # Use object.__setattr__ for dataclass frozen fields
        if color_name == "background_color":
            object.__setattr__(self, 'background_color', color)
        elif color_name == "text_color":
            object.__setattr__(self, 'text_color', color)
        elif color_name == "hover_color":
            object.__setattr__(self, 'hover_color', color)
        elif color_name == "active_color":
            object.__setattr__(self, 'active_color', color)
        elif color_name == "disabled_color":
            object.__setattr__(self, 'disabled_color', color)
        elif color_name == "border_color":
            object.__setattr__(self, 'border_color', color)
    
    def generate_gradient(self, start_color_name: str, end_color_name: str, steps: int) -> List[Tuple[int, int, int]]:
        """
        Generate color gradient between two theme colors.
        
        Args:
            start_color_name: Name of start color
            end_color_name: Name of end color
            steps: Number of gradient steps
            
        Returns:
            List of color tuples
        """
        start_color = getattr(self, start_color_name, self.background_color)
        end_color = getattr(self, end_color_name, self.hover_color)
        
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0.0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            gradient.append(self._clamp_color((r, g, b)))
        
        return gradient
    
    def get_responsive_font_size(self, resolution: Tuple[int, int]) -> int:
        """
        Get responsive font size based on resolution.
        
        Args:
            resolution: Screen resolution (width, height)
            
        Returns:
            Adjusted font size
        """
        width, height = resolution
        base_resolution = 1920  # Base desktop resolution
        
        # Scale font size based on width (mobile-friendly)
        scale_factor = min(width / base_resolution, 1.0)
        scaled_size = int(self.font_size * scale_factor)
        
        # Ensure minimum readable size
        return max(12, scaled_size)
    
    def copy(self, new_name: str, **overrides) -> 'Theme':
        """
        Copy theme with optional modifications.
        
        Args:
            new_name: Name for new theme
            **overrides: Color or property overrides
            
        Returns:
            New Theme instance
        """
        theme_dict = asdict(self)
        theme_dict["name"] = new_name
        theme_dict.update(overrides)
        return Theme(**theme_dict)
    
    def to_dict(self) -> Dict:
        """
        Convert theme to dictionary.
        
        Returns:
            Theme as dictionary
        """
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'Theme':
        """
        Create theme from dictionary.
        
        Args:
            data: Theme data dictionary
            
        Returns:
            Theme instance
        """
        # Convert lists to tuples for colors
        for key in ["background_color", "text_color", "hover_color", "active_color", 
                   "disabled_color", "border_color"]:
            if key in data and isinstance(data[key], list):
                data[key] = tuple(data[key])
        
        return Theme(**data)
    
    def to_json(self) -> str:
        """
        Convert theme to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict())
    
    @staticmethod
    def from_json(json_str: str) -> 'Theme':
        """
        Create theme from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            Theme instance
        """
        data = json.loads(json_str)
        return Theme.from_dict(data)


class ThemePreset:
    """Theme preset factory."""
    
    @staticmethod
    def light() -> Theme:
        """Create light theme preset."""
        return Theme(
            name="light",
            background_color=(240, 240, 240),
            text_color=(30, 30, 30),
            hover_color=(220, 220, 220),
            active_color=(200, 200, 200),
            disabled_color=(180, 180, 180),
            border_color=(100, 100, 100),
            border_width=2,
            font_size=24
        )
    
    @staticmethod
    def dark() -> Theme:
        """Create dark theme preset."""
        return Theme(
            name="dark",
            background_color=(20, 20, 20),
            text_color=(255, 255, 255),
            hover_color=(60, 60, 60),
            active_color=(100, 100, 100),
            disabled_color=(30, 30, 30),
            border_color=(255, 255, 255),
            border_width=1,
            font_size=24
        )
    
    @staticmethod
    def retro() -> Theme:
        """Create retro theme preset."""
        return Theme(
            name="retro",
            background_color=(50, 50, 50),
            text_color=(255, 255, 0),
            hover_color=(100, 100, 0),
            active_color=(150, 150, 0),
            disabled_color=(25, 25, 25),
            border_color=(255, 255, 0),
            border_width=3,
            font_size=20
        )
    
    @staticmethod
    def modern() -> Theme:
        """Create modern theme preset."""
        return Theme(
            name="modern",
            background_color=(30, 30, 40),
            text_color=(240, 240, 250),
            hover_color=(50, 50, 70),
            active_color=(70, 100, 150),
            disabled_color=(20, 20, 25),
            border_color=(100, 120, 150),
            border_width=1,
            font_size=22
        )


class ThemeManager:
    """Manages UI themes with enhanced functionality."""
    
    _themes: Dict[str, Theme] = {}
    _default_theme: Optional[Theme] = None
    _current_theme: Optional[Theme] = None
    _on_theme_change: Optional[Callable[[Theme], None]] = None
    _transition_tween: Optional[Tween] = None
    _transition_source: Optional[Theme] = None
    _transition_target: Optional[Theme] = None
    
    @classmethod
    def register_theme(cls, theme: Theme, is_default: bool = False) -> None:
        """
        Register a theme.
        
        Args:
            theme: Theme to register
            is_default: Whether this is the default theme
        """
        cls._themes[theme.name] = theme
        if is_default or cls._default_theme is None:
            cls._default_theme = theme
        if cls._current_theme is None:
            cls._current_theme = theme
    
    @classmethod
    def get_theme(cls, name: str) -> Optional[Theme]:
        """
        Get a theme by name.
        
        Args:
            name: Theme name
            
        Returns:
            Theme or None if not found
        """
        return cls._themes.get(name)
    
    @classmethod
    def get_all_themes(cls) -> Dict[str, Theme]:
        """
        Get all registered themes.
        
        Returns:
            Dictionary of theme names to themes
        """
        return cls._themes.copy()
    
    @classmethod
    def get_default_theme(cls) -> Theme:
        """
        Get the default theme.
        
        Returns:
            Default theme
        """
        if cls._default_theme is None:
            cls._default_theme = Theme(name="default")
            cls.register_theme(cls._default_theme, is_default=True)
        return cls._default_theme
    
    @classmethod
    def get_current_theme(cls) -> Theme:
        """
        Get current theme.
        
        Returns:
            Current theme
        """
        if cls._current_theme is None:
            return cls.get_default_theme()
        return cls._current_theme
    
    @classmethod
    def set_current_theme(cls, theme_name: str, animated: bool = False, duration: float = 0.5, apply_globally: bool = False) -> None:
        """
        Set current theme.
        
        Args:
            theme_name: Name of theme to set
            animated: Whether to animate transition
            duration: Animation duration
            apply_globally: Whether to apply to all widgets
        """
        target_theme = cls.get_theme(theme_name)
        if target_theme is None:
            return
        
        source_theme = cls._current_theme or cls.get_default_theme()
        
        if not animated:
            cls._current_theme = target_theme
            if cls._on_theme_change:
                cls._on_theme_change(target_theme)
        else:
            # Start animated transition
            cls._transition_source = source_theme
            cls._transition_target = target_theme
            
            # Create interpolated theme for transition
            transition_theme = source_theme.copy("transition")
            
            def update_theme(progress: float):
                # Interpolate colors
                for attr in ["background_color", "text_color", "hover_color", 
                           "active_color", "disabled_color", "border_color"]:
                    src = getattr(source_theme, attr)
                    tgt = getattr(target_theme, attr)
                    interp = tuple(
                        int(src[i] + (tgt[i] - src[i]) * progress)
                        for i in range(3)
                    )
                    setattr(transition_theme, attr, interp)
                
                # Interpolate numeric values
                transition_theme.font_size = int(
                    source_theme.font_size + 
                    (target_theme.font_size - source_theme.font_size) * progress
                )
                transition_theme.border_width = int(
                    source_theme.border_width + 
                    (target_theme.border_width - source_theme.border_width) * progress
                )
                
                cls._current_theme = transition_theme
                if cls._on_theme_change:
                    cls._on_theme_change(transition_theme)
            
            cls._transition_tween = Tween(
                start_value=0.0,
                end_value=1.0,
                duration=duration,
                easing=Easing.ease_in_out,
                on_update=update_theme,
                on_complete=lambda: cls._finalize_transition(target_theme)
            )
            cls._transition_tween.start()
    
    @classmethod
    def _finalize_transition(cls, target_theme: Theme) -> None:
        """Finalize theme transition."""
        cls._current_theme = target_theme
        cls._transition_tween = None
        cls._transition_source = None
        cls._transition_target = None
    
    @classmethod
    def is_transitioning(cls) -> bool:
        """
        Check if theme is currently transitioning.
        
        Returns:
            True if transitioning
        """
        return cls._transition_tween is not None and cls._transition_tween.state == AnimationState.RUNNING
    
    @classmethod
    def update_transition(cls, dt: float) -> None:
        """
        Update theme transition.
        
        Args:
            dt: Delta time
        """
        if cls._transition_tween and cls._transition_tween.state == AnimationState.RUNNING:
            cls._transition_tween.update(dt)
    
    @classmethod
    def initialize_defaults(cls) -> None:
        """Initialize default themes."""
        # Register presets
        cls.register_theme(ThemePreset.light())
        cls.register_theme(ThemePreset.dark())
        cls.register_theme(ThemePreset.retro())
        cls.register_theme(ThemePreset.modern())
        
        # Set default theme
        default = Theme(
            name="default",
            background_color=(100, 100, 100),
            text_color=(255, 255, 255),
            hover_color=(150, 150, 150),
            active_color=(200, 200, 200),
            disabled_color=(50, 50, 50),
            border_color=(0, 0, 0),
            border_width=2,
            font_size=24
        )
        cls.register_theme(default, is_default=True)
    
    @classmethod
    def get_on_theme_change(cls) -> Optional[Callable[[Theme], None]]:
        """Get theme change callback."""
        return cls._on_theme_change
    
    @classmethod
    def set_on_theme_change(cls, callback: Optional[Callable[[Theme], None]]) -> None:
        """Set theme change callback."""
        cls._on_theme_change = callback


# Initialize default themes
ThemeManager.initialize_defaults()
