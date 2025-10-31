"""Scene management system."""

from typing import Dict, Optional
from hub.scenes.base_scene import BaseScene
from hub.events.event_bus import EventBus
from hub.events.events import SceneChangeEvent, QuitEvent


class SceneManager:
    """Manages scene lifecycle and transitions."""
    
    def __init__(self, event_bus: EventBus):
        """
        Initialize scene manager.
        
        Args:
            event_bus: Event bus for scene change events
        """
        self.event_bus = event_bus
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.initial_scene: Optional[str] = None
        
        # Subscribe to events
        self.event_bus.subscribe("scene_change", self._handle_scene_change_event)
        self.event_bus.subscribe("quit", self._handle_quit_event)
    
    def register_scene(self, name: str, scene: BaseScene, is_initial: bool = False) -> None:
        """
        Register a scene.
        
        Args:
            name: Scene name/identifier
            scene: Scene instance
            is_initial: Whether this should be the initial scene
        """
        self.scenes[name] = scene
        
        if is_initial or self.current_scene is None:
            self.initial_scene = name
            self.current_scene = scene
            if not scene.init():
                scene.init()
    
    def switch_scene(self, scene_name: str) -> None:
        """
        Switch to a different scene.
        
        Args:
            scene_name: Name of scene to switch to
        """
        if scene_name not in self.scenes:
            print(f"Warning: Scene '{scene_name}' not found")
            return
        
        # Cleanup current scene
        if self.current_scene:
            self.current_scene.cleanup()
        
        # Switch to new scene
        self.current_scene = self.scenes[scene_name]
        self.current_scene.init()
        
        # Publish event
        self.event_bus.publish(SceneChangeEvent(scene_name))
    
    def _handle_scene_change_event(self, event: SceneChangeEvent) -> None:
        """Handle scene change event."""
        self.switch_scene(event.scene_name)
    
    def _handle_quit_event(self, event: QuitEvent) -> None:
        """Handle quit event."""
        if self.current_scene:
            self.current_scene.cleanup()
    
    def get_current_scene(self) -> Optional[BaseScene]:
        """Get current scene."""
        return self.current_scene
    
    def update(self, dt: float) -> None:
        """
        Update current scene.
        
        Args:
            dt: Delta time
        """
        if self.current_scene:
            self.current_scene.update(dt)
            
            # Check for scene transitions
            next_scene = self.current_scene.get_next_scene()
            if next_scene:
                self.switch_scene(next_scene)
    
    def handle_event(self, event) -> None:
        """
        Handle pygame event in current scene.
        
        Args:
            event: Pygame event
        """
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def render(self) -> None:
        """Render current scene."""
        if self.current_scene:
            self.current_scene.render()
    
    def cleanup(self) -> None:
        """Cleanup all scenes."""
        for scene in self.scenes.values():
            scene.cleanup()
        self.scenes.clear()
        self.current_scene = None

