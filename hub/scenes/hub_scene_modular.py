"""Modular hub menu scene using UI framework and services."""

from typing import Optional, List
import pygame
from hub.scenes.base_scene_modular import BaseScene
from hub.ui import Button, Label, VContainer
from hub.ui.theme import ThemeManager
from hub.manager.game_registry import GameRegistry
from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, WHITE


class HubSceneModular(BaseScene):
    """Main menu hub scene with game selection using modular architecture."""
    
    def __init__(
        self,
        display_manager,
        input_service,
        event_bus,
        game_registry: GameRegistry
    ):
        """
        Initialize the modular hub scene.
        
        Args:
            display_manager: Display manager
            input_service: Input service
            event_bus: Event bus
            game_registry: Game registry for discovering games
        """
        super().__init__(display_manager, input_service, event_bus)
        self.game_registry = game_registry
        self.root_container: Optional[VContainer] = None
        self.title_label: Optional[Label] = None
        self.subtitle_label: Optional[Label] = None
        self.game_buttons: List[Button] = []
        self.instructions_label: Optional[Label] = None
    
    def init(self) -> None:
        """Initialize the hub scene."""
        # Get theme
        theme = ThemeManager.get_default_theme()
        
        # Create root container (no automatic layout, manual positioning)
        from hub.ui.container import Container
        self.root_container = Container(
            x=0,
            y=0,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            layout_manager=None  # No automatic layout
        )
        self.root_container.background_color = BACKGROUND_COLOR
        
        # Create title label (centered)
        title_label = Label(
            x=0,  # Will be centered
            y=100,
            text="8-Bit Game Hub",
            font_size=72,
            color=WHITE
        )
        title_label.x = SCREEN_WIDTH // 2 - title_label.width // 2
        self.title_label = title_label
        
        # Create subtitle label (centered)
        subtitle_label = Label(
            x=0,  # Will be centered
            y=180,
            text="Select a game to play",
            font_size=36,
            color=WHITE
        )
        subtitle_label.x = SCREEN_WIDTH // 2 - subtitle_label.width // 2
        self.subtitle_label = subtitle_label
        
        # Get all registered games from registry
        games = self.game_registry.get_all_games()
        
        # Create game buttons dynamically
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = SCREEN_HEIGHT // 2 - 50
        
        for i, game_metadata in enumerate(games):
            x = SCREEN_WIDTH // 2 - button_width // 2
            y = start_y + i * button_spacing
            
            # Create callback that switches to game scene
            def make_callback(scene_name: str):
                return lambda: self.switch_scene(scene_name)
            
            button = Button(
                x=x,
                y=y,
                width=button_width,
                height=button_height,
                text=game_metadata.display_name,
                callback=make_callback(game_metadata.name),
                event_bus=self.event_bus,
                theme=theme
            )
            self.game_buttons.append(button)
            self.root_container.add_child(button)
        
        # Create instructions label (centered)
        instructions_label = Label(
            x=0,  # Will be centered
            y=SCREEN_HEIGHT - 30,
            text="Press ESC to quit",
            font_size=24,
            color=WHITE
        )
        instructions_label.x = SCREEN_WIDTH // 2 - instructions_label.width // 2
        self.instructions_label = instructions_label
        
        # Add labels to container
        self.root_container.add_child(self.title_label)
        self.root_container.add_child(self.subtitle_label)
        self.root_container.add_child(self.instructions_label)
    
    def update(self, dt: float) -> None:
        """Update the hub scene."""
        if not self.root_container:
            return
        
        # Get mouse state from input service
        mouse_pos = self.input_service.get_mouse_pos()
        mouse_clicked = self.input_service.is_mouse_button_clicked(0)
        
        # Update root container (which updates all children)
        self.root_container.update(dt, mouse_pos, mouse_clicked)
    
    def render(self) -> None:
        """Render the hub scene."""
        # Fill background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Render root container (which renders all children)
        if self.root_container:
            self.root_container.render(self.screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events."""
        super().handle_event(event)
        # Input service is updated by scene manager, so we don't need to do anything here
        # The update() method handles mouse clicks via input service

