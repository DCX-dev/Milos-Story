import pygame
import math

class Rock:
    def __init__(self, x, y, target_x, target_y):
        """Create a rock at (x, y) heading towards (target_x, target_y)"""
        self.x = float(x)
        self.y = float(y)
        self.width = 10
        self.height = 10
        self.speed = 12
        self.is_alive = True
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0.01:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            # Default: throw up if target is same position
            self.vel_x = 0.0
            self.vel_y = -self.speed
    
    def update(self):
        """Update rock position"""
        if not self.is_alive:
            return
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Remove if way off screen
        if self.x < -200 or self.x > 1400 or self.y < -200 or self.y > 1000:
            self.is_alive = False
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def draw(self, screen, camera_x, camera_y):
        """Draw the rock"""
        if not self.is_alive:
            return
        
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Only draw if visible
        if screen_x < -20 or screen_x > screen.get_width() + 20:
            return
        if screen_y < -20 or screen_y > screen.get_height() + 20:
            return
        
        # Draw simple gray circle
        center_x = screen_x + self.width // 2
        center_y = screen_y + self.height // 2
        pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), self.width // 2)
        pygame.draw.circle(screen, (60, 60, 60), (center_x, center_y), self.width // 2 - 1)
