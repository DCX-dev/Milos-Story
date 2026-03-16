import pygame

class CreditsScreen:
    def __init__(self, screen):
        self.screen = screen
        # Initialize Back button rect
        button_width = 150
        button_height = 50
        button_x = screen.get_width() // 2 - button_width // 2
        button_y = 750
        self.back_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
    def draw(self):
        """Draw credits screen"""
        # Background gradient
        for y in range(self.screen.get_height()):
            color_factor = y / self.screen.get_height()
            color = (
                int(30 + color_factor * 20),
                int(30 + color_factor * 20),
                int(40 + color_factor * 30)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
        
        # Credits title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("CREDITS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Team Banana Labs Studios
        studio_font = pygame.font.Font(None, 56)
        studio_text = studio_font.render("Team Banana Labs Studios", True, (255, 215, 0))
        studio_rect = studio_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(studio_text, studio_rect)
        
        # Music credit section
        music_title_font = pygame.font.Font(None, 36)
        music_title_text = music_title_font.render("Music", True, (200, 200, 200))
        music_title_rect = music_title_text.get_rect(center=(self.screen.get_width() // 2, 280))
        self.screen.blit(music_title_text, music_title_rect)
        
        # Music attribution text
        credit_font = pygame.font.Font(None, 28)
        attr_font = pygame.font.Font(None, 24)
        
        # Level 1 Music Credits
        level1_label = attr_font.render("Level 1:", True, (160, 160, 160))
        level1_rect = level1_label.get_rect(center=(self.screen.get_width() // 2, 310))
        self.screen.blit(level1_label, level1_rect)
        
        # Level 1: "Music by Viacheslav Starostin"
        line1_text = credit_font.render("Music by Viacheslav Starostin", True, (180, 180, 180))
        line1_rect = line1_text.get_rect(center=(self.screen.get_width() // 2, 335))
        self.screen.blit(line1_text, line1_rect)
        
        # Level 1: "from Pixabay"
        line2_text = credit_font.render("from Pixabay", True, (180, 180, 180))
        line2_rect = line2_text.get_rect(center=(self.screen.get_width() // 2, 360))
        self.screen.blit(line2_text, line2_rect)
        
        # Level 1 Attribution note
        attr_text = attr_font.render("Attribution: pixabay.com/users/viacheslavstarostin-50153119", True, (150, 150, 150))
        attr_rect = attr_text.get_rect(center=(self.screen.get_width() // 2, 385))
        self.screen.blit(attr_text, attr_rect)
        
        # Level 2 Music Credits
        level2_label = attr_font.render("Level 2:", True, (160, 160, 160))
        level2_rect = level2_label.get_rect(center=(self.screen.get_width() // 2, 415))
        self.screen.blit(level2_label, level2_rect)
        
        # Level 2: "Music by HitsLab"
        level2_line1 = credit_font.render("Music by HitsLab", True, (180, 180, 180))
        level2_line1_rect = level2_line1.get_rect(center=(self.screen.get_width() // 2, 440))
        self.screen.blit(level2_line1, level2_line1_rect)
        
        # Level 2: "from Pixabay"
        level2_line2 = credit_font.render("from Pixabay", True, (180, 180, 180))
        level2_line2_rect = level2_line2.get_rect(center=(self.screen.get_width() // 2, 465))
        self.screen.blit(level2_line2, level2_line2_rect)
        
        # Level 2 Attribution note
        level2_attr_text = attr_font.render("Attribution: pixabay.com/users/hitslab-47305729", True, (150, 150, 150))
        level2_attr_rect = level2_attr_text.get_rect(center=(self.screen.get_width() // 2, 490))
        self.screen.blit(level2_attr_text, level2_attr_rect)
        
        # Level 3 Music Credits
        level3_label = attr_font.render("Level 3:", True, (160, 160, 160))
        level3_rect = level3_label.get_rect(center=(self.screen.get_width() // 2, 520))
        self.screen.blit(level3_label, level3_rect)
        
        # Level 3: "Music by Mykola Sosin"
        level3_line1 = credit_font.render("Music by Mykola Sosin", True, (180, 180, 180))
        level3_line1_rect = level3_line1.get_rect(center=(self.screen.get_width() // 2, 545))
        self.screen.blit(level3_line1, level3_line1_rect)
        
        # Level 3: "from Pixabay"
        level3_line2 = credit_font.render("from Pixabay", True, (180, 180, 180))
        level3_line2_rect = level3_line2.get_rect(center=(self.screen.get_width() // 2, 570))
        self.screen.blit(level3_line2, level3_line2_rect)
        
        # Level 3 Attribution note
        level3_attr_text = attr_font.render("Attribution: pixabay.com/users/tatamusic-51344851", True, (150, 150, 150))
        level3_attr_rect = level3_attr_text.get_rect(center=(self.screen.get_width() // 2, 595))
        self.screen.blit(level3_attr_text, level3_attr_rect)
        
        # Levels 4-10 Music Credits
        level4_10_label = attr_font.render("Levels 4-10:", True, (160, 160, 160))
        level4_10_rect = level4_10_label.get_rect(center=(self.screen.get_width() // 2, 625))
        self.screen.blit(level4_10_label, level4_10_rect)
        
        # Levels 4-10: "Music by Maksym Malko"
        level4_10_line1 = credit_font.render("Music by Maksym Malko", True, (180, 180, 180))
        level4_10_line1_rect = level4_10_line1.get_rect(center=(self.screen.get_width() // 2, 650))
        self.screen.blit(level4_10_line1, level4_10_line1_rect)
        
        # Levels 4-10: "from Pixabay"
        level4_10_line2 = credit_font.render("from Pixabay", True, (180, 180, 180))
        level4_10_line2_rect = level4_10_line2.get_rect(center=(self.screen.get_width() // 2, 675))
        self.screen.blit(level4_10_line2, level4_10_line2_rect)
        
        # Levels 4-10 Attribution note
        level4_10_attr_text = attr_font.render("Attribution: pixabay.com/users/backgroundmusicforvideos-46459014", True, (150, 150, 150))
        level4_10_attr_rect = level4_10_attr_text.get_rect(center=(self.screen.get_width() // 2, 700))
        self.screen.blit(level4_10_attr_text, level4_10_attr_rect)
        
        # License note (applies to all music)
        license_text = attr_font.render("Music licensed under Pixabay License", True, (150, 150, 150))
        license_rect = license_text.get_rect(center=(self.screen.get_width() // 2, 725))
        self.screen.blit(license_text, license_rect)
        
        # Back button
        button_width = 150
        button_height = 50
        button_x = self.screen.get_width() // 2 - button_width // 2
        button_y = 750
        self.back_button_rect.x = button_x
        self.back_button_rect.y = button_y
        self.back_button_rect.width = button_width
        self.back_button_rect.height = button_height
        
        # Check if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button_rect.collidepoint(mouse_pos):
            button_color = (100, 150, 255)
        else:
            button_color = (80, 130, 230)
        
        pygame.draw.rect(self.screen, button_color, self.back_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_rect, 2)
        
        back_font = pygame.font.Font(None, 40)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                return "title"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(event.pos):
                    return "title"
        return None
    
    def update(self):
        """Update credits screen"""
        pass
