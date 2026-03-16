import pygame

class LevelSelector:
    def __init__(self, screen):
        self.screen = screen
        self.selected_level = 1
        
    def draw(self):
        """Draw level selector screen"""
        # Background
        self.screen.fill((20, 20, 40))
        
        # Title
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("DEBUG: Select Level", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw level buttons (1-10)
        button_width = 150
        button_height = 80
        button_spacing = 20
        start_x = (self.screen.get_width() - (5 * button_width + 4 * button_spacing)) // 2
        start_y = 250
        
        self.level_buttons = []
        for i in range(10):
            row = i // 5
            col = i % 5
            button_x = start_x + col * (button_width + button_spacing)
            button_y = start_y + row * (button_height + button_spacing)
            
            level_num = i + 1
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.level_buttons.append((level_num, button_rect))
            
            # Button color based on selection
            is_selected = (self.selected_level == level_num)
            button_color = (100, 200, 255) if is_selected else (60, 60, 100)
            hover_color = (120, 220, 255)
            
            # Check hover
            mouse_pos = pygame.mouse.get_pos()
            is_hover = button_rect.collidepoint(mouse_pos)
            if is_hover and not is_selected:
                button_color = hover_color
            
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, width=3 if is_selected else 2, border_radius=10)
            
            # Level number
            level_font = pygame.font.Font(None, 48)
            level_text = level_font.render(str(level_num), True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(level_text, level_rect)
            
            # Boss indicator for level 10
            if level_num == 10:
                boss_font = pygame.font.Font(None, 20)
                boss_text = boss_font.render("BOSS", True, (255, 100, 100))
                boss_rect = boss_text.get_rect(center=(button_x + button_width // 2, button_y + button_height - 15))
                self.screen.blit(boss_text, boss_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 28)
        inst_text = inst_font.render("Click a level or press 1-0 to select | ENTER/Click to start | ESC to cancel", True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(self.screen.get_width() // 2, 600))
        self.screen.blit(inst_text, inst_rect)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                for level_num, button_rect in self.level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_level = level_num
                        return ("start_level", level_num)
        
        if event.type == pygame.KEYDOWN:
            # Number keys 1-9 and 0 for level 10
            if pygame.K_1 <= event.key <= pygame.K_9:
                self.selected_level = event.key - pygame.K_0
            elif event.key == pygame.K_0:
                self.selected_level = 10
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return ("start_level", self.selected_level)
            elif event.key == pygame.K_ESCAPE:
                return "cancel"
        
        return None
    
    def update(self):
        """Update level selector"""
        pass
