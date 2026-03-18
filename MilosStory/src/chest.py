import pygame

class Chest:
    """Collectible chest - gives arrows (14) or damage upgrade (+1 heart)"""
    def __init__(self, x, y, chest_type="arrows"):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.chest_type = chest_type  # "arrows" or "damage"
        self.collected = False
        self.color = (180, 140, 80)  # Wood brown
        self.highlight = (220, 180, 100)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def collect(self, player_rect):
        """Check if player is near and collect. Returns (arrows, damage) or None"""
        if self.collected:
            return None
        # Expand rect for "near" - about 80px
        expand = 40
        check_rect = self.get_rect().inflate(expand, expand)
        if check_rect.colliderect(player_rect):
            self.collected = True
            if self.chest_type == "arrows":
                return (14, 0)
            else:  # damage
                return (0, 1)
        return None
    
    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)
        if sx < -60 or sx > screen.get_width() + 60 or sy < -60 or sy > screen.get_height() + 60:
            return
        # Chest body
        pygame.draw.rect(screen, self.color, (sx, sy, self.width, self.height))
        pygame.draw.rect(screen, self.highlight, (sx, sy, self.width, self.height), 2)
        # Lid
        lid_color = (160, 120, 60)
        pygame.draw.rect(screen, lid_color, (sx + 5, sy - 8, self.width - 10, 12))
        # Icon hint
        if self.chest_type == "arrows":
            # Small arrow symbol
            pygame.draw.line(screen, (100, 80, 40), (sx + self.width//2 - 5, sy + self.height//2),
                           (sx + self.width//2 + 5, sy + self.height//2), 2)
            pygame.draw.polygon(screen, (100, 80, 40), [(sx + self.width//2 + 8, sy + self.height//2 - 3),
                (sx + self.width//2 + 8, sy + self.height//2 + 3), (sx + self.width//2 + 14, sy + self.height//2)])
        else:
            # Heart/damage symbol - small plus or star
            cx, cy = sx + self.width//2, sy + self.height//2
            pygame.draw.line(screen, (180, 60, 60), (cx - 5, cy), (cx + 5, cy), 2)
            pygame.draw.line(screen, (180, 60, 60), (cx, cy - 5), (cx, cy + 5), 2)
