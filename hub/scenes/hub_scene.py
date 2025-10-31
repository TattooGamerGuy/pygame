"""Main hub menu scene."""

from typing import Optional
import pygame
from hub.scenes.base_scene import BaseScene
from hub.scenes.game_overlay import Button, render_text_centered
from hub.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, 
    WHITE, BUTTON_COLOR, BUTTON_HOVER_COLOR
)


class HubScene(BaseScene):
    """Main menu hub scene with game selection."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize the hub scene."""
        super().__init__(screen)
        self.buttons: list = []
        self.title_font: Optional[pygame.font.Font] = None
        self.button_font: Optional[pygame.font.Font] = None
        self.mouse_pos = (0, 0)
        self.mouse_clicked_this_frame = False
        
    def init(self) -> None:
        """Initialize the hub scene."""
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        
        # Game names
        games = [
            ("Tetris", "tetris"),
            ("Snake", "snake"),
            ("Pong", "pong"),
            ("Space Invaders", "space_invaders_menu"),  # Show menu first
            ("Pac-Man", "pacman"),
        ]
        
        # Create buttons
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = SCREEN_HEIGHT // 2 - 50
        
        for i, (display_name, scene_name) in enumerate(games):
            x = SCREEN_WIDTH // 2 - button_width // 2
            y = start_y + i * button_spacing
            
            def make_callback(scene: str):
                return lambda: self.switch_scene(scene)
            
            button = Button(
                x, y, button_width, button_height,
                display_name,
                self.button_font,
                callback=make_callback(scene_name),
                color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER_COLOR
            )
            self.buttons.append(button)
    
    def update(self, dt: float) -> None:
        """Update the hub scene."""
        # Update mouse position for hover states
        self.mouse_pos = pygame.mouse.get_pos()
        # Update button hover states (but not clicks, those are handled in handle_event)
        for button in self.buttons:
            button.update(self.mouse_pos, False)
    
    def render(self) -> None:
        """Render the hub scene."""
        # Fill background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Render title
        if self.title_font:
            render_text_centered(
                self.screen,
                "8-Bit Game Hub",
                self.title_font,
                100,
                WHITE
            )
        
        # Render subtitle
        if self.button_font:
            render_text_centered(
                self.screen,
                "Select a game to play",
                self.button_font,
                180,
                WHITE
            )
        
        # Render buttons
        for button in self.buttons:
            button.render(self.screen)
        
        # Render instructions
        if self.button_font:
            instructions = self.button_font.render(
                "Press ESC to quit",
                True,
                WHITE
            )
            instructions_rect = instructions.get_rect(
                centerx=SCREEN_WIDTH // 2,
                bottom=SCREEN_HEIGHT - 30
            )
            self.screen.blit(instructions, instructions_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events."""
        super().handle_event(event)
        
        # Update mouse position first
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            self.mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button clicked - check all buttons
            for button in self.buttons:
                button.update(self.mouse_pos, True)
        
        # Update button hover states on mouse motion
        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(self.mouse_pos, False)

