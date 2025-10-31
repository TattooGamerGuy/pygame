"""Modular main entry point for the 8-bit Game Hub."""

import sys
import pygame
from hub.core.engine import GameEngine
from hub.core.display import DisplayManager
from hub.core.audio import AudioManager
from hub.core.clock import ClockManager
from hub.events.event_bus import EventBus
from hub.events.events import QuitEvent
from hub.manager.scene_manager import SceneManager
from hub.manager.game_registry import GameRegistry
from hub.services.input_service import InputService
from hub.services.config_service import ConfigService
from hub.config.settings import Settings
from hub.scenes.hub_scene import HubScene
from hub.games.pong import PongGame
from hub.games.snake import SnakeGame
from hub.games.space_invaders import SpaceInvadersGame
from hub.games.tetris import TetrisGame
from hub.games.pacman import PacManGame


class ModularGameHub:
    """Modular game hub application."""
    
    def __init__(self):
        """Initialize the modular game hub."""
        # Load settings
        self.settings = Settings()
        
        # Create core systems
        display_manager = DisplayManager(
            size=tuple(self.settings.get('resolution', (1280, 720))),
            title="8-Bit Game Hub"
        )
        audio_manager = AudioManager()
        clock_manager = ClockManager(
            target_fps=self.settings.get('target_fps', 60)
        )
        
        # Create engine
        self.engine = GameEngine(display_manager, audio_manager, clock_manager)
        
        # Create event bus
        self.event_bus = EventBus()
        self.event_bus.subscribe("quit", self._handle_quit)
        
        # Create services
        self.input_service = InputService(self.event_bus)
        self.config_service = ConfigService(self.settings)
        
        # Apply configuration
        self.config_service.apply_to_display(display_manager)
        self.config_service.apply_to_audio(audio_manager)
        self.config_service.apply_to_clock(clock_manager)
        
        # Create managers
        self.scene_manager = SceneManager(self.event_bus)
        
        # Initialize engine
        self.engine.initialize()
        
        # Register scenes and games
        self._register_scenes()
        
        self.engine.running = True
    
    def _register_scenes(self) -> None:
        """Register all scenes with the scene manager."""
        screen = self.engine.display.screen
        
        # Register hub scene
        hub_scene = HubScene(screen)
        self.scene_manager.register_scene("hub", hub_scene, is_initial=True)
        
        # Register games
        self.scene_manager.register_scene("pong", PongGame(screen))
        self.scene_manager.register_scene("snake", SnakeGame(screen))
        self.scene_manager.register_scene("space_invaders", SpaceInvadersGame(screen))
        self.scene_manager.register_scene("tetris", TetrisGame(screen))
        self.scene_manager.register_scene("pacman", PacManGame(screen))
    
    def _handle_quit(self, event: QuitEvent) -> None:
        """Handle quit event."""
        self.engine.running = False
    
    def run(self) -> None:
        """Run the main game loop."""
        while self.engine.running:
            # Handle events
            events = pygame.event.get()
            self.input_service.update(events)
            
            for event in events:
                self.scene_manager.handle_event(event)
            
            # Update
            dt = self.engine.tick()
            self.scene_manager.update(dt)
            
            # Render
            self.scene_manager.render()
            self.engine.display.flip()
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.scene_manager.cleanup()
        self.settings.save()
        self.engine.cleanup()


def main():
    """Main entry point."""
    hub = ModularGameHub()
    hub.run()
    sys.exit(0)


if __name__ == "__main__":
    main()

