# Pong Game - Modular Architecture

Professional modular directory structure for the Pong game implementation.

## Directory Structure

```
pong/
├── __init__.py              # Module exports
├── constants.py              # Game constants and configuration
├── game/                     # Game logic and main class
│   ├── __init__.py
│   └── game.py              # PongGameModular main class
├── components/              # Game entities/components
│   ├── __init__.py
│   ├── paddle.py            # Paddle component
│   └── ball.py              # Ball component
└── ai/                      # AI controllers
    ├── __init__.py
    └── paddle_ai.py         # AI controller for paddle
```

## Module Descriptions

### `constants.py`
Game configuration constants:
- `PADDLE_WIDTH`, `PADDLE_HEIGHT`, `PADDLE_SPEED`
- `BALL_RADIUS`, `BALL_SPEED`
- `WIN_SCORE`

### `game/game.py`
Main game class (`PongGameModular`) that:
- Manages game state
- Handles input
- Updates game entities
- Renders game scene
- Manages scoring and win conditions

### `components/`
Game entities/components:
- **paddle.py**: Paddle entity with movement and rendering
- **ball.py**: Ball entity with physics, collision detection, and rendering

### `ai/`
AI controllers:
- **paddle_ai.py**: AI controller that makes paddle follow the ball

## Architecture Principles

1. **Separation of Concerns**: Game logic, components, and AI are separated
2. **Dependency Injection**: Game receives services via constructor
3. **Modularity**: Each component is self-contained
4. **Testability**: Components can be tested independently
5. **Extensibility**: Easy to add new AI strategies or components

## Usage

```python
from hub.games.pong import PongGameModular

game = PongGameModular(
    display_manager,
    input_service,
    audio_service,
    event_bus
)
```

## Extending

### Adding a New AI Strategy

1. Create a new AI class in `ai/` directory
2. Implement the same interface as `PaddleAI`
3. Use in `game.py`

### Adding New Components

1. Create component class in `components/`
2. Add to `components/__init__.py`
3. Use in `game.py`

