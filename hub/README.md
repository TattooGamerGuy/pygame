# 8-Bit Game Hub

A retro game hub featuring 5 classic 8-bit games built with Pygame.

## Games Included

1. **Tetris** - Classic falling block puzzle game
2. **Snake** - Grow your snake by eating food
3. **Pong** - Classic paddle game (player vs AI)
4. **Space Invaders** - Shoot down waves of enemies
5. **Pac-Man** - Navigate mazes and collect dots while avoiding ghosts

## Installation

1. Install Python 3.6 or higher
2. Install pygame:
   ```bash
   pip install -r requirements.txt
   ```

## Running

From the project root directory:

```bash
python -m hub.main
```

Or:

```bash
python hub/main.py
```

## Controls

### Hub Menu
- Mouse: Click buttons to select games
- ESC: Quit

### General Game Controls
- ESC: Return to hub (from game over screen) or quit
- P: Pause/Unpause (in most games)
- R: Restart (when game over)

### Game-Specific Controls

**Tetris**
- Arrow Keys: Move/rotate piece
- Down Arrow: Fast fall

**Snake**
- Arrow Keys: Change direction

**Pong**
- W/Up Arrow or S/Down Arrow: Move paddle

**Space Invaders**
- Arrow Keys: Move ship
- Space: Shoot

**Pac-Man**
- Arrow Keys: Move

## Architecture

The game hub uses a scene-based architecture:

- `scenes/`: Scene management (hub menu, base scene classes)
- `games/`: Individual game implementations
- `utils/`: Shared utilities (constants, asset manager, input handler)

Each game inherits from `BaseGame` which provides common functionality like:
- Score tracking
- High score persistence
- Pause functionality
- Game over handling

## Project Structure

```
hub/
├── main.py                 # Entry point
├── scenes/                 # Scene management
│   ├── base_scene.py
│   ├── hub_scene.py
│   └── game_overlay.py
├── games/                  # Game implementations
│   ├── base_game.py
│   ├── tetris.py
│   ├── snake.py
│   ├── pong.py
│   ├── space_invaders.py
│   └── pacman.py
├── utils/                  # Utilities
│   ├── constants.py
│   ├── asset_manager.py
│   └── input_handler.py
└── assets/                 # Game assets
    ├── fonts/
    ├── sounds/
    └── images/
```

## Performance

The game hub targets 60 FPS. All games use delta-time based movement for smooth gameplay.

## License

This project is part of the pygame-hub repository.

