"""
Enhanced audio system management.

Supports 3D audio, audio mixing, dynamic music, audio effects,
voice chat hooks, and audio visualization.
"""

from typing import Dict, Optional, List, Tuple, Callable
from enum import Enum
import pygame
import math


class EffectType(Enum):
    """Audio effect types."""
    REVERB = "reverb"
    ECHO = "echo"
    LOWPASS = "lowpass"
    HIGHPASS = "highpass"
    BANDPASS = "bandpass"
    DISTORTION = "distortion"
    CHORUS = "chorus"


class AudioGroup:
    """Audio group for organizing related sounds."""
    
    def __init__(self, name: str):
        """Initialize audio group."""
        self.name = name
        self._volume = 1.0
        self._muted = False
        self._paused = False
        self._sounds: List[str] = []
    
    @property
    def volume(self) -> float:
        """Get group volume."""
        return 0.0 if self._muted else self._volume
    
    def set_volume(self, volume: float) -> None:
        """Set group volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
    
    @property
    def is_muted(self) -> bool:
        """Check if group is muted."""
        return self._muted
    
    def mute(self) -> None:
        """Mute group."""
        self._muted = True
    
    def unmute(self) -> None:
        """Unmute group."""
        self._muted = False
    
    @property
    def is_paused(self) -> bool:
        """Check if group is paused."""
        return self._paused
    
    def pause(self) -> None:
        """Pause group."""
        self._paused = True
    
    def resume(self) -> None:
        """Resume group."""
        self._paused = False


class AudioBus:
    """Audio bus for routing and mixing."""
    
    def __init__(self, name: str, parent: Optional['AudioBus'] = None):
        """Initialize audio bus."""
        self.name = name
        self._parent = parent
        self._volume = 1.0
        self._channels: List[pygame.mixer.Channel] = []
    
    @property
    def volume(self) -> float:
        """Get bus volume."""
        return self._volume
    
    def set_volume(self, volume: float) -> None:
        """Set bus volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
    
    @property
    def effective_volume(self) -> float:
        """Get effective volume (parent volume * this volume)."""
        parent_vol = self._parent.effective_volume if self._parent else 1.0
        return parent_vol * self._volume
    
    def add_channel(self, channel: pygame.mixer.Channel) -> None:
        """Add channel to bus."""
        if channel not in self._channels:
            self._channels.append(channel)


class AudioEffect:
    """Audio effect processor."""
    
    def __init__(self, name: str, effect_type: EffectType):
        """Initialize audio effect."""
        self.name = name
        self.type = effect_type
        self._parameters: Dict[str, float] = {}
        self._bypassed = False
        
        # Initialize default parameters based on effect type
        self._init_default_parameters()
    
    def _init_default_parameters(self) -> None:
        """Initialize default parameters for effect type."""
        if self.type == EffectType.REVERB:
            self._parameters = {'room_size': 0.5, 'damping': 0.5, 'width': 1.0}
        elif self.type == EffectType.ECHO:
            self._parameters = {'delay': 0.2, 'feedback': 0.3, 'wet_mix': 0.5}
        elif self.type == EffectType.LOWPASS:
            self._parameters = {'cutoff': 2000.0, 'resonance': 0.7}
        elif self.type == EffectType.HIGHPASS:
            self._parameters = {'cutoff': 200.0, 'resonance': 0.7}
        elif self.type == EffectType.BANDPASS:
            self._parameters = {'center': 1000.0, 'bandwidth': 500.0}
        elif self.type == EffectType.DISTORTION:
            self._parameters = {'drive': 0.5, 'tone': 0.5}
        elif self.type == EffectType.CHORUS:
            self._parameters = {'rate': 1.0, 'depth': 0.5, 'delay': 0.02}
    
    def set_parameter(self, name: str, value: float) -> None:
        """Set effect parameter."""
        self._parameters[name] = value
    
    def get_parameter(self, name: str) -> Optional[float]:
        """Get effect parameter."""
        return self._parameters.get(name)
    
    @property
    def is_bypassed(self) -> bool:
        """Check if effect is bypassed."""
        return self._bypassed
    
    def set_bypass(self, bypass: bool) -> None:
        """Set bypass state."""
        self._bypassed = bypass


class EffectChain:
    """Chain of audio effects."""
    
    def __init__(self, effects: List[AudioEffect]):
        """Initialize effect chain."""
        self.effects = effects


class MusicLayer:
    """Layer in dynamic music system."""
    
    def __init__(self, name: str, filepath: str):
        """Initialize music layer."""
        self.name = name
        self.filepath = filepath
        self._volume = 1.0
        self._active = False
    
    @property
    def volume(self) -> float:
        """Get layer volume."""
        return self._volume
    
    def set_volume(self, volume: float) -> None:
        """Set layer volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
    
    @property
    def is_active(self) -> bool:
        """Check if layer is active."""
        return self._active
    
    def activate(self) -> None:
        """Activate layer."""
        self._active = True
    
    def deactivate(self) -> None:
        """Deactivate layer."""
        self._active = False


class DynamicMusicSystem:
    """Dynamic/adaptive music system."""
    
    def __init__(self):
        """Initialize dynamic music system."""
        self.layers: List[MusicLayer] = []
        self._intensity = 0.0  # 0.0 to 1.0
        self._playing = False
    
    def add_layer(self, name: str, filepath: str) -> MusicLayer:
        """
        Add music layer.
        
        Args:
            name: Layer name
            filepath: Path to audio file
            
        Returns:
            Created layer
        """
        layer = MusicLayer(name, filepath)
        self.layers.append(layer)
        return layer
    
    def set_intensity(self, intensity: float) -> None:
        """
        Set music intensity (affects which layers play).
        
        Args:
            intensity: Intensity level (0.0 to 1.0)
        """
        self._intensity = max(0.0, min(1.0, intensity))
        # Update layer volumes based on intensity
        for layer in self.layers:
            # Simple intensity-based volume (can be made more sophisticated)
            layer.set_volume(self._intensity)
    
    def play_all(self) -> None:
        """Play all active layers."""
        self._playing = True
    
    def stop_all(self) -> None:
        """Stop all layers."""
        self._playing = False
    
    def crossfade(self, from_track: str, to_track: str, duration_ms: int = 1000) -> None:
        """
        Crossfade between two tracks.
        
        Args:
            from_track: Track to fade out
            to_track: Track to fade in
            duration_ms: Crossfade duration in milliseconds
        """
        # Implementation would fade out from_track and fade in to_track
        pass


class SpatialAudioEmitter:
    """3D spatial audio emitter."""
    
    def __init__(self, name: str, position: Tuple[float, float]):
        """Initialize spatial audio emitter."""
        self.name = name
        self.position = position
        self.max_distance = 500.0
        self.min_distance = 50.0
        self.rolloff_factor = 1.0
        self._volume = 1.0
    
    def set_position(self, position: Tuple[float, float]) -> None:
        """Set emitter position."""
        self.position = position
    
    def calculate_volume(
        self,
        listener_position: Tuple[float, float],
        listener_volume: float = 1.0
    ) -> float:
        """
        Calculate volume based on distance from listener.
        
        Args:
            listener_position: Listener position
            listener_volume: Base listener volume
            
        Returns:
            Calculated volume (0.0 to 1.0)
        """
        # Calculate distance
        dx = self.position[0] - listener_position[0]
        dy = self.position[1] - listener_position[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Calculate attenuation
        if distance <= self.min_distance:
            volume = 1.0
        elif distance >= self.max_distance:
            volume = 0.0
        else:
            # Linear attenuation (can be made logarithmic for more realism)
            factor = (self.max_distance - distance) / (self.max_distance - self.min_distance)
            volume = factor * self.rolloff_factor
        
        return max(0.0, min(1.0, volume * listener_volume * self._volume))
    
    def set_volume(self, volume: float) -> None:
        """Set emitter base volume."""
        self._volume = max(0.0, min(1.0, volume))


class AudioVisualizer:
    """Audio visualization system."""
    
    def __init__(self):
        """Initialize audio visualizer."""
        self._waveform_buffer: List[float] = []
        self._spectrum_buffer: List[float] = []
    
    def update(self) -> None:
        """Update visualizer (call each frame)."""
        # In real implementation, would sample audio here
        pass
    
    def get_waveform(self, num_samples: int = 100) -> List[float]:
        """
        Get waveform data.
        
        Args:
            num_samples: Number of samples to return
            
        Returns:
            Waveform samples (normalized -1.0 to 1.0)
        """
        # Mock implementation - would sample from actual audio
        return [0.0] * min(num_samples, 100)
    
    def get_spectrum(self, num_bands: int = 64) -> List[float]:
        """
        Get frequency spectrum data.
        
        Args:
            num_bands: Number of frequency bands
            
        Returns:
            Spectrum data (normalized 0.0 to 1.0)
        """
        # Mock implementation - would perform FFT on actual audio
        return [0.0] * min(num_bands, 64)


class EnhancedAudioManager:
    """Enhanced audio manager with advanced features."""
    
    def __init__(
        self,
        frequency: int = 44100,
        size: int = -16,
        channels: int = 2,
        buffer: int = 2048
    ):
        """Initialize enhanced audio manager."""
        self._frequency = frequency
        self._size = size
        self._channels = channels
        self._buffer = buffer
        self._initialized = False
        self._available = False
        
        # Groups and buses
        self._groups: Dict[str, AudioGroup] = {}
        self._buses: Dict[str, AudioBus] = {}
        
        # 3D audio
        self._emitters: Dict[str, SpatialAudioEmitter] = {}
        self._listener_position: Tuple[float, float] = (0.0, 0.0)
        
        # Effects
        self._effects: Dict[str, AudioEffect] = {}
        
        # Dynamic music
        self._dynamic_music: Optional[DynamicMusicSystem] = None
        
        # Visualization
        self._visualizer: Optional[AudioVisualizer] = None
        
        # Volume control
        self._master_volume = 1.0
        self._channel_volumes: Dict[str, float] = {}
        self._max_channels: Dict[str, int] = {}
    
    def initialize(self) -> bool:
        """Initialize audio system."""
        if self._initialized:
            return self._available
        
        try:
            pygame.mixer.pre_init(self._frequency, self._size, self._channels, self._buffer)
            pygame.mixer.init()
            self._available = pygame.mixer.get_init() is not None
            self._initialized = True
            return self._available
        except pygame.error:
            self._available = False
            self._initialized = True
            return False
    
    def cleanup(self) -> None:
        """Cleanup audio resources."""
        if self._initialized and self._available:
            try:
                pygame.mixer.quit()
            except Exception:
                pass
            finally:
                self._initialized = False
                self._available = False
    
    @property
    def available(self) -> bool:
        """Check if audio is available."""
        return self._available
    
    @property
    def master_volume(self) -> float:
        """Get master volume."""
        return self._master_volume
    
    def set_master_volume(self, volume: float) -> None:
        """Set master volume (0.0 to 1.0)."""
        self._master_volume = max(0.0, min(1.0, volume))
        if self._available:
            pygame.mixer.music.set_volume(self._master_volume)
    
    def create_group(self, name: str) -> AudioGroup:
        """Create audio group."""
        group = AudioGroup(name)
        self._groups[name] = group
        return group
    
    def get_group(self, name: str) -> Optional[AudioGroup]:
        """Get audio group."""
        return self._groups.get(name)
    
    def create_bus(self, name: str, parent: Optional[AudioBus] = None) -> AudioBus:
        """Create audio bus."""
        bus = AudioBus(name, parent)
        self._buses[name] = bus
        return bus
    
    def create_3d_emitter(
        self,
        name: str,
        position: Tuple[float, float]
    ) -> SpatialAudioEmitter:
        """Create 3D audio emitter."""
        emitter = SpatialAudioEmitter(name, position)
        self._emitters[name] = emitter
        return emitter
    
    def get_3d_emitter(self, name: str) -> Optional[SpatialAudioEmitter]:
        """Get 3D audio emitter."""
        return self._emitters.get(name)
    
    def set_3d_listener_position(self, position: Tuple[float, float]) -> None:
        """Set 3D audio listener position."""
        self._listener_position = position
    
    def get_3d_listener_position(self) -> Tuple[float, float]:
        """Get 3D audio listener position."""
        return self._listener_position
    
    def create_effect(self, name: str, effect_type: EffectType) -> AudioEffect:
        """Create audio effect."""
        effect = AudioEffect(name, effect_type)
        self._effects[name] = effect
        return effect
    
    def create_effect_chain(self, effects: List[AudioEffect]) -> EffectChain:
        """Create effect chain."""
        return EffectChain(effects)
    
    def create_music_layer(self, name: str, filepath: str) -> MusicLayer:
        """Create music layer."""
        return MusicLayer(name, filepath)
    
    def get_dynamic_music(self) -> DynamicMusicSystem:
        """Get or create dynamic music system."""
        if self._dynamic_music is None:
            self._dynamic_music = DynamicMusicSystem()
        return self._dynamic_music
    
    def create_visualizer(self) -> AudioVisualizer:
        """Create audio visualizer."""
        if self._visualizer is None:
            self._visualizer = AudioVisualizer()
        return self._visualizer
    
    def set_channel_volume(self, channel: str, volume: float) -> None:
        """Set channel volume."""
        self._channel_volumes[channel] = max(0.0, min(1.0, volume))
    
    def get_channel_volume(self, channel: str) -> float:
        """Get channel volume."""
        return self._channel_volumes.get(channel, 1.0)
    
    def set_max_channels(self, group: str, max_channels: int) -> None:
        """Set maximum channels for group."""
        self._max_channels[group] = max(1, max_channels)
    
    def get_max_channels(self, group: str) -> int:
        """Get maximum channels for group."""
        return self._max_channels.get(group, 8)
    
    def enable_ducking(
        self,
        target_channel: str,
        trigger_channel: str,
        duck_amount: float = 0.5
    ) -> None:
        """
        Enable audio ducking (lower target when trigger plays).
        
        Args:
            target_channel: Channel to duck
            trigger_channel: Channel that triggers ducking
            duck_amount: Duck amount (0.0 to 1.0)
        """
        # Implementation would handle ducking
        pass
    
    def ramp_volume(
        self,
        channel: str,
        target_volume: float,
        duration_ms: int = 500
    ) -> None:
        """
        Smoothly ramp volume.
        
        Args:
            channel: Channel name
            target_volume: Target volume
            duration_ms: Ramp duration
        """
        # Implementation would smoothly transition volume
        pass
    
    def supports_voice_chat(self) -> bool:
        """Check if voice chat is supported."""
        # Would check for voice chat support
        return False
    
    def save_state(self) -> Dict:
        """Save audio state."""
        return {
            'master_volume': self._master_volume,
            'channel_volumes': self._channel_volumes.copy(),
            'listener_position': self._listener_position
        }
    
    def restore_state(self, state: Dict) -> None:
        """Restore audio state."""
        if 'master_volume' in state:
            self.set_master_volume(state['master_volume'])
        if 'channel_volumes' in state:
            self._channel_volumes = state['channel_volumes'].copy()
        if 'listener_position' in state:
            self.set_3d_listener_position(state['listener_position'])

