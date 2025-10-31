# Space Invaders Game - Modular Architecture

Professional modular directory structure for the Space Invaders game implementation.

## Directory Structure

```
space_invaders/
├── __init__.py              # Module exports
├── constants.py              # Game constants and configuration
├── README.md                 # Documentation
├── game/                     # Game logic module
│   ├── __init__.py
│   └── game.py              # SpaceInvadersGameModular main class
└── components/              # Game entities/components
    ├── __init__.py
    ├── bullet.py            # Bullet component
    ├── enemy.py             # Enemy ship component
    └── player.py            # Player ship component
```

## Module Descriptions

### `constants.py`
Game configuration constants:
- Enemy formation: `ENEMY_ROWS`, `ENEMY_COLS`, spacing
- Speeds: `PLAYER_SPEED`, `ENEMY_SPEED`, bullet speeds
- Timers: `ENEMY_MOVE_INTERVAL`, `ENEMY_SHOOT_INTERVAL`
- Scoring: `ENEMY_SCORE`, `CLEAR_BONUS`

### `game/game.py`
Main game class (`SpaceInvadersGameModular`) that:
- Manages game state
- Handles input (movement, shooting)
- Updates all entities (player, enemies, bullets)
- Handles collision detection
- Manages enemy formation and AI
- Renders game scene

### `components/`
Game entities/components:
- **bullet.py**: Bullet entity with movement and rendering
- **enemy.py**: Enemy ship entity
- **player.py**: Player ship entity

## Architecture Principles

1. **Separation of Concerns**: Game logic, components separated
2. **Component-Based**: Each entity is a self-contained component
3. **Dependency Injection**: Game receives services via constructor
4. **Modularity**: Easy to add new enemy types or bullet types

