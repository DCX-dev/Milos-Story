import pygame
import math

class Enemy:
    def __init__(self, x, y, gravity=0.7, speed=2.0, jump_strength=-15):
        self.start_x = x
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
        
        # Enemy state
        self.is_alive = True
        self.max_health = 3
        self.health = self.max_health
        self.color = (200, 50, 50)  # Red stick figure
        self.facing_right = True
        
        # AI state
        self.chase_player = True
        self.patrol_distance = 200
        self.patrol_left = x
        self.patrol_right = x + self.patrol_distance
        self.jump_cooldown = 0
        
    def update(self, platforms, player_x=None, player_y=None):
        """Update enemy AI with proper physics"""
        if not self.is_alive:
            return
        
        # Update jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        
        # Determine movement direction
        if self.chase_player and player_x is not None:
            # Chase player
            if player_x < self.x - 20:
                self.vel_x = -self.speed
                self.facing_right = False
            elif player_x > self.x + 20:
                self.vel_x = self.speed
                self.facing_right = True
            else:
                self.vel_x = 0
            
            # Try to jump if player is above and we're on ground
            if self.on_ground and player_y is not None and player_y < self.y - 50:
                if self.jump_cooldown == 0:
                    self.jump()
        else:
            # Patrol mode
            self.vel_x = self.speed if self.facing_right else -self.speed
            
            # Reverse direction at patrol boundaries
            if self.x <= self.patrol_left:
                self.vel_x = self.speed
                self.facing_right = True
            elif self.x >= self.patrol_right:
                self.vel_x = -self.speed
                self.facing_right = False
        
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Reset ground state
        self.on_ground = False
        
        # Collision detection with platforms (same as player)
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            
            if enemy_rect.colliderect(platform_rect):
                # Check if landing on top of platform
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Check if hitting platform from below
                elif self.vel_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                # Check side collisions
                elif self.vel_x > 0:  # Moving right
                    self.x = platform.x - self.width
                    self.vel_x = 0
                    # Try to jump over obstacle
                    if self.on_ground and self.jump_cooldown == 0:
                        self.jump()
                elif self.vel_x < 0:  # Moving left
                    self.x = platform.x + platform.width
                    self.vel_x = 0
                    # Try to jump over obstacle
                    if self.on_ground and self.jump_cooldown == 0:
                        self.jump()
        
        # Prevent falling through bottom of screen
        if self.y > 800 - self.height:
            self.y = 800 - self.height
            self.vel_y = 0
            self.on_ground = True
        
        # Prevent going off left edge
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
    
    def jump(self):
        """Jump like player"""
        if self.on_ground and self.jump_cooldown == 0:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.jump_cooldown = 30  # Cooldown between jumps
    
    def take_damage(self, amount=1):
        """Take damage from rock"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
    
    def get_rect(self):
        """Get enemy collision rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen, camera_x, camera_y):
        """Draw stick figure enemy"""
        if not self.is_alive:
            return
        
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Only draw if on screen
        if (screen_x + self.width < 0 or screen_x > screen.get_width() or
            screen_y + self.height < 0 or screen_y > screen.get_height()):
            return
        
        # Draw stick figure (bigger and more visible)
        # Head
        head_radius = 12
        head_x = int(screen_x + self.width // 2)
        head_y = int(screen_y + head_radius)
        pygame.draw.circle(screen, self.color, (head_x, head_y), head_radius)
        pygame.draw.circle(screen, (0, 0, 0), (head_x, head_y), head_radius, 2)
        
        # Body (line)
        body_start_y = head_y + head_radius
        body_end_y = screen_y + self.height - 15
        pygame.draw.line(screen, self.color, (head_x, body_start_y), 
                       (head_x, body_end_y), 4)
        
        # Arms
        arm_y = body_start_y + 10
        arm_length = 18
        arm_angle = 45 if self.facing_right else 135
        arm_rad = math.radians(arm_angle)
        left_arm_x = head_x + int(math.cos(arm_rad) * arm_length)
        left_arm_y = arm_y + int(math.sin(arm_rad) * arm_length)
        right_arm_x = head_x - int(math.cos(arm_rad) * arm_length)
        right_arm_y = arm_y + int(math.sin(arm_rad) * arm_length)
        
        pygame.draw.line(screen, self.color, (head_x, arm_y), 
                       (left_arm_x, left_arm_y), 3)
        pygame.draw.line(screen, self.color, (head_x, arm_y), 
                       (right_arm_x, right_arm_y), 3)
        
        # Legs
        leg_y = body_end_y
        leg_length = 15
        leg_angle = 30 if self.facing_right else 150
        leg_rad = math.radians(leg_angle)
        left_leg_x = head_x + int(math.cos(leg_rad) * leg_length)
        left_leg_y = leg_y + int(math.sin(leg_rad) * leg_length)
        right_leg_x = head_x - int(math.cos(leg_rad) * leg_length)
        right_leg_y = leg_y + int(math.sin(leg_rad) * leg_length)
        
        pygame.draw.line(screen, self.color, (head_x, leg_y), 
                       (left_leg_x, left_leg_y), 3)
        pygame.draw.line(screen, self.color, (head_x, leg_y), 
                       (right_leg_x, right_leg_y), 3)
        
        # Eyes
        eye_size = 3
        eye_offset = 4
        pygame.draw.circle(screen, (255, 255, 255), 
                         (head_x - eye_offset, head_y - 2), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (head_x + eye_offset, head_y - 2), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (head_x - eye_offset, head_y - 2), eye_size - 1)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (head_x + eye_offset, head_y - 2), eye_size - 1)
