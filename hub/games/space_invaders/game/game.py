"""Main Space Invaders game class."""

import random
from typing import List, Optional
import pygame
from hub.games.base_game_modular import BaseGameModular
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.core.display import DisplayManager
from hub.events.event_bus import EventBus
from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from hub.games.space_invaders.components import Bullet, Enemy, Player, Shield, UFO
from hub.games.space_invaders.graphics.sprite_renderer import SpriteRenderer
from hub.games.space_invaders.waves import WaveManager
from hub.games.space_invaders.audio import SoundManager
from hub.games.space_invaders.effects.screen_shake import ScreenShake
from hub.games.space_invaders.effects.particles import ParticleSystem
from hub.games.space_invaders.constants import (
    PLAYER_SPEED, PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED, UFO_SPEED,
    ENEMY_TYPE1_SCORE, ENEMY_TYPE2_SCORE, ENEMY_TYPE3_SCORE, WAVE_CLEAR_BONUS,
    STARTING_LIVES, SHIELD_COUNT, SHIELD_WIDTH, SHIELD_HEIGHT, SHIELD_Y
)


class SpaceInvadersGameModular(BaseGameModular):
    """Modular Space Invaders game implementation."""
    
    def __init__(
        self,
        display_manager: DisplayManager,
        input_service: InputService,
        audio_service: AudioService,
        event_bus: EventBus
    ):
        """Initialize Space Invaders game with dependency injection."""
        super().__init__(display_manager, input_service, audio_service, event_bus, "SpaceInvaders")
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.player_bullets: List[Bullet] = []
        self.enemy_bullets: List[Bullet] = []
        self.shields: List[Shield] = []
        self.ufo: Optional[UFO] = None
        self.enemy_direction = 1
        self.enemy_move_timer = 0.0
        self.enemy_shoot_timer = 0.0
        self.ufo_spawn_timer = 0.0
        
        # Wave management
        self.wave_manager = WaveManager()
        self.current_wave = 1
        
        # Lives system
        self.lives = STARTING_LIVES
        self.respawning = False
        self.respawn_timer = 0.0
        self.respawn_delay = 2.0  # seconds
        
        # Sprite rendering
        self.sprite_renderer = SpriteRenderer()
        
        # Sound manager
        self.sound_manager = SoundManager(audio_service)
        
        # Screen shake effect
        self.screen_shake = ScreenShake()
        
        # Particle system
        self.particle_system = ParticleSystem()
        
        # Explosion effects
        self.explosions: List[tuple] = []  # (x, y, frame, timer)
        
        # Between wave state
        self.show_wave_complete = False
        self.wave_complete_timer = 0.0
    
    def init(self) -> None:
        """Initialize game resources."""
        super().init()
        self.reset_game_state()
    
    def reset_game_state(self) -> None:
        """Reset game state for new game."""
        self.lives = STARTING_LIVES
        self.current_wave = 1
        self.score = 0
        self.respawning = False
        self.respawn_timer = 0.0
        self.show_wave_complete = False
        self.wave_complete_timer = 0.0
        
        # Start first wave
        self.start_wave(1)
    
    def start_wave(self, wave_number: int) -> None:
        """Start a new wave."""
        self.current_wave = wave_number
        self.show_wave_complete = False
        
        # Create player if doesn't exist
        if not self.player:
            self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60, PLAYER_SPEED)
        
        # Reset player position
        self.player.x = SCREEN_WIDTH // 2 - 20
        self.player.y = SCREEN_HEIGHT - 60
        
        # Get enemies from wave manager
        self.enemies = self.wave_manager.start_wave(wave_number)
        # Store initial enemy count for adaptive difficulty
        self.wave_manager._initial_enemy_count = len(self.enemies)
        for enemy in self.enemies:
            enemy.set_sprite_renderer(self.sprite_renderer)
        
        # Create shields (4 shields across screen)
        self.shields.clear()
        shield_spacing = SCREEN_WIDTH // (SHIELD_COUNT + 1)
        for i in range(SHIELD_COUNT):
            shield_x = (i + 1) * shield_spacing - SHIELD_WIDTH // 2
            shield = Shield(shield_x, SHIELD_Y, SHIELD_WIDTH, SHIELD_HEIGHT)
            self.shields.append(shield)
        
        # Clear bullets
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        
        # Clear UFO
        self.ufo = None
        
        # Reset timers
        self.enemy_move_timer = 0.0
        self.enemy_shoot_timer = 0.0
        self.ufo_spawn_timer = 0.0
        self.enemy_direction = 1
        
        # Clear explosions and particles
        self.explosions.clear()
        self.particle_system.clear()
    
    def update_game(self, dt: float) -> None:
        """Update game logic."""
        # Update sprite renderer animations
        self.sprite_renderer.update(dt)
        
        # Update screen shake
        self.screen_shake.update(dt)
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Handle respawning
        if self.respawning:
            self.respawn_timer += dt
            if self.respawn_timer >= self.respawn_delay:
                self.respawning = False
                self.respawn_timer = 0.0
                # Respawn player
                self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60, PLAYER_SPEED)
            return
        
        # Handle wave complete screen
        if self.show_wave_complete:
            self.wave_complete_timer += dt
            if self.wave_complete_timer >= 3.0:  # Show for 3 seconds
                self.show_wave_complete = False
                self.wave_complete_timer = 0.0
                # Start next wave
                self.start_wave(self.current_wave + 1)
            return
        
        if not self.player:
            return
        
        # Handle player input using InputService
        direction = 0
        if self.input_service.is_key_pressed(pygame.K_LEFT):
            direction = -1
        elif self.input_service.is_key_pressed(pygame.K_RIGHT):
            direction = 1
        
        self.player.update(dt, direction)
        
        # Shooting using InputService (allow up to 2 bullets on screen)
        MAX_PLAYER_BULLETS = 2
        if (self.input_service.is_key_just_pressed(pygame.K_SPACE) and 
            len(self.player_bullets) < MAX_PLAYER_BULLETS):
            # Bullet spawns from top-center of ship
            bullet_x = self.player.x + self.player.width // 2 - 2
            bullet_y = self.player.y  # Top of player ship
            # Create player bullet (is_enemy=False means it goes UP with negative speed)
            player_bullet = Bullet(bullet_x, bullet_y, PLAYER_BULLET_SPEED, is_enemy=False)
            self.player_bullets.append(player_bullet)
            self.sound_manager.play_shoot()
        
        # Update enemies with adaptive speed
        move_interval = self.wave_manager.get_move_interval()
        
        # Speed increases as enemies are eliminated and with wave progression
        remaining_enemies = len(self.enemies)
        total_enemies = getattr(self.wave_manager, '_initial_enemy_count', 50)
        
        # Base adaptive speed from remaining enemies
        remaining_factor = 1.0 - remaining_enemies / max(total_enemies, 1)
        
        # Wave progression factor (enemies faster in later waves)
        wave_speed_factor = min(0.3, (self.current_wave - 1) * 0.02)
        
        # Combined speed multiplier
        speed_multiplier = 1.0 + remaining_factor * 0.5 + wave_speed_factor
        
        self.enemy_move_timer += dt
        
        # Adaptive move interval (faster when fewer enemies)
        adaptive_interval = move_interval / speed_multiplier
        
        if self.enemy_move_timer >= adaptive_interval:
            self.enemy_move_timer = 0.0
            
            # Check if enemies need to move down and reverse
            need_reverse = False
            leftmost = min(e.x for e in self.enemies) if self.enemies else 0
            rightmost = max(e.x + e.width for e in self.enemies) if self.enemies else SCREEN_WIDTH
            
            for enemy in self.enemies:
                enemy.update(dt, self.enemy_direction)
                if enemy.x <= 0 or enemy.x + enemy.width >= SCREEN_WIDTH:
                    need_reverse = True
            
            if need_reverse:
                self.enemy_direction *= -1
                # Descent speed increases with fewer enemies and as they get closer to player
                base_descent = 20
                remaining_factor = 1.0 - remaining_enemies / max(total_enemies, 1)
                
                # More aggressive descent when enemies are lower on screen
                lowest_enemy_y = max((e.y for e in self.enemies), default=100)
                depth_factor = min(1.0, (lowest_enemy_y - 100) / 300)  # More descent when closer to player
                
                descent_amount = base_descent * (1.0 + remaining_factor * 0.5 + depth_factor * 0.4)
                
                # Move all enemies down maintaining formation
                for enemy in self.enemies:
                    enemy.move_down(descent_amount)
        
        # Enemy shooting with strategic targeting and adaptive difficulty
        shoot_interval = self.wave_manager.get_shoot_interval()
        
        # Adaptive shooting frequency (more frequent with fewer enemies and higher waves)
        remaining = len(self.enemies)
        total = getattr(self.wave_manager, '_initial_enemy_count', 50)
        
        # Base adaptive factor from remaining enemies
        remaining_factor = 1.0 - remaining / max(total, 1)
        
        # Wave difficulty factor (increases shooting frequency in later waves)
        wave_factor = min(1.0, (self.current_wave - 1) * 0.1)
        
        # Combine factors for adaptive interval
        adaptive_shoot_interval = shoot_interval / (1.0 + remaining_factor * 0.5 + wave_factor * 0.3)
        
        self.enemy_shoot_timer += dt
        if self.enemy_shoot_timer >= adaptive_shoot_interval and self.enemies and self.player:
            self.enemy_shoot_timer = 0.0
            
            # Strategic shooter selection: prefer enemies closest to player horizontally
            player_center_x = self.player.x + self.player.width // 2
            
            # Find enemies closest to player's X position (better targeting)
            def distance_to_player(enemy):
                enemy_center_x = enemy.x + enemy.width // 2
                return abs(enemy_center_x - player_center_x)
            
            # Sort enemies by row (prefer bottom) and distance to player
            sorted_enemies = sorted(self.enemies, key=lambda e: (e.row, distance_to_player(e)))
            
            # Adaptive shooter selection based on wave difficulty
            # Early waves: more random, later waves: more strategic
            strategic_chance = min(0.85, 0.6 + (self.current_wave - 1) * 0.05)
            
            if random.random() < strategic_chance and sorted_enemies:
                # Pick from bottom enemies, preferring closest
                bottom_count = max(1, len(sorted_enemies) // max(2, 4 - self.current_wave // 5))
                # In later waves, be more precise with selection
                if self.current_wave > 3:
                    # Top 2 closest bottom enemies
                    shooter = sorted_enemies[min(bottom_count // 2, len(sorted_enemies) - 1)]
                else:
                    shooter = random.choice(sorted_enemies[:bottom_count])
            else:
                shooter = random.choice(self.enemies)
            
            # Bullet spawns from bottom of enemy (center X, bottom Y)
            bullet_x = shooter.x + shooter.width // 2 - 2
            bullet_y = shooter.y + shooter.height  # Bottom of enemy
            self.enemy_bullets.append(Bullet(bullet_x, bullet_y, ENEMY_BULLET_SPEED, is_enemy=True))
            
            # In later waves, allow multiple enemies to shoot if few remain
            if self.current_wave > 5 and remaining < total * 0.3:
                if random.random() < 0.3:  # 30% chance for second shooter
                    second_shooter = random.choice([e for e in self.enemies if e != shooter])
                    bullet_x2 = second_shooter.x + second_shooter.width // 2 - 2
                    bullet_y2 = second_shooter.y + second_shooter.height
                    self.enemy_bullets.append(Bullet(bullet_x2, bullet_y2, ENEMY_BULLET_SPEED, is_enemy=True))
        
        # UFO spawning
        if self.ufo is None:
            spawn_chance = self.wave_manager.get_ufo_spawn_chance()
            self.ufo_spawn_timer += dt
            if self.ufo_spawn_timer >= 1.0:  # Check every second
                self.ufo_spawn_timer = 0.0
                if random.random() < spawn_chance:
                    # Spawn from random side
                    if random.random() < 0.5:
                        ufo_x = -50
                    else:
                        ufo_x = SCREEN_WIDTH + 50
                    self.ufo = UFO(ufo_x, 40, UFO_SPEED)
                    self.ufo.set_sprite_renderer(self.sprite_renderer)
        
        # Update UFO
        if self.ufo:
            if not self.ufo.update(dt):
                self.ufo = None  # UFO left screen
        
        # Update bullets
        for bullet in self.player_bullets[:]:
            if bullet.update(dt):
                # Add trail particles for player bullets
                if random.random() < 0.3:  # 30% chance per frame
                    self.particle_system.add_bullet_trail(
                        bullet.x + bullet.width // 2,
                        bullet.y + bullet.height // 2,
                        is_enemy=False
                    )
            else:
                self.player_bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            if bullet.update(dt):
                # Add trail particles for enemy bullets
                if random.random() < 0.2:  # 20% chance per frame
                    self.particle_system.add_bullet_trail(
                        bullet.x + bullet.width // 2,
                        bullet.y + bullet.height // 2,
                        is_enemy=True
                    )
            else:
                self.enemy_bullets.remove(bullet)
        
        # Update explosions
        self.explosions = [
            (x, y, frame + 1, timer + dt) 
            for x, y, frame, timer in self.explosions 
            if frame < 4
        ]
        
        # Check collisions - Player bullets vs shields
        for bullet in self.player_bullets[:]:
            bullet_rect = bullet.get_rect()
            for shield in self.shields:
                if shield.check_bullet_collision(bullet_rect):
                    self.player_bullets.remove(bullet)
                    # Add spark particles on shield hit
                    self.particle_system.add_hit_spark(
                        bullet_rect.centerx,
                        bullet_rect.centery
                    )
                    self.sound_manager.play_shield_hit()
                    break
        
        # Check collisions - Enemy bullets vs shields
        for bullet in self.enemy_bullets[:]:
            bullet_rect = bullet.get_rect()
            for shield in self.shields:
                if shield.check_bullet_collision(bullet_rect):
                    self.enemy_bullets.remove(bullet)
                    # Add spark particles on shield hit
                    self.particle_system.add_hit_spark(
                        bullet_rect.centerx,
                        bullet_rect.centery
                    )
                    self.sound_manager.play_shield_hit()
                    break
        
        # Check collisions - Player bullets vs enemies
        for bullet in self.player_bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if bullet_rect.colliderect(enemy.get_rect()):
                    self.player_bullets.remove(bullet)
                    # Add explosion
                    center = enemy.get_center()
                    self.explosions.append((center[0], center[1], 0, 0.0))
                    
                    # Particle explosion based on enemy type
                    if enemy.enemy_type == 1:
                        particle_color = YELLOW
                    elif enemy.enemy_type == 2:
                        particle_color = (0, 255, 255)  # Cyan
                    else:
                        particle_color = RED
                    self.particle_system.add_explosion(center[0], center[1], particle_color, count=12)
                    self.particle_system.add_hit_spark(center[0], center[1])
                    
                    self.sound_manager.play_explosion()
                    # Screen shake on enemy hit
                    self.screen_shake.shake(duration=0.15, intensity=3.0)
                    
                    # Score based on enemy type
                    if enemy.enemy_type == 1:
                        self.score += ENEMY_TYPE1_SCORE
                    elif enemy.enemy_type == 2:
                        self.score += ENEMY_TYPE2_SCORE
                    else:
                        self.score += ENEMY_TYPE3_SCORE
                    
                    self.enemies.remove(enemy)
                    self.wave_manager.remove_enemy(enemy)
                    break
        
        # Check collisions - Player bullets vs UFO
        if self.ufo:
            for bullet in self.player_bullets[:]:
                if bullet.get_rect().colliderect(self.ufo.get_rect()):
                    self.player_bullets.remove(bullet)
                    # Add explosion
                    center = self.ufo.get_center()
                    self.explosions.append((center[0], center[1], 0, 0.0))
                    
                    # Big particle explosion for UFO
                    self.particle_system.add_explosion(center[0], center[1], GREEN, count=20)
                    self.particle_system.add_explosion(center[0], center[1], YELLOW, count=15)
                    
                    self.sound_manager.play_explosion()
                    # Bigger shake for UFO hit
                    self.screen_shake.shake(duration=0.25, intensity=6.0)
                    self.score += self.ufo.points
                    self.ufo = None
                    break
            
            # Play UFO sound while it's on screen
            self.sound_manager.play_ufo()
        
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.enemy_bullets.remove(bullet)
                # Particle explosion on player hit
                player_center = (self.player.x + self.player.width // 2,
                               self.player.y + self.player.height // 2)
                self.particle_system.add_explosion(player_center[0], player_center[1], RED, count=15)
                # Strong shake on player hit
                self.screen_shake.shake(duration=0.3, intensity=8.0)
                self.lose_life()
                break
        
        # Enemies reach player
        for enemy in self.enemies:
            if enemy.y + enemy.height >= self.player.y:
                self.end_game()
                return
        
        # Check wave complete
        if self.wave_manager.is_wave_complete():
            self.score += WAVE_CLEAR_BONUS
            self.show_wave_complete = True
            self.wave_complete_timer = 0.0
    
    def lose_life(self) -> None:
        """Handle player losing a life."""
        self.lives -= 1
        if self.lives <= 0:
            self.end_game()
        else:
            # Start respawn timer
            self.respawning = True
            self.respawn_timer = 0.0
            self.player = None
            # Clear bullets
            self.player_bullets.clear()
    
    def render_game(self) -> None:
        """Render game objects."""
        # Apply screen shake offset
        shake_x, shake_y = self.screen_shake.get_offset()
        
        # Create a temporary surface for game content that we can offset
        from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(BLACK)
        
        # Render shields
        for shield in self.shields:
            shield.render(game_surface)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(game_surface)
        
        # Render UFO
        if self.ufo:
            self.ufo.render(game_surface)
        
        # Render player (if not respawning)
        if self.player and not self.respawning:
            self.player.render(game_surface, self.sprite_renderer)
        
        # Render bullets
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.render(game_surface)
        
        # Render explosions
        for x, y, frame, _ in self.explosions:
            self.sprite_renderer.draw_explosion_effect(game_surface, x, y, frame)
        
        # Render particles
        self.particle_system.render(game_surface)
        
        # Blit game surface with shake offset to main screen
        self.screen.blit(game_surface, (int(shake_x), int(shake_y)))
        
        # Render wave complete message (not affected by shake)
        if self.show_wave_complete:
            if self.font:
                wave_text = self.font.render(f"WAVE {self.current_wave} COMPLETE!", True, WHITE)
                text_rect = wave_text.get_rect(centerx=SCREEN_WIDTH // 2, 
                                             centery=SCREEN_HEIGHT // 2)
                self.screen.blit(wave_text, text_rect)
    
    def render_ui(self) -> None:
        """Render UI including scores and lives."""
        super().render_ui()
        
        if self.font:
            # Render score (top left)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # Render high score
            if self.high_score > 0:
                high_score_text = self.font.render(f"High: {self.high_score}", True, WHITE)
                self.screen.blit(high_score_text, (10, 50))
            
            # Render lives (top right)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
            
            # Render wave number
            wave_text = self.font.render(f"Wave: {self.current_wave}", True, WHITE)
            self.screen.blit(wave_text, (SCREEN_WIDTH - 150, 50))
            
            # Render respawn message
            if self.respawning:
                respawn_text = self.font.render("RESPAWNING...", True, WHITE)
                text_rect = respawn_text.get_rect(centerx=SCREEN_WIDTH // 2, 
                                                 centery=SCREEN_HEIGHT // 2)
                self.screen.blit(respawn_text, text_rect)

