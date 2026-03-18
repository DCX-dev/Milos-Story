import pygame
import os
import json

def _get_options_path():
    """Get path to options config file"""
    try:
        from src.paths import get_data_path
        return os.path.normpath(os.path.join(get_data_path(), "options.json"))
    except ImportError:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.normpath(os.path.join(base_dir, "data", "options.json"))

def load_volume():
    """Load volume from options file (0-100). Default 100."""
    try:
        path = _get_options_path()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return max(0, min(100, int(data.get("volume", 100))))
    except Exception:
        pass
    return 100

def save_volume(volume):
    """Save volume to options file"""
    try:
        path = _get_options_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({"volume": max(0, min(100, int(volume)))}, f, indent=2)
    except Exception as e:
        print(f"Error saving options: {e}")

class OptionsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.volume = load_volume()
        self.dragging_slider = False
        
        # Slider dimensions
        self.slider_width = 400
        self.slider_height = 24
        self.slider_track_height = 8
        self.thumb_radius = 12
        
        # Back button rect (set here so it exists before first draw)
        bw, bh = 150, 50
        self.back_button_rect = pygame.Rect(
            screen.get_width() // 2 - bw // 2, 550, bw, bh
        )
        
    def draw(self):
        """Draw options screen"""
        # Background gradient
        for y in range(self.screen.get_height()):
            color_factor = y / self.screen.get_height()
            color = (
                int(30 + color_factor * 20),
                int(30 + color_factor * 20),
                int(40 + color_factor * 30)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
        
        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("OPTIONS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # Volume label
        label_font = pygame.font.Font(None, 36)
        label_text = label_font.render("Music Volume", True, (220, 220, 220))
        label_rect = label_text.get_rect(center=(self.screen.get_width() // 2, 280))
        self.screen.blit(label_text, label_rect)
        
        # Slider track
        center_x = self.screen.get_width() // 2
        slider_y = 350
        track_left = center_x - self.slider_width // 2
        track_rect = pygame.Rect(track_left, slider_y - self.slider_track_height // 2,
                                 self.slider_width, self.slider_track_height)
        
        # Track background
        pygame.draw.rect(self.screen, (80, 80, 100), track_rect, border_radius=4)
        pygame.draw.rect(self.screen, (120, 120, 140), track_rect, width=1, border_radius=4)
        
        # Filled portion (0-100)
        fill_width = int((self.volume / 100) * self.slider_width)
        if fill_width > 0:
            fill_rect = pygame.Rect(track_left, track_rect.y, fill_width, self.slider_track_height)
            pygame.draw.rect(self.screen, (100, 150, 255), fill_rect, border_radius=4)
        
        # Thumb position
        thumb_x = track_left + int((self.volume / 100) * self.slider_width)
        thumb_y = slider_y
        self.thumb_pos = (thumb_x, thumb_y)
        
        # Thumb circle
        mouse_pos = pygame.mouse.get_pos()
        thumb_rect = pygame.Rect(thumb_x - self.thumb_radius, thumb_y - self.thumb_radius,
                                 self.thumb_radius * 2, self.thumb_radius * 2)
        is_hover = thumb_rect.collidepoint(mouse_pos) or self.dragging_slider
        thumb_color = (150, 200, 255) if is_hover else (120, 170, 255)
        pygame.draw.circle(self.screen, thumb_color, (thumb_x, thumb_y), self.thumb_radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (thumb_x, thumb_y), self.thumb_radius, 2)
        
        # Store track rect for click/drag
        self.track_left = track_left
        self.track_right = track_left + self.slider_width
        self.slider_y = slider_y
        
        # Volume value text
        value_font = pygame.font.Font(None, 32)
        value_text = value_font.render(f"{self.volume}%", True, (255, 255, 255))
        value_rect = value_text.get_rect(center=(self.screen.get_width() // 2, 420))
        self.screen.blit(value_text, value_rect)
        
        # Back button
        button_width = 150
        button_height = 50
        button_x = self.screen.get_width() // 2 - button_width // 2
        button_y = 550
        self.back_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        is_back_hover = self.back_button_rect.collidepoint(mouse_pos)
        back_color = (100, 150, 255) if is_back_hover else (80, 130, 230)
        pygame.draw.rect(self.screen, back_color, self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_rect, width=2, border_radius=10)
        
        back_font = pygame.font.Font(None, 40)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def _get_slider_bounds(self):
        """Get slider track bounds (doesn't depend on draw being called first)"""
        center_x = self.screen.get_width() // 2
        slider_y = 350
        track_left = center_x - self.slider_width // 2
        track_right = track_left + self.slider_width
        return track_left, track_right, slider_y
    
    def _volume_from_x(self, x):
        """Convert screen x to volume 0-100"""
        track_left, track_right, _ = self._get_slider_bounds()
        rel = (x - track_left) / self.slider_width
        return max(0, min(100, int(rel * 100)))
    
    def _is_slider_click(self, pos):
        """Check if click is on slider (track or thumb)"""
        track_left, track_right, slider_y = self._get_slider_bounds()
        # Whole slider hit area: full track width, generous height for thumb
        return (track_left <= pos[0] <= track_right and
                abs(pos[1] - slider_y) <= self.thumb_radius * 3)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                save_volume(self.volume)
                return "title"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.back_button_rect.collidepoint(mouse_pos):
                    save_volume(self.volume)
                    return "title"
                # Check if click on slider track or thumb
                if self._is_slider_click(mouse_pos):
                    self.dragging_slider = True
                    self.volume = self._volume_from_x(mouse_pos[0])
                    save_volume(self.volume)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging_slider:
                    save_volume(self.volume)
                self.dragging_slider = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider:
                self.volume = self._volume_from_x(event.pos[0])
                save_volume(self.volume)
        return None
    
    def update(self):
        """Update options screen - poll mouse position when dragging (ensures smooth sliding with single click)"""
        if self.dragging_slider and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.volume = self._volume_from_x(mouse_pos[0])
            save_volume(self.volume)
    
    def get_volume(self):
        """Return current volume 0-100"""
        return self.volume
