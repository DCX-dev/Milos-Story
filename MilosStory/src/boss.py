import pygame
import math

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 120
        self.max_health = 100
        self.health = self.max_health
        self.speed = 2
        self.vel_x = self.speed
        self.vel_y = 0
        
        # Boss movement pattern
        self.move_timer = 0
        self.attack_timer = 0
        self.attack_cooldown = 120  # Frames between attacks
        
        # Boss state
        self.is_alive = True
        self.color = (200, 50, 50)  # Dark red
        
        # Attack projectiles
        self.projectiles = []
        
    def update(self, platforms, player_x, player_y):
        """Update boss AI and movement"""
        if not self.is_alive:
            return
        
        self.move_timer += 1
        self.attack_timer += 1
        
        # Simple movement: move back and forth
        self.x += self.vel_x
        
        # Bounce off edges
        if self.x <= 100 or self.x >= 1100 - self.width:
            self.vel_x = -self.vel_x
        
        # Attack player periodically
        if self.attack_timer >= self.attack_cooldown:
            self.attack(player_x, player_y)
            self.attack_timer = 0
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile["x"] += projectile["vel_x"]
            projectile["y"] += projectile["vel_y"]
            
            # Remove if off screen
            if (projectile["x"] < -50 or projectile["x"] > 1250 or
                projectile["y"] < -50 or projectile["y"] > 850):
                self.projectiles.remove(projectile)
    
    def attack(self, player_x, player_y):
        """Shoot projectiles at player"""
        # Calculate direction to player
        dx = player_x - (self.x + self.width // 2)
        dy = player_y - (self.y + self.height // 2)
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Create projectile
            projectile = {
                "x": self.x + self.width // 2,
                "y": self.y + self.height // 2,
                "vel_x": dx * 5,
                "vel_y": dy * 5,
                "radius": 10
            }
            self.projectiles.append(projectile)
    
    def take_damage(self, amount):
        """Take damage from player"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
    
    def check_projectile_collision(self, player_rect):
        """Check if projectiles hit player"""
        hits = []
        for projectile in self.projectiles[:]:
            proj_rect = pygame.Rect(
                projectile["x"] - projectile["radius"],
                projectile["y"] - projectile["radius"],
                projectile["radius"] * 2,
                projectile["radius"] * 2
            )
            if proj_rect.colliderect(player_rect):
                hits.append(projectile)
                self.projectiles.remove(projectile)
        return len(hits) > 0
    
    def get_rect(self):
        """Get boss collision rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen, camera_x, camera_y):
        """Draw boss"""
        if not self.is_alive:
            return
        
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Draw boss body
        pygame.draw.ellipse(screen, self.color, (screen_x, screen_y, self.width, self.height))
        pygame.draw.ellipse(screen, (255, 0, 0), (screen_x, screen_y, self.width, self.height), 3)
        
        # Draw eyes
        eye_size = 15
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(screen_x + self.width // 3), int(screen_y + self.height // 3)), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(screen_x + 2 * self.width // 3), int(screen_y + self.height // 3)), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(screen_x + self.width // 3), int(screen_y + self.height // 3)), eye_size // 2)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(screen_x + 2 * self.width // 3), int(screen_y + self.height // 3)), eye_size // 2)
        
        # Draw health bar
        bar_width = 100
        bar_height = 10
        bar_x = screen_x + (self.width - bar_width) // 2
        bar_y = screen_y - 20
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw projectiles
        for projectile in self.projectiles:
            proj_x = projectile["x"] - camera_x
            proj_y = projectile["y"] - camera_y
            pygame.draw.circle(screen, (255, 100, 100), 
                            (int(proj_x), int(proj_y)), projectile["radius"])
            pygame.draw.circle(screen, (255, 0, 0), 
                            (int(proj_x), int(proj_y)), projectile["radius"], 2)
