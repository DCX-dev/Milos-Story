import pygame
import sys
import os

# macOS: allow native fullscreen (green button / Spaces behavior)
if sys.platform == "darwin":
    os.environ.setdefault("SDL_VIDEO_MAC_FULLSCREEN_SPACES", "1")

# Add project root to path for imports
from src.paths import get_base_path
project_root = get_base_path()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.player import Player
from src.game_platform import Platform
from screens.title_screen import TitleScreen
from src.level_system import create_level, get_level_background
from src.boss import Boss
from screens.victory_screen import VictoryScreen
from screens.credits_screen import CreditsScreen
from screens.options_screen import OptionsScreen, load_options, save_options
from src.save_system import SaveSystem
from src.enemy import Enemy
from screens.level_selector import LevelSelector
from src.arrow import Arrow

# Windows high-DPI: without this, the window can be huge and hard to close.
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

pygame.init()
pygame.mixer.init()  # Initialize mixer for music


def _compute_window_size():
    """Default window (3:2), scaled down to fit any desktop with margins."""
    base_w, base_h = 800, 534
    margin_w, margin_h = 64, 120
    dw, dh = 1280, 720
    if hasattr(pygame.display, "get_desktop_sizes"):
        sizes = pygame.display.get_desktop_sizes()
        if sizes:
            dw, dh = sizes[0][0], sizes[0][1]
    else:
        info = pygame.display.Info()
        if info.current_w and info.current_h:
            dw, dh = info.current_w, info.current_h
    avail_w = max(320, dw - margin_w)
    avail_h = max(240, dh - margin_h)
    scale = min(1.0, avail_w / base_w, avail_h / base_h)
    w = int(base_w * scale)
    h = int(base_h * scale)
    w = max(320, min(w, avail_w))
    h = max(240, min(h, avail_h))
    w -= w % 2
    h -= h % 2
    return w, h


# ========== DEBUG MODE ==========
# Set to True to enable level selector for testing
DEBUG_MODE = False
# =================================

# Set for real in Game.__init__ (_setup_display); placeholders for import safety
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 534
FPS = 60
GRAVITY = 0.7
JUMP_STRENGTH = -20
PLAYER_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (255, 100, 100)

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        opts = load_options()
        self.fullscreen = bool(opts.get("fullscreen", False))
        self._setup_display()

        # Game state
        self.state = "title"  # "title", "level_select", "playing", "victory", "credits", "options"
        self.current_level = 1
        self.save_slot = None
        
        # Initialize systems
        self.save_system = SaveSystem()
        self.title_screen = TitleScreen(self.screen)
        self.victory_screen = VictoryScreen(self.screen)
        self.level_selector = LevelSelector(self.screen)
        self.credits_screen = CreditsScreen(self.screen)
        self.options_screen = OptionsScreen(self.screen, game=self)
        
        # Level start position (for respawning)
        self.level_start_x = 100
        self.level_start_y = 100
        
        # Gameplay variables
        self.player = None
        self.platforms = []
        self.lava_zones = []  # Lava areas that kill instantly
        self.enemies = []
        self.boss = None
        self.chests = []
        self.arrows = []  # Player's shot arrows
        self.arrow_count = 20  # Start with 20 arrows
        self.player_damage = 1  # Hearts of damage per hit (1 = 1 heart)
        self.camera_x = 0
        self.camera_y = 0
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        
        # Boss fight variables
        self.boss_damage_timer = 0
        self.boss_damage_cooldown = 30  # Frames between damage
        
        # Player health
        self.player_health = 100
        self.max_health = 100
        
        # Aiming line toggle
        self.show_aim_line = True  # Default: show aiming line
        
        # Shoot cooldown (for held mouse/key - prevents instant drain)
        self.shoot_cooldown = 0
        
        # Music system
        self.current_music = None  # Track currently playing music file
        self.music_folder = "assets/music"
    
    def _setup_display(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        flags = pygame.DOUBLEBUF
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), flags | pygame.FULLSCREEN)
            SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()
        else:
            SCREEN_WIDTH, SCREEN_HEIGHT = _compute_window_size()
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                flags | pygame.RESIZABLE,
            )
        pygame.display.set_caption("Milo's Story - Platformer")
    
    def _sync_all_screens(self):
        self.title_screen.screen = self.screen
        self.title_screen.refresh_for_screen()
        self.victory_screen.screen = self.screen
        self.level_selector.screen = self.screen
        self.credits_screen.screen = self.screen
        self.options_screen.screen = self.screen
        self.options_screen.relayout()
    
    def _set_fullscreen(self, enabled: bool):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        enabled = bool(enabled)
        if enabled == self.fullscreen:
            return
        playing = self.state == "playing" and self.player is not None
        px = py = cl = None
        ar = pd = None
        if playing:
            px, py, cl = self.player.x, self.player.y, self.current_level
            ar, pd = self.arrow_count, self.player_damage
        self.fullscreen = enabled
        save_options(fullscreen=enabled)
        self._setup_display()
        self._sync_all_screens()
        if playing and cl is not None and px is not None:
            self.arrow_count = ar
            self.player_damage = pd
            self.load_level(cl, int(px), int(py))
    
    def _apply_window_size(self, w, h):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        if self.fullscreen:
            return
        w = max(320, min(int(w), 7680))
        h = max(240, min(int(h), 4320))
        if w == SCREEN_WIDTH and h == SCREEN_HEIGHT:
            return
        playing = self.state == "playing" and self.player is not None
        px = py = cl = None
        ar = pd = None
        if playing:
            px, py, cl = self.player.x, self.player.y, self.current_level
            ar, pd = self.arrow_count, self.player_damage
        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.DOUBLEBUF)
        SCREEN_WIDTH, SCREEN_HEIGHT = w, h
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        self._sync_all_screens()
        if playing and cl is not None and px is not None:
            self.arrow_count = ar
            self.player_damage = pd
            self.load_level(cl, int(px), int(py))
    
    def _find_music_file(self, level_num):
        """Find music file for a level. Looks for level1, level2, etc. in any format."""
        import glob
        
        # Try to find music folder (relative to project root)
        base_dir = get_base_path()
        music_path = os.path.normpath(os.path.join(base_dir, self.music_folder))
        
        if not os.path.exists(music_path):
            return None
        
        # Look for files matching "level{num}.*" pattern
        pattern = os.path.join(music_path, f"level{level_num}.*")
        matches = glob.glob(pattern)
        
        if matches:
            # Return first match (prioritize common formats)
            audio_formats = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
            for fmt in audio_formats:
                for match in matches:
                    if match.lower().endswith(fmt):
                        return match
            # If no preferred format found, return first match
            return matches[0]
        
        return None
    
    def _find_theme_music_file(self):
        """Find theme music file. Looks for theme.* in any format."""
        import glob
        
        base_dir = get_base_path()
        music_path = os.path.normpath(os.path.join(base_dir, self.music_folder))
        
        if not os.path.exists(music_path):
            return None
        
        pattern = os.path.join(music_path, "theme.*")
        matches = glob.glob(pattern)
        
        if matches:
            audio_formats = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
            for fmt in audio_formats:
                for match in matches:
                    if match.lower().endswith(fmt):
                        return match
            return matches[0]
        
        return None
    
    def _apply_music_volume(self):
        """Apply current volume from options to mixer"""
        vol = load_options()["volume"] / 100.0
        pygame.mixer.music.set_volume(vol)
    
    def _play_theme_music(self):
        """Play theme music on title/save screen. Loops forever."""
        theme_file = self._find_theme_music_file()
        if not theme_file:
            return
        # Only load/play if not already playing this file
        if self.current_music == theme_file and pygame.mixer.music.get_busy():
            self._apply_music_volume()
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(theme_file)
            self._apply_music_volume()
            pygame.mixer.music.play(loops=-1)
            self.current_music = theme_file
        except Exception as e:
            print(f"Error playing theme music {theme_file}: {e}")
    
    def _play_level_music(self, level_num):
        """Play music for a specific level"""
        # Stop current music if playing
        pygame.mixer.music.stop()
        self.current_music = None
        
        # Find and play music for this level
        music_file = self._find_music_file(level_num)
        if music_file:
            try:
                pygame.mixer.music.load(music_file)
                self._apply_music_volume()
                pygame.mixer.music.play(loops=-1)  # Loop forever (repeat)
                self.current_music = music_file
            except Exception as e:
                print(f"Error playing music {music_file}: {e}")
    
    def _stop_music(self):
        """Stop currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def _attempt_shoot_arrow(self):
        if self.state != "playing" or not self.player:
            return
        # Ensure arrow_count is int (in case of save data type)
        count = int(self.arrow_count) if self.arrow_count is not None else 0
        if count <= 0:
            return
        mx, my = pygame.mouse.get_pos()
        wx = mx + self.camera_x
        wy = my + self.camera_y
        arr = self.player.shoot_arrow(wx, wy)
        if arr:
            self.arrows.append(arr)
            self.arrow_count = count - 1
        
    def start_game(self, save_slot):
        """Start a new game or load from save"""
        self.save_slot = save_slot
        
        # Try to load save
        save_data = self.save_system.load_game(save_slot)
        if save_data:
            self.current_level = save_data.get("level", 1)
            start_x = save_data.get("player_x", 100)
            start_y = save_data.get("player_y", 100)
            self.arrow_count = save_data.get("arrow_count", 20)
            self.player_damage = save_data.get("player_damage", 1)
        else:
            # New game
            self.current_level = 1
            start_x = 100
            start_y = 100
            self.arrow_count = 20
            self.player_damage = 1
        
        self.load_level(self.current_level, start_x, start_y)
        self.state = "playing"
    
    def load_level(self, level_num, player_x=100, player_y=100):
        """Load a specific level"""
        self.current_level = level_num
        
        # Store level start position for respawning
        self.level_start_x = player_x
        self.level_start_y = player_y
        
        # Create player
        self.player = Player(
            player_x, player_y, PLAYER_SPEED, GRAVITY, JUMP_STRENGTH,
            screen_height=SCREEN_HEIGHT,
        )
        
        # Reset player health
        self.player_health = self.max_health
        
        # Clear arrows when loading new level
        self.arrows = []
        
        # Create platforms, enemies, lava, and chests for level
        self.platforms, self.enemies, self.lava_zones, self.world_width, self.chests = create_level(
            level_num, SCREEN_HEIGHT, SCREEN_WIDTH)
        for enemy in self.enemies:
            enemy.screen_height = SCREEN_HEIGHT
        
        # Create boss for level 10
        self.boss = None
        if level_num == 10:
            self.boss = Boss(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 200)
        
        # Reset camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Reset boss damage timer
        self.boss_damage_timer = 0
        
        # Play level music
        self._play_level_music(level_num)
    
    def respawn_player(self):
        """Restart game from level 1 when player dies"""
        # Stop music
        self._stop_music()

        # Clear all arrows and reset progress
        self.arrows = []
        self.arrow_count = 20
        self.player_damage = 1

        # Delete save file if exists
        if self.save_slot is not None:
            self.save_system.delete_save(self.save_slot)
        
        # Reset to level 1
        self.current_level = 1
        self.save_slot = None
        
        # Load level 1 from scratch (music will play automatically)
        self.load_level(1, 100, 100)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self._set_fullscreen(not self.fullscreen)
                continue
            
            if not self.fullscreen:
                if event.type == pygame.VIDEORESIZE:
                    self._apply_window_size(event.w, event.h)
                    continue
                if hasattr(pygame, "WINDOWEVENT") and event.type == pygame.WINDOWEVENT:
                    sub = event.event
                    resized = getattr(pygame, "WINDOWEVENT_RESIZED", None)
                    size_changed = getattr(pygame, "WINDOWEVENT_SIZE_CHANGED", None)
                    resize_codes = {c for c in (resized, size_changed) if c is not None}
                    if resize_codes and sub in resize_codes:
                        try:
                            nw, nh = pygame.display.get_window_size()
                            self._apply_window_size(nw, nh)
                        except (pygame.error, AttributeError):
                            pass
                        continue
            
            if self.state == "title":
                result = self.title_screen.handle_event(event)
                if result == "quit":
                    self.running = False
                elif result == "credits":
                    self._stop_music()
                    self.state = "credits"
                elif result == "options":
                    self.state = "options"
                elif result and result[0] == "start_game":
                    if DEBUG_MODE:
                        self.state = "level_select"
                    else:
                        self.start_game(result[1])
            
            
            elif self.state == "level_select":
                result = self.level_selector.handle_event(event)
                if result == "cancel":
                    self.state = "title"
                elif result and result[0] == "start_level":
                    self.current_level = result[1]
                    self.save_slot = 0  # Use slot 0 for debug
                    self.load_level(self.current_level, 100, 100)
                    self.state = "playing"
            
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Save and return to title
                        self.save_game()
                        self._stop_music()
                        self.state = "title"
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                    elif event.key == pygame.K_6:
                        # Toggle aiming line
                        self.show_aim_line = not self.show_aim_line
                    elif event.key in (pygame.K_x, pygame.K_f):
                        self._attempt_shoot_arrow()
                        self.shoot_cooldown = 8
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._attempt_shoot_arrow()
                        self.shoot_cooldown = 8
            
            elif self.state == "victory":
                result = self.victory_screen.handle_event(event)
                if result == "title":
                    # Delete save file when OK is pressed (in case it wasn't deleted before)
                    if self.save_slot is not None:
                        self.save_system.delete_save(self.save_slot)
                    self.state = "title"
            
            elif self.state == "credits":
                result = self.credits_screen.handle_event(event)
                if result == "title":
                    self.state = "title"
            
            elif self.state == "options":
                result = self.options_screen.handle_event(event)
                if result == "title":
                    self.state = "title"
    
    def save_game(self):
        """Save current game state"""
        if self.save_slot is not None and self.player:
            self.save_system.save_game(
                self.save_slot,
                self.current_level,
                self.player.x,
                self.player.y,
                self.arrow_count,
                self.player_damage
            )
    
    def update(self):
        """Update game state"""
        if self.state == "title":
            self._play_theme_music()
            self.title_screen.update()
        
        elif self.state == "level_select":
            self.level_selector.update()
        
        elif self.state == "playing":
            keys = pygame.key.get_pressed()
            
            # Decrement shoot cooldown
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            
            # Allow shooting while holding mouse or X/F key (with cooldown)
            if self.shoot_cooldown == 0 and self.arrow_count > 0:
                mouse_held = pygame.mouse.get_pressed()[0]
                key_held = keys[pygame.K_x] or keys[pygame.K_f]
                if mouse_held or key_held:
                    self._attempt_shoot_arrow()
                    self.shoot_cooldown = 8  # ~7 shots per second when held
            
            self.player.update(keys, self.platforms)
            
            # Update arrows
            i = 0
            while i < len(self.arrows):
                arr = self.arrows[i]
                if not arr.is_alive:
                    self.arrows.pop(i)
                    continue
                arr.update()
                if not arr.is_alive:
                    self.arrows.pop(i)
                    continue
                arr_rect = arr.get_rect()
                hit = False
                for enemy in self.enemies:
                    if enemy.is_alive and arr_rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(self.player_damage)
                        arr.is_alive = False
                        hit = True
                        break
                if not hit and self.boss and self.boss.is_alive:
                    if arr_rect.colliderect(self.boss.get_rect()):
                        self.boss.take_damage(self.player_damage)
                        arr.is_alive = False
                        hit = True
                if arr.is_alive:
                    i += 1
                else:
                    self.arrows.pop(i)
            
            # Update enemies (pass player position for chase AI)
            for enemy in self.enemies[:]:
                if enemy.is_alive:
                    enemy.update(self.platforms, self.player.x, self.player.y)
                    
                    # Check collision with player
                    player_rect = pygame.Rect(self.player.x, self.player.y, 
                                            self.player.width, self.player.height)
                    enemy_rect = enemy.get_rect()
                    
                    if player_rect.colliderect(enemy_rect):
                        # Player takes damage from enemy
                        self.player_health -= 1
                        if self.player_health <= 0:
                            # Respawn player at start of level
                            self.respawn_player()
                else:
                    # Remove dead enemies
                    self.enemies.remove(enemy)
            
            # Check chest collection
            player_rect = pygame.Rect(self.player.x, self.player.y, 
                                     self.player.width, self.player.height)
            for chest in self.chests:
                result = chest.collect(player_rect)
                if result:
                    arrows_gain, damage_gain = result
                    self.arrow_count += arrows_gain
                    self.player_damage += damage_gain
            
            # Check lava collision (instant death)
            for lava_zone in self.lava_zones:
                lava_rect = pygame.Rect(lava_zone["x"], lava_zone["y"], 
                                       lava_zone["width"], lava_zone["height"])
                if player_rect.colliderect(lava_rect):
                    # Instant death from lava
                    self.respawn_player()
            
            # Update boss if present
            if self.boss:
                if self.boss.is_alive:
                    self.boss.update(self.platforms, self.player.x, self.player.y)
                    
                    # Check boss-projectile collisions with player
                    player_rect = pygame.Rect(self.player.x, self.player.y, 
                                           self.player.width, self.player.height)
                    if self.boss.check_projectile_collision(player_rect):
                        # Boss projectile hits player - 20 damage
                        self.player_health -= 20
                        if self.player_health <= 0:
                            self.respawn_player()
                    
                    # Check if player hits boss (boss damages player on contact)
                    boss_rect = self.boss.get_rect()
                    if player_rect.colliderect(boss_rect):
                        # Boss damages player on contact - 20 damage
                        self.boss_damage_timer += 1
                        if self.boss_damage_timer >= self.boss_damage_cooldown:
                            self.player_health -= 20
                            self.boss_damage_timer = 0
                            if self.player_health <= 0:
                                self.respawn_player()
                
                # Check if boss is defeated (check outside the is_alive block)
                if not self.boss.is_alive:
                    # Delete save file after completing level 10
                    if self.save_slot is not None:
                        self.save_system.delete_save(self.save_slot)
                    # Stop music and transition to victory screen
                    self._stop_music()
                    self.state = "victory"
            
            # Check if player reached end of level (for non-boss levels)
            if self.current_level < 10:
                if self.player.x >= self.world_width - 100:
                    # Level complete
                    self.current_level += 1
                    self.save_game()
                    if self.current_level <= 10:
                        self.load_level(self.current_level, 100, 100)  # Music will change automatically
                    else:
                        # All levels complete
                        self._stop_music()
                        self.state = "victory"
            
            # Update camera to follow player
            self.camera_x = self.player.x - SCREEN_WIDTH // 2
            self.camera_x = max(0, min(self.camera_x, self.world_width - SCREEN_WIDTH))
            
            self.camera_y = self.player.y - SCREEN_HEIGHT // 2
            self.camera_y = max(0, min(self.camera_y, self.world_height - SCREEN_HEIGHT))
            
            # Auto-save periodically
            if pygame.time.get_ticks() % 3000 == 0:  # Every 3 seconds
                self.save_game()
        
        elif self.state == "victory":
            self.victory_screen.update()
        
        elif self.state == "credits":
            self.credits_screen.update()
        
        elif self.state == "options":
            self.options_screen.update()
            self._apply_music_volume()  # Apply volume changes in real-time
    
    def draw(self):
        """Draw current game state"""
        if self.state == "title":
            self.title_screen.draw()
        
        elif self.state == "playing":
            # Clear screen with level-specific background
            bg_color = get_level_background(self.current_level)
            self.screen.fill(bg_color)
            
            # Draw lava zones
            for lava_zone in self.lava_zones:
                screen_x = lava_zone["x"] - self.camera_x
                screen_y = lava_zone["y"] - self.camera_y
                lava_rect = pygame.Rect(screen_x, screen_y, lava_zone["width"], lava_zone["height"])
                # Animated lava effect (simple pulsing)
                pulse = int(pygame.time.get_ticks() / 100) % 2
                lava_color = (255, 100 + pulse * 50, 0) if pulse else (255, 50, 0)
                pygame.draw.rect(self.screen, lava_color, lava_rect)
                # Lava bubbles
                for i in range(5):
                    bubble_x = screen_x + (i * lava_zone["width"] // 5) + int(pygame.time.get_ticks() / 50) % (lava_zone["width"] // 5)
                    bubble_y = screen_y + lava_zone["height"] // 2
                    pygame.draw.circle(self.screen, (255, 200, 0), 
                                     (bubble_x % lava_zone["width"] + screen_x, bubble_y), 5)
            
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw chests
            for chest in self.chests:
                chest.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw enemies
            for enemy in self.enemies:
                if enemy.is_alive:
                    enemy.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw arrows
            for arrow in self.arrows:
                arrow.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw boss if present
            if self.boss:
                self.boss.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw player
            self.player.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw aiming line if enabled
            if self.show_aim_line:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_mouse_x = mouse_x + self.camera_x
                world_mouse_y = mouse_y + self.camera_y
                # Draw line from player center to mouse position
                player_center_x = self.player.x + self.player.width // 2 - self.camera_x
                player_center_y = self.player.y + self.player.height // 2 - self.camera_y
                pygame.draw.line(self.screen, (255, 255, 0), 
                               (player_center_x, player_center_y),
                               (mouse_x, mouse_y), 2)
                # Draw small circle at mouse position
                pygame.draw.circle(self.screen, (255, 255, 0), (mouse_x, mouse_y), 5)
            
            # Draw UI
            font = pygame.font.Font(None, 36)
            level_text = font.render(f"Level: {self.current_level}", True, WHITE)
            self.screen.blit(level_text, (10, 10))
            
            # Arrow count (top left, below level)
            arrow_text = font.render(f"Arrows: {self.arrow_count}", True, (200, 200, 100))
            self.screen.blit(arrow_text, (10, 45))
            
            # Damage (hearts) - top left
            damage_text = font.render(f"Damage: {self.player_damage} heart{'s' if self.player_damage != 1 else ''}", True, (255, 100, 100))
            self.screen.blit(damage_text, (10, 80))
            
            score_text = font.render(f"Score: {int(self.player.x // 10)}", True, WHITE)
            self.screen.blit(score_text, (10, 115))
            
            # Player health bar
            health_bar_width = 200
            health_bar_height = 20
            health_x = 10
            health_y = 150
            
            # Background
            pygame.draw.rect(self.screen, (100, 0, 0), 
                          (health_x, health_y, health_bar_width, health_bar_height))
            # Health
            health_width = int((self.player_health / self.max_health) * health_bar_width)
            pygame.draw.rect(self.screen, (255, 0, 0), 
                          (health_x, health_y, health_width, health_bar_height))
            # Border
            pygame.draw.rect(self.screen, WHITE, 
                          (health_x, health_y, health_bar_width, health_bar_height), 2)
            
            # Health text
            health_text = font.render(f"Health: {self.player_health}/{self.max_health}", True, WHITE)
            self.screen.blit(health_text, (220, 145))
            
            # Boss health if boss exists
            if self.boss and self.boss.is_alive:
                boss_text = font.render("BOSS FIGHT!", True, RED)
                self.screen.blit(boss_text, (SCREEN_WIDTH - 200, 10))
            
            # Instructions with background for visibility
            small_font = pygame.font.Font(None, 24)
            instructions = [
                "Arrow Keys / WASD: Move",
                "Space / Up: Jump",
                "X / F / Click: Shoot Arrow (aims at mouse)",
                "Chests: +14 arrows or +1 damage (walk near to collect)",
                "6: Toggle Aiming Line | F11: Fullscreen | ESC: Save & Quit"
            ]
            # Draw semi-transparent background for instructions
            instruction_bg_height = len(instructions) * 25 + 10
            instruction_bg = pygame.Surface((400, instruction_bg_height))
            instruction_bg.set_alpha(200)  # Semi-transparent
            instruction_bg.fill((0, 0, 0))  # Black background
            self.screen.blit(instruction_bg, (5, SCREEN_HEIGHT - instruction_bg_height - 5))
            
            # Draw instructions with bright text
            for i, instruction in enumerate(instructions):
                text = small_font.render(instruction, True, (255, 255, 255))  # Bright white
                self.screen.blit(text, (10, SCREEN_HEIGHT - instruction_bg_height + 5 + i * 25))
        
        elif self.state == "level_select":
            self.level_selector.draw()
        
        elif self.state == "victory":
            self.victory_screen.draw()
        
        elif self.state == "credits":
            self.credits_screen.draw()
        
        elif self.state == "options":
            self.options_screen.draw()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Stop music and save before quitting
        self._stop_music()
        if self.state == "playing":
            self.save_game()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
