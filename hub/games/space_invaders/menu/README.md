# Space Invaders Menu

Main menu screen for Space Invaders game.

## Features

- **Animated Enemy Formation**: Preview of enemies with smooth movement
- **Space Background**: Starfield with gradient effect
- **High Score Display**: Shows your best score
- **Controls Information**: Clear instructions for gameplay
- **Blinking Start Prompt**: Eye-catching "PRESS SPACE" indicator

## Controls

- **SPACE or ENTER**: Start the game
- **ESC**: Return to main hub

## Structure

```
menu/
├── __init__.py          # Module exports
├── menu_scene.py        # Menu scene implementation
└── README.md            # This file
```

## Integration

The menu is registered in `main.py` as `space_invaders_menu` and is shown when selecting "Space Invaders" from the main hub. The menu scene transitions to `space_invaders` game scene when the player presses SPACE or ENTER.

