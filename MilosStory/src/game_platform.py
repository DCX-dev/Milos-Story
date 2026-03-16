import pygame

class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, screen, camera_x, camera_y):
        # Draw platform relative to camera
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Only draw if on screen
        if (screen_x + self.width > 0 and screen_x < screen.get_width() and
            screen_y + self.height > 0 and screen_y < screen.get_height()):
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
            
            # Add a border for depth
            border_color = tuple(max(0, c - 30) for c in self.color)
            pygame.draw.rect(screen, border_color, (screen_x, screen_y, self.width, self.height), 2)
