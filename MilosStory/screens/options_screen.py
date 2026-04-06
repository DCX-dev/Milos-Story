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


def load_options():
    """Load options dict: volume 0-100, fullscreen bool."""
    defaults = {"volume": 100, "fullscreen": False}
    try:
        path = _get_options_path()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    defaults.update(data)
    except Exception:
        pass
    defaults["volume"] = max(0, min(100, int(defaults.get("volume", 100))))
    defaults["fullscreen"] = bool(defaults.get("fullscreen", False))
    return defaults


def save_options(**kwargs):
    """Merge kwargs into options file (preserves other keys)."""
    try:
        current = load_options()
        current.update(kwargs)
        if "volume" in kwargs:
            current["volume"] = max(0, min(100, int(current["volume"])))
        if "fullscreen" in kwargs:
            current["fullscreen"] = bool(current["fullscreen"])
        path = _get_options_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"Error saving options: {e}")


def load_volume():
    """Load volume from options file (0-100). Default 100."""
    return load_options()["volume"]


def save_volume(volume):
    """Save volume only (merges with existing options)."""
    save_options(volume=max(0, min(100, int(volume))))


class OptionsScreen:
    def __init__(self, screen, game=None):
        self.screen = screen
        self.game = game
        self.volume = load_volume()
        self.dragging_slider = False
        self.fullscreen_toggle_rect = pygame.Rect(0, 0, 1, 1)
        self.relayout()
        
    def relayout(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.slider_width = min(400, max(200, sw - 80))
        self.slider_height = 24
        self.slider_track_height = 8
        self.thumb_radius = 12
        bw, bh = 118, 38
        self.back_button_rect = pygame.Rect(
            sw // 2 - bw // 2, max(380, sh - 50), bw, bh
        )
        tcx = sw // 2
        fs_y = min(sh - 120, max(400, int(sh * 0.54)))
        self.fullscreen_toggle_rect = pygame.Rect(tcx - 100, fs_y, 200, 36)
        
    def draw(self):
        """Draw options screen"""
        self.relayout()
        for y in range(self.screen.get_height()):
            color_factor = y / self.screen.get_height()
            color = (
                int(30 + color_factor * 20),
                int(30 + color_factor * 20),
                int(40 + color_factor * 30)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
        
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("OPTIONS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        label_font = pygame.font.Font(None, 36)
        label_text = label_font.render("Music Volume", True, (220, 220, 220))
        label_rect = label_text.get_rect(center=(self.screen.get_width() // 2, 230))
        self.screen.blit(label_text, label_rect)
        
        center_x = self.screen.get_width() // 2
        slider_y = 300
        track_left = center_x - self.slider_width // 2
        track_rect = pygame.Rect(track_left, slider_y - self.slider_track_height // 2,
                                 self.slider_width, self.slider_track_height)
        
        pygame.draw.rect(self.screen, (80, 80, 100), track_rect, border_radius=4)
        pygame.draw.rect(self.screen, (120, 120, 140), track_rect, width=1, border_radius=4)
        
        fill_width = int((self.volume / 100) * self.slider_width)
        if fill_width > 0:
            fill_rect = pygame.Rect(track_left, track_rect.y, fill_width, self.slider_track_height)
            pygame.draw.rect(self.screen, (100, 150, 255), fill_rect, border_radius=4)
        
        thumb_x = track_left + int((self.volume / 100) * self.slider_width)
        thumb_y = slider_y
        self.thumb_pos = (thumb_x, thumb_y)
        
        mouse_pos = pygame.mouse.get_pos()
        thumb_rect = pygame.Rect(thumb_x - self.thumb_radius, thumb_y - self.thumb_radius,
                                 self.thumb_radius * 2, self.thumb_radius * 2)
        is_hover = thumb_rect.collidepoint(mouse_pos) or self.dragging_slider
        thumb_color = (150, 200, 255) if is_hover else (120, 170, 255)
        pygame.draw.circle(self.screen, thumb_color, (thumb_x, thumb_y), self.thumb_radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (thumb_x, thumb_y), self.thumb_radius, 2)
        
        self.track_left = track_left
        self.track_right = track_left + self.slider_width
        self.slider_y = slider_y
        
        value_font = pygame.font.Font(None, 32)
        value_text = value_font.render(f"{self.volume}%", True, (255, 255, 255))
        value_rect = value_text.get_rect(center=(self.screen.get_width() // 2, 360))
        self.screen.blit(value_text, value_rect)
        
        # Fullscreen toggle
        fs_label_font = pygame.font.Font(None, 30)
        fs_label = fs_label_font.render("Fullscreen (F11)", True, (220, 220, 220))
        fs_label_rect = fs_label.get_rect(center=(self.screen.get_width() // 2, self.fullscreen_toggle_rect.y - 22))
        self.screen.blit(fs_label, fs_label_rect)
        
        fs_on = self.game.fullscreen if self.game else load_options()["fullscreen"]
        fs_hover = self.fullscreen_toggle_rect.collidepoint(mouse_pos)
        fs_bg = (90, 140, 90) if fs_on else (70, 70, 95)
        if fs_hover:
            fs_bg = tuple(min(255, c + 25) for c in fs_bg)
        pygame.draw.rect(self.screen, fs_bg, self.fullscreen_toggle_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.fullscreen_toggle_rect, width=2, border_radius=8)
        fs_btn_font = pygame.font.Font(None, 28)
        fs_txt = fs_btn_font.render("ON" if fs_on else "OFF", True, (255, 255, 255))
        fs_txt_rect = fs_txt.get_rect(center=self.fullscreen_toggle_rect.center)
        self.screen.blit(fs_txt, fs_txt_rect)
        
        is_back_hover = self.back_button_rect.collidepoint(mouse_pos)
        back_color = (100, 150, 255) if is_back_hover else (80, 130, 230)
        pygame.draw.rect(self.screen, back_color, self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_rect, width=2, border_radius=10)
        
        back_font = pygame.font.Font(None, 30)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def _get_slider_bounds(self):
        """Get slider track bounds (doesn't depend on draw being called first)"""
        self.relayout()
        center_x = self.screen.get_width() // 2
        slider_y = 300
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
                if self.fullscreen_toggle_rect.collidepoint(mouse_pos) and self.game:
                    self.game._set_fullscreen(not self.game.fullscreen)
                    return None
                if self.back_button_rect.collidepoint(mouse_pos):
                    save_volume(self.volume)
                    return "title"
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
