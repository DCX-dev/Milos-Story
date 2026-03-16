import pygame
import math

class Arrow:
    def __init__(self, x, y, target_x, target_y):
        self.x = float(x)
        self.y = float(y)
        self.width = 20
        self.height = 5
        self.speed = 18
        self.is_alive = True
        
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0.01:
            self.vel_x = (dx / dist) * self.speed
            self.vel_y = (dy / dist) * self.speed
            self.angle = math.atan2(dy, dx)
        else:
            self.vel_x = 0.0
            self.vel_y = -self.speed
            self.angle = -math.pi / 2
    
    def update(self):
        if not self.is_alive:
            return
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x < -200 or self.x > 1400 or self.y < -200 or self.y > 1000:
            self.is_alive = False
    
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def draw(self, screen, camera_x, camera_y):
        if not self.is_alive:
            return
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)
        if sx < -30 or sx > screen.get_width() + 30 or sy < -30 or sy > screen.get_height() + 30:
            return
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (139, 90, 43), (0, 0, self.width - 5, self.height))
        pygame.draw.polygon(surf, (80, 50, 20), [(self.width - 5, 0), (self.width, self.height // 2), (self.width - 5, self.height)])
        rot = pygame.transform.rotate(surf, math.degrees(-self.angle))
        rect = rot.get_rect(center=(sx + self.width // 2, sy + self.height // 2))
        screen.blit(rot, rect)
