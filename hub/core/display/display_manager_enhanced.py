"""
Enhanced display and window management.

Supports multi-monitor, window management, VSync options, resolution scaling,
and various display modes.
"""

from typing import Tuple, Optional, List, Dict, Callable
from enum import Enum
import pygame
from hub.config.defaults import DEFAULT_RESOLUTION, DEFAULT_WINDOW_TITLE


class DisplayMode(Enum):
    """Display mode options."""
    WINDOWED = "windowed"
    FULLSCREEN = "fullscreen"
    BORDERLESS_FULLSCREEN = "borderless_fullscreen"


class ScalingMode(Enum):
    """Resolution scaling modes."""
    STRETCH = "stretch"  # Stretch to fill (may distort)
    LETTERBOX = "letterbox"  # Maintain aspect ratio with black bars
    INTEGER_SCALE = "integer_scale"  # Scale by integer factors only
    FIT = "fit"  # Fit to screen maintaining aspect ratio


class VSyncMode(Enum):
    """VSync modes."""
    OFF = "off"
    ON = "on"
    ADAPTIVE = "adaptive"  # Adaptive sync (if supported)


class EnhancedDisplayManager:
    """Enhanced display manager with advanced features."""
    
    def __init__(
        self,
        size: Tuple[int, int] = DEFAULT_RESOLUTION,
        title: str = DEFAULT_WINDOW_TITLE,
        display_mode: DisplayMode = DisplayMode.WINDOWED,
        vsync: VSyncMode = VSyncMode.OFF,
        scaling_mode: ScalingMode = ScalingMode.LETTERBOX
    ):
        """
        Initialize enhanced display manager.
        
        Args:
            size: Window size (width, height)
            title: Window title
            display_mode: Initial display mode
            vsync: VSync mode
            scaling_mode: Resolution scaling mode
        """
        self._size = size
        self._virtual_width = size[0]
        self._virtual_height = size[1]
        self._title = title
        self._current_mode = display_mode
        self._vsync_mode = vsync
        self._scaling_mode = scaling_mode
        self._current_display_index = 0
        
        self._screen: Optional[pygame.Surface] = None
        self._initialized = False
        
        # Window management
        self._min_width = 320
        self._min_height = 240
        self._max_width = None
        self._max_height = None
        
        # Callbacks
        self.on_resize: Optional[Callable[[Tuple[int, int]], None]] = None
        self.on_focus: Optional[Callable[[bool], None]] = None
        self.on_expose: Optional[Callable[[], None]] = None
        
        # Window state
        self._is_minimized = False
        self._is_maximized = False
    
    @property
    def min_width(self) -> int:
        """Get minimum width."""
        return self._min_width
    
    @min_width.setter
    def min_width(self, value: int) -> None:
        """Set minimum width."""
        self._min_width = max(1, value)
    
    @property
    def min_height(self) -> int:
        """Get minimum height."""
        return self._min_height
    
    @min_height.setter
    def min_height(self, value: int) -> None:
        """Set minimum height."""
        self._min_height = max(1, value)
    
    @property
    def max_width(self) -> Optional[int]:
        """Get maximum width."""
        return self._max_width
    
    @max_width.setter
    def max_width(self, value: Optional[int]) -> None:
        """Set maximum width."""
        self._max_width = value
    
    @property
    def max_height(self) -> Optional[int]:
        """Get maximum height."""
        return self._max_height
    
    @max_height.setter
    def max_height(self, value: Optional[int]) -> None:
        """Set maximum height."""
        self._max_height = value
    
    def initialize(self) -> None:
        """Initialize the display."""
        if self._initialized:
            return
        
        pygame.display.init()
        
        flags = self._get_display_flags()
        self._screen = pygame.display.set_mode(self._size, flags)
        pygame.display.set_caption(self._title)
        self._initialized = True
    
    def _get_display_flags(self) -> int:
        """Get pygame display flags for current settings."""
        flags = 0
        
        if self._current_mode == DisplayMode.FULLSCREEN:
            flags |= pygame.FULLSCREEN
        elif self._current_mode == DisplayMode.BORDERLESS_FULLSCREEN:
            flags |= pygame.FULLSCREEN | pygame.NOFRAME
        else:  # WINDOWED
            flags |= pygame.RESIZABLE
        
        # VSync is typically handled via pygame.display.set_mode() with vsync parameter
        # But pygame might not support all VSync modes directly
        
        return flags
    
    def cleanup(self) -> None:
        """Cleanup display resources."""
        if self._initialized:
            try:
                pygame.display.quit()
            except Exception:
                pass
            finally:
                self._initialized = False
                self._screen = None
    
    @property
    def screen(self) -> pygame.Surface:
        """Get the main screen surface."""
        if not self._initialized:
            raise RuntimeError("Display not initialized. Call initialize() first.")
        return self._screen
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get current window size."""
        if self._screen:
            return self._screen.get_size()
        return self._size
    
    @property
    def width(self) -> int:
        """Get window width."""
        return self.size[0]
    
    @property
    def height(self) -> int:
        """Get window height."""
        return self.size[1]
    
    @property
    def virtual_width(self) -> int:
        """Get virtual resolution width."""
        return self._virtual_width
    
    @property
    def virtual_height(self) -> int:
        """Get virtual resolution height."""
        return self._virtual_height
    
    @property
    def current_mode(self) -> DisplayMode:
        """Get current display mode."""
        return self._current_mode
    
    @property
    def is_fullscreen(self) -> bool:
        """Check if in fullscreen mode."""
        return self._current_mode in [DisplayMode.FULLSCREEN, DisplayMode.BORDERLESS_FULLSCREEN]
    
    @property
    def scaling_mode(self) -> ScalingMode:
        """Get current scaling mode."""
        return self._scaling_mode
    
    @property
    def vsync_mode(self) -> VSyncMode:
        """Get current VSync mode."""
        return self._vsync_mode
    
    @property
    def current_display_index(self) -> int:
        """Get current display index."""
        return self._current_display_index
    
    def set_title(self, title: str) -> None:
        """Set window title."""
        self._title = title
        if self._initialized:
            pygame.display.set_caption(title)
    
    def set_resolution(self, size: Tuple[int, int]) -> bool:
        """
        Set window resolution.
        
        Args:
            size: New resolution (width, height)
            
        Returns:
            True if successful
        """
        width, height = size
        
        # Apply constraints
        width = max(self._min_width, width)
        height = max(self._min_height, height)
        
        if self._max_width:
            width = min(width, self._max_width)
        if self._max_height:
            height = min(height, self._max_height)
        
        self._size = (width, height)
        
        if self._initialized:
            flags = self._get_display_flags()
            try:
                self._screen = pygame.display.set_mode(self._size, flags)
                self._handle_resize(self._size)
                return True
            except Exception:
                return False
        
        return True
    
    def resize(self, width: int, height: int) -> bool:
        """
        Resize window.
        
        Args:
            width: New width
            height: New height
            
        Returns:
            True if successful
        """
        return self.set_resolution((width, height))
    
    def set_display_mode(self, mode: DisplayMode) -> None:
        """
        Set display mode.
        
        Args:
            mode: Display mode to set
        """
        if self._current_mode == mode:
            return
        
        self._current_mode = mode
        
        if self._initialized:
            flags = self._get_display_flags()
            try:
                self._screen = pygame.display.set_mode(self._size, flags)
            except Exception:
                pass  # Graceful degradation
    
    def set_virtual_resolution(self, width: int, height: int) -> None:
        """
        Set virtual resolution (game logic resolution).
        
        Args:
            width: Virtual width
            height: Virtual height
        """
        self._virtual_width = max(1, width)
        self._virtual_height = max(1, height)
    
    def set_scaling_mode(self, mode: ScalingMode) -> None:
        """
        Set resolution scaling mode.
        
        Args:
            mode: Scaling mode
        """
        self._scaling_mode = mode
    
    def set_vsync(self, mode: VSyncMode) -> None:
        """
        Set VSync mode.
        
        Args:
            mode: VSync mode
        """
        self._vsync_mode = mode
        # Note: pygame's VSync support is limited, this sets the preference
    
    def toggle_vsync(self) -> None:
        """Toggle VSync on/off."""
        if self._vsync_mode == VSyncMode.OFF:
            self.set_vsync(VSyncMode.ON)
        else:
            self.set_vsync(VSyncMode.OFF)
    
    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        if self.is_fullscreen:
            self.set_display_mode(DisplayMode.WINDOWED)
        else:
            self.set_display_mode(DisplayMode.FULLSCREEN)
    
    def minimize(self) -> None:
        """Minimize window."""
        if self._initialized:
            pygame.display.iconify()
            self._is_minimized = True
    
    def maximize(self) -> None:
        """Maximize window."""
        # pygame doesn't have direct maximize, but we track state
        self._is_maximized = True
        self._is_minimized = False
    
    def restore(self) -> None:
        """Restore window."""
        if self._initialized and self._is_minimized:
            # pygame doesn't have direct restore
            self._is_minimized = False
    
    def get_available_displays(self) -> List[Dict]:
        """
        Get list of available displays.
        
        Returns:
            List of display info dictionaries
        """
        displays = []
        try:
            # pygame.display.get_driver() gives current driver
            # Full multi-monitor support requires platform-specific code
            # For now, return primary display info
            if self._initialized:
                size = self._screen.get_size() if self._screen else self._size
                displays.append({
                    'index': 0,
                    'width': size[0],
                    'height': size[1],
                    'primary': True
                })
            else:
                displays.append({
                    'index': 0,
                    'width': self._size[0],
                    'height': self._size[1],
                    'primary': True
                })
        except Exception:
            # Fallback
            displays.append({
                'index': 0,
                'width': 1920,
                'height': 1080,
                'primary': True
            })
        
        return displays
    
    def get_primary_display(self) -> Dict:
        """
        Get primary display information.
        
        Returns:
            Primary display info dictionary
        """
        displays = self.get_available_displays()
        for display in displays:
            if display.get('primary', False):
                return display
        return displays[0] if displays else {'index': 0, 'width': 1920, 'height': 1080, 'primary': True}
    
    def set_display(self, display_index: int) -> None:
        """
        Set active display (for multi-monitor).
        
        Args:
            display_index: Display index
        """
        self._current_display_index = display_index
        # Full implementation would require platform-specific code
    
    def get_scaling_ratio(self) -> Tuple[float, float]:
        """
        Get current scaling ratio.
        
        Returns:
            (scale_x, scale_y) tuple
        """
        if self._scaling_mode == ScalingMode.INTEGER_SCALE:
            scale_x = int(self.width / self._virtual_width)
            scale_y = int(self.height / self._virtual_height)
            return (float(max(1, scale_x)), float(max(1, scale_y)))
        elif self._scaling_mode == ScalingMode.LETTERBOX or self._scaling_mode == ScalingMode.FIT:
            scale_x = self.width / self._virtual_width
            scale_y = self.height / self._virtual_height
            scale = min(scale_x, scale_y)
            return (scale, scale)
        else:  # STRETCH
            return (self.width / self._virtual_width, self.height / self._virtual_height)
    
    def get_resolution_presets(self) -> List[Tuple[int, int]]:
        """
        Get common resolution presets.
        
        Returns:
            List of (width, height) tuples
        """
        return [
            (640, 480),   # VGA
            (800, 600),   # SVGA
            (1024, 768),  # XGA
            (1280, 720),  # HD
            (1280, 1024), # SXGA
            (1920, 1080), # Full HD
            (2560, 1440), # QHD
            (3840, 2160)  # 4K UHD
        ]
    
    def get_supported_resolutions(self) -> List[Tuple[int, int]]:
        """
        Get supported resolutions for current display.
        
        Returns:
            List of supported resolutions
        """
        # pygame doesn't provide this directly, return common presets
        return self.get_resolution_presets()
    
    def get_display_info(self) -> Dict:
        """
        Get current display information.
        
        Returns:
            Display info dictionary
        """
        return {
            'width': self.width,
            'height': self.height,
            'virtual_width': self._virtual_width,
            'virtual_height': self._virtual_height,
            'fullscreen': self.is_fullscreen,
            'mode': self._current_mode.value,
            'vsync': self._vsync_mode.value,
            'scaling_mode': self._scaling_mode.value
        }
    
    def save_state(self) -> Dict:
        """
        Save current display state.
        
        Returns:
            State dictionary
        """
        return {
            'width': self.width,
            'height': self.height,
            'virtual_width': self._virtual_width,
            'virtual_height': self._virtual_height,
            'mode': self._current_mode.value,  # Save as string value
            'vsync': self._vsync_mode.value,  # Save as string value
            'scaling_mode': self._scaling_mode.value,  # Save as string value
            'title': self._title
        }
    
    def restore_state(self, state: Dict) -> None:
        """
        Restore display state.
        
        Args:
            state: State dictionary from save_state()
        """
        if 'width' in state and 'height' in state:
            self.set_resolution((state['width'], state['height']))
        
        if 'virtual_width' in state and 'virtual_height' in state:
            self.set_virtual_resolution(state['virtual_width'], state['virtual_height'])
        
        if 'mode' in state:
            if isinstance(state['mode'], DisplayMode):
                self.set_display_mode(state['mode'])
            elif isinstance(state['mode'], str):
                self.set_display_mode(DisplayMode(state['mode']))
        
        if 'vsync' in state:
            if isinstance(state['vsync'], VSyncMode):
                self.set_vsync(state['vsync'])
            elif isinstance(state['vsync'], str):
                self.set_vsync(VSyncMode(state['vsync']))
        
        if 'scaling_mode' in state:
            if isinstance(state['scaling_mode'], ScalingMode):
                self.set_scaling_mode(state['scaling_mode'])
            elif isinstance(state['scaling_mode'], str):
                self.set_scaling_mode(ScalingMode(state['scaling_mode']))
        
        if 'title' in state:
            self.set_title(state['title'])
    
    def flip(self) -> None:
        """Update the display."""
        if self._initialized:
            pygame.display.flip()
    
    def _handle_resize(self, size: Tuple[int, int]) -> None:
        """Handle window resize event."""
        if self.on_resize:
            self.on_resize(size)
    
    def _handle_focus(self, focused: bool) -> None:
        """Handle window focus event."""
        if self.on_focus:
            self.on_focus(focused)
    
    def _handle_expose(self) -> None:
        """Handle window expose event."""
        if self.on_expose:
            self.on_expose()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame display events.
        
        Args:
            event: pygame event
        """
        if event.type == pygame.VIDEORESIZE:
            self._handle_resize(event.size)
            if self._screen:
                self._size = event.size
        elif event.type == pygame.ACTIVEEVENT:
            if event.gain == 0:  # Lost focus
                self._handle_focus(False)
            elif event.gain == 1:  # Gained focus
                self._handle_focus(True)

