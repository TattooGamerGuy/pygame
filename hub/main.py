"""Main entry point for the 8-bit Game Hub."""

import sys
from typing import Optional
import pygame
from hub.utils.constants import SCREEN_SIZE, TARGET_FPS
from hub.scenes.base_scene import BaseScene
from hub.scenes.hub_scene import HubScene
from hub.games.pong import PongGame
from hub.games.snake import SnakeGame
from hub.games.space_invaders import SpaceInvadersGame
from hub.games.space_invaders.menu import SpaceInvadersMenuScene
from hub.games.tetris import TetrisGame
from hub.games.pacman import PacManGame


class GameHub:
    """Main game hub application."""
    
    def __init__(self):
        """Initialize the game hub."""
        pygame.init()
        
        # Initialize display
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("8-Bit Game Hub")
        
        # Initialize audio
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Warning: Audio initialization failed")
        
        # Initialize font
        pygame.font.init()
        
        # Scene management
        self.current_scene: Optional[BaseScene] = None
        self.scenes: dict = {}
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Register all scenes
        self.register_scene("hub", HubScene(self.screen))
        self.register_scene("pong", PongGame(self.screen))
        self.register_scene("snake", SnakeGame(self.screen))
        # Register Space Invaders menu and game
        self.register_scene("space_invaders_menu", SpaceInvadersMenuScene(self.screen))
        self.register_scene("space_invaders", SpaceInvadersGame(self.screen))
        self.register_scene("tetris", TetrisGame(self.screen))
        self.register_scene("pacman", PacManGame(self.screen))
    
    def register_scene(self, name: str, scene: BaseScene) -> None:
        """
        Register a scene.
        
        Args:
            name: Scene name
            scene: Scene instance
        """
        self.scenes[name] = scene
        if self.current_scene is None:
            self.current_scene = scene
            scene.init()
    
    def run(self) -> None:
        """Run the main game loop."""
        last_time = pygame.time.get_ticks()
        
        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Cap delta time to prevent large jumps
            dt = min(dt, 0.1)
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_scene:
                    self.current_scene.handle_event(event)
            
            # Update current scene
            if self.current_scene:
                self.current_scene.update(dt)
            
            # Check for scene transitions
            if self.current_scene:
                next_scene_name = self.current_scene.get_next_scene()
                if next_scene_name:
                    self.switch_scene(next_scene_name)
                
                # Check for quit
                if self.current_scene.should_quit():
                    self.running = False
            
            # Render
            if self.current_scene:
                self.current_scene.render()
                pygame.display.flip()
            
            # Tick clock
            self.clock.tick(TARGET_FPS)
        
        # Cleanup
        self.cleanup()
    
    def switch_scene(self, scene_name: str) -> None:
        """
        Switch to a different scene.
        
        Args:
            scene_name: Name of scene to switch to
        """
        if scene_name in self.scenes:
            # Cleanup current scene
            if self.current_scene:
                self.current_scene.cleanup()
            
            # Switch to new scene
            self.current_scene = self.scenes[scene_name]
            self.current_scene.init()
        else:
            print(f"Warning: Scene '{scene_name}' not found")
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        if self.current_scene:
            self.current_scene.cleanup()
        pygame.quit()


def main():
    """Main entry point."""
    hub = GameHub()
    hub.run()
    sys.exit(0)


if __name__ == "__main__":
    main()

