"""Theming system for UI components."""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional


@dataclass
class Theme:
    """UI theme definition."""
    name: str
    background_color: Tuple[int, int, int]
    text_color: Tuple[int, int, int]
    hover_color: Tuple[int, int, int]
    active_color: Tuple[int, int, int]
    disabled_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int]
    border_width: int
    font_size: int
    
    def __init__(
        self,
        name: str = "default",
        background_color: Tuple[int, int, int] = (100, 100, 100),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        active_color: Tuple[int, int, int] = (200, 200, 200),
        disabled_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Tuple[int, int, int] = (0, 0, 0),
        border_width: int = 2,
        font_size: int = 24
    ):
        """Initialize theme."""
        self.name = name
        self.background_color = background_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.disabled_color = disabled_color
        self.border_color = border_color
        self.border_width = border_width
        self.font_size = font_size


class ThemeManager:
    """Manages UI themes."""
    
    _themes: Dict[str, Theme] = {}
    _default_theme: Optional[Theme] = None
    
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
    def get_default_theme(cls) -> Theme:
        """
        Get the default theme.
        
        Returns:
            Default theme
        """
        if cls._default_theme is None:
            cls._default_theme = Theme()
        return cls._default_theme
    
    @classmethod
    def initialize_defaults(cls) -> None:
        """Initialize default themes."""
        # Default theme
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
        
        # Dark theme
        dark = Theme(
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
        cls.register_theme(dark)
        
        # Retro theme
        retro = Theme(
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
        cls.register_theme(retro)


# Initialize default themes
ThemeManager.initialize_defaults()

