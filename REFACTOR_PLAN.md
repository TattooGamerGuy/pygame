# Modular Refactoring Plan

## Overview
Complete modular refactoring of the game hub to separate concerns, improve maintainability, and enable easier extension.

## Target Architecture

```
hub/
├── core/                      # Core engine systems
│   ├── __init__.py
│   ├── engine.py              # Main engine orchestrator
│   ├── display.py             # Display/window management
│   ├── audio.py               # Audio system
│   └── clock.py               # Frame timing and clock management
│
├── manager/                   # Management systems
│   ├── __init__.py
│   ├── scene_manager.py       # Scene lifecycle and transitions
│   ├── game_registry.py       # Game discovery and registration
│   └── asset_manager.py       # Enhanced asset management
│
├── services/                  # Service layer
│   ├── __init__.py
│   ├── input_service.py       # Centralized input handling
│   ├── audio_service.py       # Audio playback service
│   └── config_service.py       # Configuration management
│
├── events/                    # Event system
│   ├── __init__.py
│   ├── event_bus.py            # Event bus for pub/sub
│   └── events.py               # Event type definitions
│
├── ui/                        # UI framework
│   ├── __init__.py
│   ├── base_widget.py         # Base widget class
│   ├── button.py              # Button widget
│   ├── label.py               # Text label widget
│   ├── container.py           # Container/layout widget
│   └── theme.py               # UI theming system
│
├── scenes/                    # Scene implementations
│   ├── __init__.py
│   ├── base_scene.py          # Base scene interface
│   ├── hub_scene.py           # Main menu scene
│   └── transition.py          # Scene transition effects
│
├── games/                      # Game implementations
│   ├── __init__.py
│   ├── base_game.py           # Base game interface
│   ├── registry.py            # Game metadata and registration
│   └── [game files]           # Individual games
│
├── config/                    # Configuration
│   ├── __init__.py
│   ├── settings.py            # Application settings
│   └── defaults.py            # Default configuration values
│
└── main.py                    # Slim entry point

```

## Module Responsibilities

### Core Module
- **engine.py**: Orchestrates all systems, main game loop
- **display.py**: Window creation, resolution, fullscreen management
- **audio.py**: Audio initialization, mixer management
- **clock.py**: Frame timing, delta time calculation, FPS limiting

### Manager Module
- **scene_manager.py**: Scene lifecycle, transitions, state management
- **game_registry.py**: Game discovery (scan games/), metadata, registration
- **asset_manager.py**: Asset loading, caching, preloading

### Services Module
- **input_service.py**: Centralized keyboard/mouse/joystick input
- **audio_service.py**: Sound/music playback with volume control
- **config_service.py**: Settings persistence, file loading

### Events Module
- **event_bus.py**: Publisher/subscriber pattern for decoupled communication
- **events.py**: Event type definitions (SceneChangeEvent, GameStartEvent, etc.)

### UI Module
- **base_widget.py**: Abstract widget base with layout system
- **button.py**: Interactive button component
- **label.py**: Text rendering component
- **container.py**: Layout containers (vertical, horizontal, grid)
- **theme.py**: Centralized styling and theming

### Games Module
- **registry.py**: Game metadata, auto-discovery, registration decorator
- Games auto-register themselves via decorator

## Key Improvements

1. **Separation of Concerns**: Each module has single responsibility
2. **Dependency Injection**: Services passed to components, not global
3. **Event-Driven**: Components communicate via event bus
4. **Plugin System**: Games auto-discover and register
5. **Configuration**: Centralized settings with file support
6. **Testability**: Each module can be tested independently
7. **Extensibility**: Easy to add new games, UI components, services

## Implementation Order

1. Core engine modules (display, audio, clock)
2. Event system (event bus)
3. Service layer (input, audio, config)
4. Manager modules (scene, game registry)
5. UI framework
6. Refactor scenes and games to use new modules
7. Refactor main.py

## Migration Strategy

- Keep old code working during refactor
- Migrate one module at a time
- Test after each module migration
- Old imports will gradually be replaced

