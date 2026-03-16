import pygame
import math

class VictoryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.timer = 0
        # Initialize OK button rect
        button_width = 150
        button_height = 50
        button_x = screen.get_width() // 2 - button_width // 2
        button_y = 550
        self.ok_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
    def draw(self):
        """Draw victory screen"""
        # Background with stars effect
        self.screen.fill((20, 10, 40))  # Dark purple
        
        # Draw stars
        for i in range(100):
            x = (i * 37) % self.screen.get_width()
            y = (i * 73) % self.screen.get_height()
            brightness = (self.timer + i) % 60
            if brightness < 30:
                color = (255, 255, 255)
            else:
                color = (200, 200, 255)
            pygame.draw.circle(self.screen, color, (x, y), 2)
        
        # Victory text
        victory_font = pygame.font.Font(None, 72)
        victory_text = victory_font.render("VICTORY!", True, (255, 215, 0))
        victory_rect = victory_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(victory_text, victory_rect)
        
        # Obtained text
        obtained_font = pygame.font.Font(None, 48)
        obtained_text = obtained_font.render("You've obtained the Order of the Stone!", True, (255, 255, 100))
        obtained_rect = obtained_text.get_rect(center=(self.screen.get_width() // 2, 250))
        self.screen.blit(obtained_text, obtained_rect)
        
        # Draw stone icon
        stone_size = 80
        stone_x = self.screen.get_width() // 2 - stone_size // 2
        stone_y = 320
        pygame.draw.ellipse(self.screen, (150, 150, 200), 
                          (stone_x, stone_y, stone_size, stone_size))
        pygame.draw.ellipse(self.screen, (200, 200, 255), 
                          (stone_x, stone_y, stone_size, stone_size), 3)
        # Draw sparkle effect
        sparkle_size = 10
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            sparkle_x = stone_x + stone_size // 2 + math.cos(rad) * (stone_size // 2 + 20)
            sparkle_y = stone_y + stone_size // 2 + math.sin(rad) * (stone_size // 2 + 20)
            pygame.draw.circle(self.screen, (255, 255, 200), 
                            (int(sparkle_x), int(sparkle_y)), sparkle_size)
        
        # Continue playing text
        continue_font = pygame.font.Font(None, 36)
        continue_text = continue_font.render("If you want to keep playing, please download", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(self.screen.get_width() // 2, 450))
        self.screen.blit(continue_text, continue_rect)
        
        download_text = continue_font.render("Order of the Stone the same way you got this game", True, (200, 200, 200))
        download_rect = download_text.get_rect(center=(self.screen.get_width() // 2, 490))
        self.screen.blit(download_text, download_rect)
        
        # OK button (update position in case screen size changed)
        button_width = 150
        button_height = 50
        button_x = self.screen.get_width() // 2 - button_width // 2
        button_y = 550
        self.ok_button_rect.x = button_x
        self.ok_button_rect.y = button_y
        self.ok_button_rect.width = button_width
        self.ok_button_rect.height = button_height
        
        # Check if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.ok_button_rect.collidepoint(mouse_pos):
            button_color = (100, 200, 100)
        else:
            button_color = (80, 180, 80)
        
        pygame.draw.rect(self.screen, button_color, self.ok_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.ok_button_rect, 2)
        
        ok_font = pygame.font.Font(None, 40)
        ok_text = ok_font.render("OK", True, (255, 255, 255))
        ok_text_rect = ok_text.get_rect(center=self.ok_button_rect.center)
        self.screen.blit(ok_text, ok_text_rect)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                return "title"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if hasattr(self, 'ok_button_rect') and self.ok_button_rect.collidepoint(event.pos):
                    return "title"
        return None
    
    def update(self):
        """Update victory screen"""
        self.timer += 1
