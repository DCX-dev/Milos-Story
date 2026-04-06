import pygame
import os
import sys
import glob
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.save_system import SaveSystem

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.save_system = SaveSystem()
        self.selected_slot = None
        self.showing_slot_selection = False
        self.hovered_slot = None  # Track which slot is being hovered
        
        # Load background image (shared for title and save screens)
        self.background_image = self._load_background()
        
        # Save slot names
        self.slot_names = ["Milo A", "Milo B", "Milo C"]
    
    def _load_background(self):
        """Load first image file from background folder (supports any format)"""
        try:
            try:
                from src.paths import get_base_path
                base_dir = get_base_path()
            except ImportError:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder_path = os.path.normpath(os.path.join(base_dir, "assets", "background"))
            
            if not os.path.exists(folder_path):
                return None
            
            # Find first image file (any format)
            image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG", 
                              "*.bmp", "*.BMP", "*.gif", "*.GIF"]
            image_files = []
            for ext in image_extensions:
                image_files.extend(glob.glob(os.path.join(folder_path, ext)))
            
            if image_files:
                bg_image = pygame.image.load(image_files[0])
                # Convert to RGBA if needed for transparency support
                if bg_image.get_flags() & pygame.SRCALPHA == 0:
                    bg_image = bg_image.convert()
                else:
                    bg_image = bg_image.convert_alpha()
                
                # Scale to screen size
                screen_width = self.screen.get_width()
                screen_height = self.screen.get_height()
                bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
                return bg_image
        except Exception as e:
            print(f"Error loading background: {e}")
        return None
    
    def refresh_for_screen(self):
        """Rescale background after window resize or fullscreen change."""
        self.background_image = self._load_background()
        
    def draw(self):
        """Draw the title screen"""
        # Background image (shared for both title and save screens)
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            # Fallback gradient for title screen, dark for save screen
            if not self.showing_slot_selection:
                for y in range(self.screen.get_height()):
                    color_factor = y / self.screen.get_height()
                    color = (
                        int(50 + color_factor * 50),
                        int(100 + color_factor * 100),
                        int(150 + color_factor * 100)
                    )
                    pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
            else:
                self.screen.fill((30, 30, 50))
        
        # Title
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Milo's Story", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Platformer Adventure", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen.get_width() // 2, 220))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        if not self.showing_slot_selection:
            h = self.screen.get_height()
            cy = self.screen.get_width() // 2
            # Compact menu buttons (font + padding)
            btn_font_sz = 34
            pad_x, pad_y = 22, 9
            br = 7
            y0 = max(300, int(h * 0.38))
            gap = 46

            play_font = pygame.font.Font(None, btn_font_sz)
            play_text = play_font.render("Click to Play", True, (255, 255, 255))
            play_rect = play_text.get_rect(center=(cy, y0))
            self.play_button_rect = play_rect.inflate(pad_x, pad_y)
            mouse_pos = pygame.mouse.get_pos()
            is_hover = self.play_button_rect.collidepoint(mouse_pos)
            button_color = (120, 170, 255) if is_hover else (100, 150, 255)
            pygame.draw.rect(self.screen, button_color, self.play_button_rect, border_radius=br)
            pygame.draw.rect(self.screen, (255, 255, 255), self.play_button_rect, width=2, border_radius=br)
            self.screen.blit(play_text, play_rect)

            credits_font = pygame.font.Font(None, btn_font_sz)
            credits_text = credits_font.render("Credits", True, (255, 255, 255))
            credits_rect = credits_text.get_rect(center=(cy, y0 + gap))
            self.credits_button_rect = credits_rect.inflate(pad_x, pad_y)
            is_credits_hover = self.credits_button_rect.collidepoint(mouse_pos)
            credits_button_color = (150, 120, 200) if is_credits_hover else (130, 100, 180)
            pygame.draw.rect(self.screen, credits_button_color, self.credits_button_rect, border_radius=br)
            pygame.draw.rect(self.screen, (255, 255, 255), self.credits_button_rect, width=2, border_radius=br)
            self.screen.blit(credits_text, credits_rect)

            options_font = pygame.font.Font(None, btn_font_sz)
            options_text = options_font.render("Options", True, (255, 255, 255))
            options_rect = options_text.get_rect(center=(cy, y0 + gap * 2))
            self.options_button_rect = options_rect.inflate(pad_x, pad_y)
            is_options_hover = self.options_button_rect.collidepoint(mouse_pos)
            options_button_color = (120, 150, 100) if is_options_hover else (100, 130, 80)
            pygame.draw.rect(self.screen, options_button_color, self.options_button_rect, border_radius=br)
            pygame.draw.rect(self.screen, (255, 255, 255), self.options_button_rect, width=2, border_radius=br)
            self.screen.blit(options_text, options_rect)

            quit_font = pygame.font.Font(None, btn_font_sz)
            quit_text = quit_font.render("Quit", True, (255, 255, 255))
            quit_rect = quit_text.get_rect(center=(cy, y0 + gap * 3))
            self.quit_button_rect = quit_rect.inflate(pad_x, pad_y)
            is_quit_hover = self.quit_button_rect.collidepoint(mouse_pos)
            quit_button_color = (200, 80, 80) if is_quit_hover else (180, 60, 60)
            pygame.draw.rect(self.screen, quit_button_color, self.quit_button_rect, border_radius=br)
            pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button_rect, width=2, border_radius=br)
            self.screen.blit(quit_text, quit_rect)

            inst_font = pygame.font.Font(None, 22)
            inst_text = inst_font.render("Select a save file to continue your adventure", True, (200, 200, 200))
            inst_rect = inst_text.get_rect(center=(cy, min(h - 24, y0 + gap * 3 + 52)))
            self.screen.blit(inst_text, inst_rect)
        else:
            # Show save slot selection
            self.draw_slot_selection()
    
    def draw_slot_selection(self):
        """Draw save slot selection screen"""
        slot_font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        title_text = title_font.render("Select Save File", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw 3 save slots (compact for smaller windows)
        slot_width = 210
        slot_height = 108
        slot_spacing = 28
        start_x = (self.screen.get_width() - (3 * slot_width + 2 * slot_spacing)) // 2
        start_y = max(200, min(250, self.screen.get_height() // 3))
        
        for i in range(3):
            slot_x = start_x + i * (slot_width + slot_spacing)
            slot_y = start_y
            
            # Slot background
            slot_rect = pygame.Rect(slot_x, slot_y, slot_width, slot_height)
            is_selected = (self.selected_slot == i)
            
            if is_selected:
                pygame.draw.rect(self.screen, (150, 200, 255), slot_rect, border_radius=10)
                pygame.draw.rect(self.screen, (255, 255, 255), slot_rect, width=4, border_radius=10)
            else:
                pygame.draw.rect(self.screen, (80, 80, 120), slot_rect, border_radius=10)
                pygame.draw.rect(self.screen, (150, 150, 150), slot_rect, width=2, border_radius=10)
            
            # Slot name (Milo A, Milo B, Milo C)
            slot_name = self.slot_names[i]
            slot_num_text = slot_font.render(slot_name, True, (255, 255, 255))
            slot_num_rect = slot_num_text.get_rect(center=(slot_x + slot_width // 2, slot_y + 22))
            self.screen.blit(slot_num_text, slot_num_rect)
            
            # Save info
            save_info = self.save_system.get_save_info(i)
            info_font = pygame.font.Font(None, 20)
            
            if save_info["exists"]:
                level_text = info_font.render(f"Level: {save_info['level']}", True, (200, 255, 200))
                level_rect = level_text.get_rect(center=(slot_x + slot_width // 2, slot_y + 52))
                self.screen.blit(level_text, level_rect)
                
                # Format timestamp
                if save_info["timestamp"]:
                    try:
                        dt = datetime.fromisoformat(save_info["timestamp"])
                        time_str = dt.strftime("%m/%d %H:%M")
                        time_text = info_font.render(time_str, True, (180, 180, 180))
                        time_rect = time_text.get_rect(center=(slot_x + slot_width // 2, slot_y + 76))
                        self.screen.blit(time_text, time_rect)
                    except:
                        pass
            else:
                empty_text = info_font.render("Empty Slot", True, (150, 150, 150))
                empty_rect = empty_text.get_rect(center=(slot_x + slot_width // 2, slot_y + 52))
                self.screen.blit(empty_text, empty_rect)
        
        # Store slot rects for mouse clicks and handle hover
        self.slot_rects = []
        self.delete_button_rects = []
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_slot = None
        
        for i in range(3):
            slot_x = start_x + i * (slot_width + slot_spacing)
            slot_rect = pygame.Rect(slot_x, start_y, slot_width, slot_height)
            self.slot_rects.append(slot_rect)
            
            save_info = self.save_system.get_save_info(i)
            is_selected = (self.selected_slot == i)
            is_hovered = slot_rect.collidepoint(mouse_pos)
            
            if is_hovered:
                self.hovered_slot = i
            
            # Highlight on hover (redraw if hovering and not selected)
            if is_hovered and not is_selected:
                pygame.draw.rect(self.screen, (100, 130, 180), slot_rect, border_radius=10)
            
            # Show delete button when hovering over non-empty file
            if is_hovered and save_info["exists"]:
                delete_button_width = 64
                delete_button_height = 24
                delete_x = slot_x + (slot_width - delete_button_width) // 2
                delete_y = slot_y + slot_height - delete_button_height - 10
                delete_rect = pygame.Rect(delete_x, delete_y, delete_button_width, delete_button_height)
                self.delete_button_rects.append((i, delete_rect))
                
                # Draw delete button
                delete_font = pygame.font.Font(None, 18)
                delete_text = delete_font.render("Delete", True, (255, 255, 255))
                pygame.draw.rect(self.screen, (200, 50, 50), delete_rect, border_radius=5)
                pygame.draw.rect(self.screen, (255, 255, 255), delete_rect, width=1, border_radius=5)
                delete_text_rect = delete_text.get_rect(center=delete_rect.center)
                self.screen.blit(delete_text, delete_text_rect)
            else:
                self.delete_button_rects.append((i, None))
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("Click a file to select | Or press 1/2/3 | ENTER/Click to confirm | ESC to cancel", True, (200, 200, 200))
        inst_y = start_y + slot_height + 30
        inst_rect = inst_text.get_rect(center=(self.screen.get_width() // 2, inst_y))
        self.screen.blit(inst_text, inst_rect)
    
    def handle_event(self, event):
        """Handle events for title screen"""
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                
                if not self.showing_slot_selection:
                    # Check if play button was clicked
                    if hasattr(self, 'play_button_rect') and self.play_button_rect.collidepoint(mouse_pos):
                        self.showing_slot_selection = True
                        self.selected_slot = 0
                    # Check if credits button was clicked
                    elif hasattr(self, 'credits_button_rect') and self.credits_button_rect.collidepoint(mouse_pos):
                        return "credits"
                    # Check if options button was clicked
                    elif hasattr(self, 'options_button_rect') and self.options_button_rect.collidepoint(mouse_pos):
                        return "options"
                    # Check if quit button was clicked
                    elif hasattr(self, 'quit_button_rect') and self.quit_button_rect.collidepoint(mouse_pos):
                        return "quit"
                else:
                    # Check delete button (for non-empty files)
                    if hasattr(self, 'delete_button_rects'):
                        for slot_idx, delete_rect in self.delete_button_rects:
                            if delete_rect and delete_rect.collidepoint(mouse_pos):
                                # Delete the file
                                if self.save_system.delete_save(slot_idx):
                                    if self.selected_slot == slot_idx:
                                        self.selected_slot = None
                                break
                    
                    # Check if a slot was clicked
                    if hasattr(self, 'slot_rects'):
                        for i, slot_rect in enumerate(self.slot_rects):
                            if slot_rect.collidepoint(mouse_pos):
                                self.selected_slot = i
                                # Clicking selected slot confirms selection
                                return ("start_game", self.selected_slot)
        
        # Keyboard handling
        if event.type == pygame.KEYDOWN:
            if not self.showing_slot_selection:
                if event.key == pygame.K_SPACE:
                    self.showing_slot_selection = True
                    self.selected_slot = 0  # Default to first slot
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
            else:
                # Slot selection
                if event.key == pygame.K_1:
                    self.selected_slot = 0
                elif event.key == pygame.K_2:
                    self.selected_slot = 1
                elif event.key == pygame.K_3:
                    self.selected_slot = 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.selected_slot is not None:
                        return ("start_game", self.selected_slot)
                elif event.key == pygame.K_ESCAPE:
                    self.showing_slot_selection = False
                    self.selected_slot = None
        
        return None
    
    def update(self):
        """Update title screen (for animations, etc.)"""
        pass
