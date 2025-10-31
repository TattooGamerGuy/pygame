"""Rendering layer/z-order management - Modular."""

from typing import List, Dict, Tuple, Optional
import pygame


class LayerManager:
    """Manages rendering layers and z-ordering."""
    
    def __init__(self):
        """Initialize layer manager."""
        self._layers: Dict[int, List[dict]] = {}
        self._default_layer = 0
    
    def add(
        self,
        surface: pygame.Surface,
        position: Tuple[float, float],
        layer: int = None,
        rotation: float = 0.0,
        scale: float = 1.0
    ) -> None:
        """
        Add item to a layer.
        
        Args:
            surface: Surface to render
            position: (x, y) position
            layer: Layer number (None uses default)
            rotation: Rotation in degrees
            scale: Scale factor
        """
        if layer is None:
            layer = self._default_layer
        
        if layer not in self._layers:
            self._layers[layer] = []
        
        self._layers[layer].append({
            'surface': surface,
            'position': position,
            'rotation': rotation,
            'scale': scale
        })
    
    def clear(self) -> None:
        """Clear all layers."""
        self._layers.clear()
    
    def clear_layer(self, layer: int) -> None:
        """
        Clear a specific layer.
        
        Args:
            layer: Layer number to clear
        """
        if layer in self._layers:
            del self._layers[layer]
    
    def render(self, target: pygame.Surface) -> None:
        """
        Render all layers in order.
        
        Args:
            target: Target surface to render to
        """
        sorted_layers = sorted(self._layers.keys())
        
        for layer in sorted_layers:
            for item in self._layers[layer]:
                surface = item['surface']
                x, y = item['position']
                rotation = item['rotation']
                scale = item['scale']
                
                # Apply transformations
                if scale != 1.0:
                    new_size = (int(surface.get_width() * scale), int(surface.get_height() * scale))
                    surface = pygame.transform.scale(surface, new_size)
                
                if rotation != 0.0:
                    surface = pygame.transform.rotate(surface, rotation)
                
                target.blit(surface, (x, y))
        
        # Clear after rendering
        self._layers.clear()
    
    def set_default_layer(self, layer: int) -> None:
        """
        Set default layer.
        
        Args:
            layer: Default layer number
        """
        self._default_layer = layer

