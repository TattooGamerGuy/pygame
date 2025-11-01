"""
Enhanced rendering system.

Supports render targets, shaders, particle systems, lighting, 
post-processing, and improved batching.
"""

from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field
import pygame
import math
import time


class ShaderType(Enum):
    """Shader types."""
    VERTEX = "vertex"
    FRAGMENT = "fragment"
    POST_PROCESS = "post_process"


class LightType(Enum):
    """Light types."""
    POINT = "point"
    DIRECTIONAL = "directional"
    SPOT = "spot"
    AMBIENT = "ambient"


class EffectType(Enum):
    """Post-processing effect types."""
    BLOOM = "bloom"
    BLUR = "blur"
    SHARPEN = "sharpen"
    COLOR_GRADING = "color_grading"
    VIGNETTE = "vignette"
    GRAIN = "grain"


@dataclass
class Particle:
    """Particle data."""
    position: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0)
    color: Tuple[int, int, int] = (255, 255, 255)
    size: float = 1.0
    lifetime: float = 1.0
    age: float = 0.0
    active: bool = True


class RenderTarget:
    """Offscreen render target."""
    
    def __init__(self, width: int, height: int):
        """Initialize render target."""
        self.width = width
        self.height = height
        self._surface = pygame.Surface((width, height))
        self._clear_color = (0, 0, 0)
    
    def clear(self, color: Tuple[int, int, int] = None) -> None:
        """Clear render target."""
        if color:
            self._clear_color = color
        self._surface.fill(self._clear_color)
    
    def get_surface(self) -> pygame.Surface:
        """Get underlying surface."""
        return self._surface
    
    def resize(self, width: int, height: int) -> None:
        """Resize render target."""
        self.width = width
        self.height = height
        self._surface = pygame.Surface((width, height))
        self.clear()


class Shader:
    """Shader wrapper (pygame has limited shader support)."""
    
    def __init__(self, name: str, shader_type: ShaderType):
        """Initialize shader."""
        self.name = name
        self.type = shader_type
        self._parameters: Dict[str, float] = {}
        self._enabled = False
        self._compiled = False
    
    def set_parameter(self, name: str, value: float) -> None:
        """Set shader parameter."""
        self._parameters[name] = value
    
    def get_parameter(self, name: str) -> Optional[float]:
        """Get shader parameter."""
        return self._parameters.get(name)
    
    def enable(self) -> None:
        """Enable shader."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable shader."""
        self._enabled = False
    
    @property
    def is_enabled(self) -> bool:
        """Check if shader is enabled."""
        return self._enabled
    
    def compile(self) -> bool:
        """Compile shader (placeholder for pygame)."""
        self._compiled = True
        return True


class ParticleSystem:
    """Advanced particle system."""
    
    def __init__(self, name: str):
        """Initialize particle system."""
        self.name = name
        self._particles: List[Particle] = []
        self._color = (255, 255, 255)
        self._lifetime = 1.0
        self._speed = 50.0
        self._spread = 360.0  # Degrees
        self._size_min = 1.0
        self._size_max = 5.0
        self._gravity = (0.0, 98.0)  # Gravity vector
    
    @property
    def particle_count(self) -> int:
        """Get active particle count."""
        return len([p for p in self._particles if p.active])
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get particle color."""
        return self._color
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Set particle color."""
        self._color = color
    
    @property
    def lifetime(self) -> float:
        """Get particle lifetime."""
        return self._lifetime
    
    def set_lifetime(self, lifetime: float) -> None:
        """Set particle lifetime."""
        self._lifetime = max(0.1, lifetime)
    
    @property
    def speed(self) -> float:
        """Get particle speed."""
        return self._speed
    
    def set_speed(self, speed: float) -> None:
        """Set particle speed."""
        self._speed = max(0.0, speed)
    
    def emit(self, count: int, position: Tuple[float, float]) -> None:
        """Emit particles."""
        for _ in range(count):
            particle = Particle()
            particle.position = position
            particle.color = self._color
            particle.lifetime = self._lifetime + (self._lifetime * 0.2 * (math.random() - 0.5) if hasattr(math, 'random') else 0)
            particle.size = self._size_min + (self._size_max - self._size_min) * 0.5
            
            # Random velocity
            angle = (self._spread / 180.0 * math.pi) * (2.0 * 0.5 - 1.0)  # Simplified
            speed = self._speed * (0.5 + 0.5 * 0.5)  # Simplified random
            particle.velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            self._particles.append(particle)
    
    def update(self, dt: float) -> None:
        """Update particles."""
        for particle in self._particles:
            if not particle.active:
                continue
            
            particle.age += dt
            
            # Check lifetime
            if particle.age >= particle.lifetime:
                particle.active = False
                continue
            
            # Update position
            dx = particle.velocity[0] * dt
            dy = particle.velocity[1] * dt
            if self._gravity:
                dy += self._gravity[1] * dt * dt
            particle.position = (
                particle.position[0] + dx,
                particle.position[1] + dy
            )
            
            # Update alpha based on lifetime
            alpha = 1.0 - (particle.age / particle.lifetime)
            # Color fading would be applied here
    
    def get_particles(self) -> List[Particle]:
        """Get active particles."""
        return [p for p in self._particles if p.active]
    
    def clear(self) -> None:
        """Clear all particles."""
        self._particles.clear()


class Light:
    """Light source."""
    
    def __init__(self, light_type: LightType, position: Tuple[float, float]):
        """Initialize light."""
        self.type = light_type
        self.position = position
        self._color = (255, 255, 255)
        self._intensity = 1.0
        self._radius = 100.0
        self._direction: Optional[Tuple[float, float]] = None
        self._enabled = True
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get light color."""
        return self._color
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Set light color."""
        self._color = color
    
    @property
    def intensity(self) -> float:
        """Get light intensity."""
        return self._intensity
    
    def set_intensity(self, intensity: float) -> None:
        """Set light intensity (0.0 to 1.0)."""
        self._intensity = max(0.0, min(1.0, intensity))
    
    @property
    def radius(self) -> float:
        """Get light radius."""
        return self._radius
    
    def set_radius(self, radius: float) -> None:
        """Set light radius."""
        self._radius = max(1.0, radius)
    
    @property
    def direction(self) -> Optional[Tuple[float, float]]:
        """Get light direction."""
        return self._direction
    
    def set_direction(self, direction: Tuple[float, float]) -> None:
        """Set light direction (for directional/spot lights)."""
        self._direction = direction
    
    def enable(self) -> None:
        """Enable light."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable light."""
        self._enabled = False
    
    @property
    def is_enabled(self) -> bool:
        """Check if light is enabled."""
        return self._enabled


class LightingSystem:
    """2D lighting system."""
    
    def __init__(self):
        """Initialize lighting system."""
        self._lights: List[Light] = []
        self._ambient_light = 0.2
    
    @property
    def ambient_light(self) -> float:
        """Get ambient light level."""
        return self._ambient_light
    
    def set_ambient_light(self, level: float) -> None:
        """Set ambient light level (0.0 to 1.0)."""
        self._ambient_light = max(0.0, min(1.0, level))
    
    def create_light(self, light_type: LightType, position: Tuple[float, float]) -> Light:
        """Create light."""
        light = Light(light_type, position)
        self._lights.append(light)
        return light
    
    def get_lights(self) -> List[Light]:
        """Get all lights."""
        return [l for l in self._lights if l.is_enabled]
    
    def clear_lights(self) -> None:
        """Clear all lights."""
        self._lights.clear()
    
    def calculate_lighting(
        self,
        position: Tuple[float, float],
        base_color: Tuple[int, int, int]
    ) -> Tuple[int, int, int]:
        """
        Calculate lighting at position.
        
        Args:
            position: Position to calculate lighting for
            base_color: Base color
            
        Returns:
            Lit color
        """
        # Simplified lighting calculation
        light_factor = self._ambient_light
        
        for light in self.get_lights():
            if light.type == LightType.POINT:
                dx = position[0] - light.position[0]
                dy = position[1] - light.position[1]
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance <= light.radius:
                    factor = 1.0 - (distance / light.radius)
                    light_factor += light.intensity * factor
        
        light_factor = min(1.0, light_factor)
        
        return (
            int(base_color[0] * light_factor),
            int(base_color[1] * light_factor),
            int(base_color[2] * light_factor)
        )


class PostProcessor:
    """Post-processing effects system."""
    
    def __init__(self):
        """Initialize post-processor."""
        self._active_effects: Set[EffectType] = set()
        self._effect_parameters: Dict[EffectType, Dict[str, float]] = {}
        self._effect_order: List[EffectType] = []
    
    @property
    def active_effects(self) -> Set[EffectType]:
        """Get active effects."""
        return self._active_effects.copy()
    
    @property
    def effect_order(self) -> List[EffectType]:
        """Get effect processing order."""
        return self._effect_order.copy()
    
    def add_effect(self, effect: EffectType) -> None:
        """Add post-processing effect."""
        if effect not in self._active_effects:
            self._active_effects.add(effect)
            self._effect_order.append(effect)
            self._effect_parameters[effect] = {}
    
    def remove_effect(self, effect: EffectType) -> None:
        """Remove post-processing effect."""
        if effect in self._active_effects:
            self._active_effects.remove(effect)
            if effect in self._effect_order:
                self._effect_order.remove(effect)
            if effect in self._effect_parameters:
                del self._effect_parameters[effect]
    
    def set_effect_parameter(self, effect: EffectType, name: str, value: float) -> None:
        """Set effect parameter."""
        if effect in self._active_effects:
            if effect not in self._effect_parameters:
                self._effect_parameters[effect] = {}
            self._effect_parameters[effect][name] = value
    
    def get_effect_parameter(self, effect: EffectType, name: str) -> Optional[float]:
        """Get effect parameter."""
        if effect in self._active_effects:
            return self._effect_parameters.get(effect, {}).get(name)
        return None
    
    def process(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Process surface with active effects.
        
        Args:
            surface: Input surface
            
        Returns:
            Processed surface
        """
        result = surface.copy()
        
        # Apply effects in order
        for effect in self._effect_order:
            if effect == EffectType.BLUR:
                # Simple blur (box blur approximation)
                pass  # Would apply blur here
            elif effect == EffectType.BLOOM:
                # Bloom effect
                pass  # Would apply bloom here
        
        return result


class LayerGroup:
    """Layer group for organizing layers."""
    
    def __init__(self, name: str):
        """Initialize layer group."""
        self.name = name
        self._visible = True
        self._opacity = 1.0
        self._order = 0
        self._layers: Set[int] = set()
    
    @property
    def is_visible(self) -> bool:
        """Check if group is visible."""
        return self._visible
    
    def set_visible(self, visible: bool) -> None:
        """Set visibility."""
        self._visible = visible
    
    @property
    def opacity(self) -> float:
        """Get opacity."""
        return self._opacity
    
    def set_opacity(self, opacity: float) -> None:
        """Set opacity (0.0 to 1.0)."""
        self._opacity = max(0.0, min(1.0, opacity))
    
    @property
    def order(self) -> int:
        """Get render order."""
        return self._order
    
    def set_order(self, order: int) -> None:
        """Set render order."""
        self._order = order
    
    def add_layer(self, layer: int) -> None:
        """Add layer to group."""
        self._layers.add(layer)
    
    def remove_layer(self, layer: int) -> None:
        """Remove layer from group."""
        self._layers.discard(layer)


class TextureAtlas:
    """Texture atlas for batching optimization."""
    
    def __init__(self, width: int, height: int):
        """Initialize texture atlas."""
        self.width = width
        self.height = height
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._textures: Dict[str, pygame.Rect] = {}
        self._current_x = 0
        self._current_y = 0
        self._row_height = 0
    
    def add_texture(self, name: str, surface: pygame.Surface) -> Optional[pygame.Rect]:
        """
        Add texture to atlas.
        
        Returns:
            Region rectangle or None if doesn't fit
        """
        sw, sh = surface.get_size()
        
        # Check if fits on current row
        if self._current_x + sw > self.width:
            # Move to next row
            self._current_x = 0
            self._current_y += self._row_height
            self._row_height = 0
        
        # Check if fits in atlas
        if self._current_y + sh > self.height:
            return None  # Doesn't fit
        
        # Add texture
        rect = pygame.Rect(self._current_x, self._current_y, sw, sh)
        self._surface.blit(surface, rect.topleft)
        self._textures[name] = rect
        
        self._current_x += sw
        self._row_height = max(self._row_height, sh)
        
        return rect
    
    def get_region(self, name: str) -> Optional[pygame.Rect]:
        """Get texture region."""
        return self._textures.get(name)
    
    @property
    def textures(self) -> Dict[str, pygame.Rect]:
        """Get all textures."""
        return self._textures.copy()
    
    def get_surface(self) -> pygame.Surface:
        """Get atlas surface."""
        return self._surface


class EnhancedRenderer:
    """Enhanced renderer with advanced features."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize enhanced renderer."""
        self.screen = screen
        self._current_target: Optional[RenderTarget] = None
        self._render_targets: Dict[str, RenderTarget] = {}
        self._shaders: Dict[str, Shader] = {}
        self._particle_systems: Dict[str, ParticleSystem] = {}
        self._lighting_system = LightingSystem()
        self._post_processor = PostProcessor()
        self._layer_groups: Dict[str, LayerGroup] = {}
        self._texture_atlases: Dict[str, TextureAtlas] = {}
        self._batch_stats = {
            'draw_calls': 0,
            'sprites_batched': 0,
            'textures_used': 0
        }
    
    def create_render_target(self, width: int, height: int, name: Optional[str] = None) -> RenderTarget:
        """Create render target."""
        target = RenderTarget(width, height)
        if name:
            self._render_targets[name] = target
        return target
    
    def set_render_target(self, target: Optional[RenderTarget]) -> None:
        """Set current render target (None = screen)."""
        self._current_target = target
    
    def get_render_target(self) -> Optional[RenderTarget]:
        """Get current render target."""
        return self._current_target
    
    def begin(self) -> None:
        """Begin rendering frame."""
        target = self._current_target if self._current_target else self.screen
        target.clear() if isinstance(target, RenderTarget) else target.fill((0, 0, 0))
        self._batch_stats = {
            'draw_calls': 0,
            'sprites_batched': 0,
            'textures_used': 0
        }
    
    def end(self) -> None:
        """End rendering frame."""
        target = self._current_target if self._current_target else self.screen
        surface = target.get_surface() if isinstance(target, RenderTarget) else target
        
        # Apply post-processing
        if self._post_processor.active_effects:
            surface = self._post_processor.process(surface)
            target_surface = target.get_surface() if isinstance(target, RenderTarget) else target
            target_surface.blit(surface, (0, 0))
        
        # Blit to screen if using render target
        if self._current_target:
            self.screen.blit(self._current_target.get_surface(), (0, 0))
        
        try:
            pygame.display.flip()
        except pygame.error:
            pass
    
    def draw_sprite(
        self,
        surface: pygame.Surface,
        position: Tuple[float, float],
        layer: int = 0,
        rotation: float = 0.0,
        scale: float = 1.0
    ) -> None:
        """Draw sprite."""
        target = self._current_target if self._current_target else self.screen
        target_surface = target.get_surface() if isinstance(target, RenderTarget) else target
        
        # Apply transformations
        if scale != 1.0:
            w, h = surface.get_size()
            surface = pygame.transform.scale(surface, (int(w * scale), int(h * scale)))
        
        if rotation != 0.0:
            surface = pygame.transform.rotate(surface, rotation)
        
        target_surface.blit(surface, position)
        self._batch_stats['draw_calls'] += 1
        self._batch_stats['sprites_batched'] += 1
    
    def create_shader(self, name: str, shader_type: ShaderType) -> Shader:
        """Create shader."""
        shader = Shader(name, shader_type)
        self._shaders[name] = shader
        return shader
    
    def create_particle_system(self, name: str) -> ParticleSystem:
        """Create particle system."""
        ps = ParticleSystem(name)
        self._particle_systems[name] = ps
        return ps
    
    def draw_particles(self, particle_system: ParticleSystem) -> None:
        """Draw particles."""
        target = self._current_target if self._current_target else self.screen
        target_surface = target.get_surface() if isinstance(target, RenderTarget) else target
        
        for particle in particle_system.get_particles():
            if not particle.active:
                continue
            
            # Draw simple particle (would use texture in real implementation)
            color = particle.color
            size = int(particle.size)
            if size > 0:
                pygame.draw.circle(target_surface, color, 
                                 (int(particle.position[0]), int(particle.position[1])), size)
    
    def get_lighting_system(self) -> LightingSystem:
        """Get lighting system."""
        return self._lighting_system
    
    def get_post_processor(self) -> PostProcessor:
        """Get post-processor."""
        return self._post_processor
    
    def create_layer_group(self, name: str) -> LayerGroup:
        """Create layer group."""
        group = LayerGroup(name)
        self._layer_groups[name] = group
        return group
    
    def create_texture_atlas(self, width: int, height: int, name: Optional[str] = None) -> TextureAtlas:
        """Create texture atlas."""
        atlas = TextureAtlas(width, height)
        if name:
            self._texture_atlases[name] = atlas
        return atlas
    
    def get_batch_stats(self) -> Dict[str, int]:
        """Get batch optimization statistics."""
        return self._batch_stats.copy()
    
    def save_state(self) -> Dict:
        """Save render state."""
        return {
            'ambient_light': self._lighting_system.ambient_light,
            'active_effects': [e.value for e in self._post_processor.active_effects]
        }
    
    def restore_state(self, state: Dict) -> None:
        """Restore render state."""
        if 'ambient_light' in state:
            self._lighting_system.set_ambient_light(state['ambient_light'])
        if 'active_effects' in state:
            for effect_value in state['active_effects']:
                try:
                    effect = EffectType(effect_value)
                    self._post_processor.add_effect(effect)
                except ValueError:
                    pass

