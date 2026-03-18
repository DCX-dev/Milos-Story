import pygame
import os
import math
from PIL import Image

class Player:
    def __init__(self, x, y, speed, gravity, jump_strength):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.speed = speed
        self.gravity = gravity
        self.jump_strength = jump_strength
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.coyote_time = 0  # Grace period for jumping after leaving platform
        self.coyote_time_max = 8  # Frames you can still jump after leaving platform
        
        # Fall damage tracking
        self.last_ground_y = y
        self.fall_start_y = y
        self.is_falling = False
        
        # Bow and arrow - infinite arrows, no cooldown
        
        # Animation state
        self.current_state = "standing"  # "standing", "walking", "falling"
        self.animation_frame = 0
        self.animation_timer = 0.0  # Use float for frame duration timing
        self.facing_right = True  # Direction player is facing
        
        # Load animations (stores both frames and durations)
        self.animations = {}  # {state: [frames]}
        self.animation_durations = {}  # {state: [durations_in_ms]}
        self.load_animations()
        
    def load_animations(self):
        """Load GIF animations from player folder"""
        # Use normpath to handle paths with spaces and special characters
        try:
            from .paths import get_base_path
            base_dir = get_base_path()
            player_folder = os.path.normpath(os.path.join(base_dir, "assets", "player"))
        except Exception:
            # Fallback
            from .paths import get_base_path
            base_dir = get_base_path()
            player_folder = os.path.normpath(os.path.join(base_dir, "assets", "player"))
        
        animation_files = {
            "walking": "walking.gif",
            "standing": "standing.gif",
            "falling": "falling.gif"
        }
        
        for state, filename in animation_files.items():
            try:
                filepath = os.path.normpath(os.path.join(player_folder, filename))
                if os.path.exists(filepath):
                    frames, durations = self.load_gif_frames(filepath)
                    self.animations[state] = frames
                    self.animation_durations[state] = durations
                else:
                    # Fallback: create a simple colored rectangle if GIF doesn't exist
                    print(f"Warning: {filename} not found in player folder. Using fallback.")
                    self.animations[state] = [self.create_fallback_surface()]
                    self.animation_durations[state] = [100]  # Default 100ms duration
            except Exception as e:
                # Fallback on any error
                print(f"Error loading {filename}: {e}. Using fallback.")
                self.animations[state] = [self.create_fallback_surface()]
                self.animation_durations[state] = [100]  # Default 100ms duration
        
        # Set default size from first animation if available
        if self.animations.get("standing"):
            first_frame = self.animations["standing"][0]
            self.width = first_frame.get_width()
            self.height = first_frame.get_height()
    
    def load_gif_frames(self, filepath):
        """Extract frames and durations from a GIF file"""
        frames = []
        durations = []
        try:
            gif = Image.open(filepath)
            frame_count = 0
            while True:
                try:
                    # Convert PIL image to pygame surface
                    frame = gif.copy()
                    # Convert RGBA if needed
                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')
                    
                    # Convert to pygame surface
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    pygame_surface = pygame.image.fromstring(data, size, mode)
                    frames.append(pygame_surface)
                    
                    # Extract frame duration (in milliseconds)
                    # GIFs store duration in info dict, default to 100ms if not found
                    duration_ms = gif.info.get('duration', 100)
                    # Ensure minimum duration of 50ms to prevent too-fast animations
                    duration_ms = max(50, duration_ms)
                    durations.append(duration_ms)
                    
                    frame_count += 1
                    gif.seek(frame_count)
                except EOFError:
                    break
            
            # If no frames were extracted, create a fallback
            if not frames:
                frames = [self.create_fallback_surface()]
                durations = [100]
                
        except Exception as e:
            print(f"Error loading GIF {filepath}: {e}")
            frames = [self.create_fallback_surface()]
            durations = [100]
        
        return frames, durations
    
    def create_fallback_surface(self):
        """Create a simple fallback surface if GIFs aren't available"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Draw a simple colored rectangle
        pygame.draw.rect(surface, (255, 200, 100), (0, 0, self.width, self.height))
        # Draw eyes
        pygame.draw.circle(surface, (0, 0, 0), (12, 15), 5)
        pygame.draw.circle(surface, (0, 0, 0), (28, 15), 5)
        # Draw smile
        pygame.draw.arc(surface, (0, 0, 0), (10, 20, 20, 15), 0, 3.14, 2)
        return surface
    
    def get_animation_state(self):
        """Determine current animation state based on player movement"""
        # Check if player is in the air (jumping or falling)
        if not self.on_ground:
            return "falling"
        # Check if player is moving horizontally (only when on ground)
        elif abs(self.vel_x) > 0.1:
            return "walking"
        # Otherwise, player is standing still on ground
        else:
            return "standing"
    
    def jump(self):
        # Allow jump if on ground or within coyote time
        if self.on_ground or self.coyote_time > 0:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.coyote_time = 0  # Consume coyote time
    
    def shoot_arrow(self, target_x, target_y):
        # No cooldown - infinite arrows!
        from src.arrow import Arrow
        sx = self.x + self.width // 2
        sy = self.y + self.height // 2
        dx = target_x - sx
        dy = target_y - sy
        d = math.sqrt(dx * dx + dy * dy)
        if d < 20:
            if d < 0.1:
                target_x = sx
                target_y = sy - 40
            else:
                s = 30 / d
                target_x = sx + dx * s
                target_y = sy + dy * s
        return Arrow(sx, sy, target_x, target_y)
    
    def get_fall_distance(self):
        """Get current fall distance in pixels"""
        if self.is_falling:
            return self.y - self.fall_start_y
        return 0
    
    def update(self, keys, platforms):
        # Horizontal movement
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
        
        # Track fall start
        was_on_ground = self.on_ground
        
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Track falling for fall damage
        if was_on_ground and not self.on_ground and self.vel_y > 0:
            # Started falling
            self.is_falling = True
            self.fall_start_y = self.y - self.vel_y
        elif self.on_ground and self.is_falling:
            # Landed - calculate fall distance
            self.is_falling = False
            # Fall distance will be calculated in main.py
        
        # Update coyote time
        if self.on_ground:
            self.coyote_time = self.coyote_time_max
            self.last_ground_y = self.y
        else:
            self.coyote_time = max(0, self.coyote_time - 1)
        
        
        # Reset ground state
        self.on_ground = False
        
        # Collision detection with platforms
        # Use previous position to detect collision direction
        prev_y = self.y - self.vel_y
        prev_bottom = prev_y + self.height
        
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_bottom = self.y + self.height
        player_left = self.x
        player_right = self.x + self.width
        
        for platform in platforms:
            platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            platform_top = platform.y
            platform_bottom = platform.y + platform.height
            platform_left = platform.x
            platform_right = platform.x + platform.width
            
            if player_rect.colliderect(platform_rect):
                # Calculate overlap amounts
                overlap_top = player_bottom - platform_top
                overlap_bottom = platform_bottom - self.y
                overlap_left = player_right - platform_left
                overlap_right = platform_right - player_left
                
                # Check horizontal overlap to ensure player is actually over the platform
                horizontal_overlap = (player_right > platform_left + 1 and 
                                     player_left < platform_right - 1)
                
                # Priority 1: Landing on top of platform
                # Check if player's bottom is near platform top and was above before
                if (horizontal_overlap and
                    overlap_top < overlap_bottom and  # More overlap from top
                    overlap_top <= 25 and  # Within reasonable distance (increased tolerance)
                    prev_bottom <= platform_top + 10 and  # Was above or just touching before
                    self.vel_y >= 0):  # Moving down or stopped
                    # Snap player to top of platform
                    self.y = platform_top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    # Update rect after position change
                    player_rect.y = self.y
                    player_bottom = self.y + self.height
                    break  # Only handle one collision per frame
                # Priority 2: Hitting platform from below
                elif (overlap_bottom < overlap_top and 
                      overlap_bottom <= 25 and
                      self.vel_y < 0):  # Moving up
                    self.y = platform_bottom
                    self.vel_y = 0
                    player_rect.y = self.y
                    break
                # Priority 3: Side collisions (only if not already on ground)
                elif not self.on_ground:
                    if overlap_left < overlap_right and overlap_left <= 25 and self.vel_x > 0:
                        # Hitting left side while moving right
                        self.x = platform_left - self.width
                        self.vel_x = 0
                        player_rect.x = self.x
                        break
                    elif overlap_right < overlap_left and overlap_right <= 25 and self.vel_x < 0:
                        # Hitting right side while moving left
                        self.x = platform_right
                        self.vel_x = 0
                        player_rect.x = self.x
                        break
                # Fallback: If player is somehow inside platform, push them out upward
                elif horizontal_overlap:
                    # Push player to top of platform as fallback
                    self.y = platform_top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    player_rect.y = self.y
                    player_bottom = self.y + self.height
                    break
        
        # Prevent falling through bottom of screen
        if self.y > 800 - self.height:
            self.y = 800 - self.height
            self.vel_y = 0
            self.on_ground = True
        
        # Prevent going off left edge
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        
        # Update animation state
        new_state = self.get_animation_state()
        if new_state != self.current_state:
            self.current_state = new_state
            self.animation_frame = 0
            self.animation_timer = 0.0
        
        # Update animation frame using GIF frame durations
        if self.current_state in self.animations:
            frames = self.animations[self.current_state]
            durations = self.animation_durations.get(self.current_state, [100])
            
            if len(frames) > 1:
                # Get duration for current frame (in milliseconds)
                current_duration = durations[self.animation_frame % len(durations)]
                # Convert to game frames (assuming 60 FPS: 1000ms / 60 = ~16.67ms per frame)
                frames_per_ms = 60.0 / 1000.0
                duration_in_frames = current_duration * frames_per_ms
                
                # Update timer (increment by 1 frame per update call)
                self.animation_timer += 1.0
                
                # Advance to next frame when duration is reached
                if self.animation_timer >= duration_in_frames:
                    self.animation_frame = (self.animation_frame + 1) % len(frames)
                    self.animation_timer = 0.0
    
    def draw(self, screen, camera_x, camera_y):
        # Draw player relative to camera
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Get current animation frame
        if self.current_state in self.animations:
            frames = self.animations[self.current_state]
            if frames:
                current_frame = frames[self.animation_frame % len(frames)]
                
                # Flip horizontally if facing left
                if not self.facing_right:
                    current_frame = pygame.transform.flip(current_frame, True, False)
                
                # Draw the frame
                screen.blit(current_frame, (screen_x, screen_y))
            else:
                # Fallback if no frames
                pygame.draw.rect(screen, (255, 200, 100), (screen_x, screen_y, self.width, self.height))
        else:
            # Fallback if state not found
            pygame.draw.rect(screen, (255, 200, 100), (screen_x, screen_y, self.width, self.height))
