import pygame
import os
import platform

class FileBrowser:
    def __init__(self, screen, start_path=None):
        self.screen = screen
        if start_path is None:
            start_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Normalize path and handle spaces/special characters
        try:
            self.current_path = os.path.abspath(os.path.normpath(start_path))
            # Verify path exists and is accessible
            if not os.path.exists(self.current_path):
                # Fallback to Desktop if path doesn't exist
                self.current_path = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.isdir(self.current_path):
                # If not a directory, use parent directory
                self.current_path = os.path.dirname(self.current_path) if os.path.isfile(self.current_path) else os.path.join(os.path.expanduser("~"), "Desktop")
        except Exception:
            # Fallback to Desktop on any error
            self.current_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.selected_file = None
        self.scroll_offset = 0
        self.items_per_page = 15
        
    def get_files_and_folders(self):
        """Get list of files and folders in current directory"""
        items = []
        try:
            # Ensure path is valid and accessible
            if not os.path.exists(self.current_path) or not os.path.isdir(self.current_path):
                return items
            
            for item in sorted(os.listdir(self.current_path)):
                try:
                    # Skip macOS metadata files (starting with ._)
                    if item.startswith('._'):
                        continue
                    
                    # Skip hidden files (starting with .) except for current/parent directory
                    if item.startswith('.') and item not in ['.', '..']:
                        continue
                    
                    # Use normpath to handle spaces and special characters properly
                    item_path = os.path.normpath(os.path.join(self.current_path, item))
                    
                    # Verify path exists before checking type
                    if not os.path.exists(item_path):
                        continue
                    
                    if os.path.isdir(item_path):
                        items.append(("folder", item, item_path))
                    elif os.path.isfile(item_path) and item.lower().endswith('.json'):
                        items.append(("file", item, item_path))
                except (OSError, PermissionError, UnicodeDecodeError):
                    # Skip items that can't be accessed
                    continue
        except (PermissionError, OSError, UnicodeDecodeError) as e:
            # Return empty list if directory can't be accessed
            pass
        return items
    
    def draw(self):
        """Draw file browser"""
        # Background
        self.screen.fill((30, 30, 40))
        
        # Title bar
        title_font = pygame.font.Font(None, 36)
        title_text = title_font.render("Select Backup File", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Current path (truncate if too long)
        path_font = pygame.font.Font(None, 20)
        display_path = self.current_path
        max_path_width = self.screen.get_width() - 20
        path_surface = path_font.render(f"Path: {display_path}", True, (200, 200, 200))
        if path_surface.get_width() > max_path_width:
            # Truncate from beginning
            while path_surface.get_width() > max_path_width and len(display_path) > 20:
                display_path = "..." + display_path[-(max_path_width // 10):]
                path_surface = path_font.render(f"Path: {display_path}", True, (200, 200, 200))
        self.screen.blit(path_surface, (10, 60))
        
        # Back button
        back_font = pygame.font.Font(None, 24)
        back_text = back_font.render("← Back", True, (150, 150, 255))
        back_rect = pygame.Rect(10, 90, 100, 30)
        mouse_pos = pygame.mouse.get_pos()
        is_hover_back = back_rect.collidepoint(mouse_pos)
        back_color = (100, 100, 200) if is_hover_back else (80, 80, 150)
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, width=1, border_radius=5)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        self.back_button_rect = back_rect
        
        # File list area
        list_y_start = 130
        list_height = self.screen.get_height() - list_y_start - 100
        list_rect = pygame.Rect(10, list_y_start, self.screen.get_width() - 20, list_height)
        pygame.draw.rect(self.screen, (20, 20, 30), list_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), list_rect, width=2)
        
        # Get files and folders
        items = self.get_files_and_folders()
        
        # Scroll handling
        item_height = 35
        visible_items = min(len(items), self.items_per_page)
        
        # Draw items
        self.item_rects = []
        for i in range(visible_items):
            idx = i + self.scroll_offset
            if idx >= len(items):
                break
            
            item_type, item_name, item_path = items[idx]
            item_y = list_y_start + 10 + i * item_height
            
            item_rect = pygame.Rect(20, item_y, list_rect.width - 40, item_height - 5)
            self.item_rects.append((item_type, item_name, item_path, item_rect))
            
            # Highlight if selected or hovered
            is_selected = (self.selected_file == item_path)
            is_hovered = item_rect.collidepoint(mouse_pos)
            
            if is_selected:
                pygame.draw.rect(self.screen, (100, 150, 255), item_rect, border_radius=3)
            elif is_hovered:
                pygame.draw.rect(self.screen, (60, 60, 80), item_rect, border_radius=3)
            
            # Draw icon and name
            item_font = pygame.font.Font(None, 24)
            if item_type == "folder":
                icon_text = "📁 "
                text_color = (150, 200, 255)
            else:
                icon_text = "📄 "
                text_color = (255, 255, 255)
            
            display_text = icon_text + item_name
            if len(display_text) > 50:
                display_text = display_text[:47] + "..."
            
            text_surface = item_font.render(display_text, True, text_color)
            text_x = item_rect.x + 5
            text_y = item_rect.y + (item_rect.height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
        
        # Scroll buttons
        if self.scroll_offset > 0:
            up_rect = pygame.Rect(self.screen.get_width() - 40, list_y_start + 10, 30, 30)
            is_hover_up = up_rect.collidepoint(mouse_pos)
            up_color = (100, 100, 150) if is_hover_up else (70, 70, 100)
            pygame.draw.rect(self.screen, up_color, up_rect, border_radius=3)
            up_text = item_font.render("↑", True, (255, 255, 255))
            up_text_rect = up_text.get_rect(center=up_rect.center)
            self.screen.blit(up_text, up_text_rect)
            self.up_button_rect = up_rect
        else:
            self.up_button_rect = None
        
        if self.scroll_offset + self.items_per_page < len(items):
            down_rect = pygame.Rect(self.screen.get_width() - 40, list_y_start + list_height - 40, 30, 30)
            is_hover_down = down_rect.collidepoint(mouse_pos)
            down_color = (100, 100, 150) if is_hover_down else (70, 70, 100)
            pygame.draw.rect(self.screen, down_color, down_rect, border_radius=3)
            down_text = item_font.render("↓", True, (255, 255, 255))
            down_text_rect = down_text.get_rect(center=down_rect.center)
            self.screen.blit(down_text, down_text_rect)
            self.down_button_rect = down_rect
        else:
            self.down_button_rect = None
        
        # Bottom buttons
        button_y = self.screen.get_height() - 60
        button_font = pygame.font.Font(None, 32)
        
        # Open button (only enabled if file selected)
        open_text = button_font.render("Open", True, (255, 255, 255))
        open_width = 120
        open_height = 50
        open_x = (self.screen.get_width() - open_width) // 2
        open_rect = pygame.Rect(open_x, button_y, open_width, open_height)
        
        is_hover_open = open_rect.collidepoint(mouse_pos)
        has_selection = self.selected_file is not None and os.path.isfile(self.selected_file)
        open_color = (100, 200, 100) if (has_selection and is_hover_open) else ((80, 180, 80) if has_selection else (60, 60, 60))
        
        pygame.draw.rect(self.screen, open_color, open_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), open_rect, width=2 if has_selection else 1, border_radius=10)
        open_text_rect = open_text.get_rect(center=open_rect.center)
        self.screen.blit(open_text, open_text_rect)
        self.open_button_rect = open_rect
        
        # Cancel button
        cancel_text = button_font.render("Cancel", True, (255, 255, 255))
        cancel_width = 120
        cancel_height = 50
        cancel_x = open_x - cancel_width - 20
        cancel_rect = pygame.Rect(cancel_x, button_y, cancel_width, cancel_height)
        
        is_hover_cancel = cancel_rect.collidepoint(mouse_pos)
        cancel_color = (200, 100, 100) if is_hover_cancel else (180, 80, 80)
        
        pygame.draw.rect(self.screen, cancel_color, cancel_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), cancel_rect, width=2, border_radius=10)
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        self.screen.blit(cancel_text, cancel_text_rect)
        self.cancel_button_rect = cancel_rect
        
        # Selected file info
        if self.selected_file:
            info_font = pygame.font.Font(None, 20)
            file_name = os.path.basename(self.selected_file)
            info_text = info_font.render(f"Selected: {file_name}", True, (150, 255, 150))
            self.screen.blit(info_text, (10, button_y - 25))
    
    def handle_event(self, event):
        """Handle events for file browser"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                
                # Check back button
                if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(mouse_pos):
                    try:
                        parent = os.path.normpath(os.path.dirname(self.current_path))
                        if parent != self.current_path and os.path.exists(parent):  # Not at root and exists
                            self.current_path = parent
                            self.scroll_offset = 0
                            self.selected_file = None
                    except (OSError, ValueError):
                        # Can't go back, stay where we are
                        pass
                
                # Check scroll buttons
                if hasattr(self, 'up_button_rect') and self.up_button_rect and self.up_button_rect.collidepoint(mouse_pos):
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                
                if hasattr(self, 'down_button_rect') and self.down_button_rect and self.down_button_rect.collidepoint(mouse_pos):
                    items = self.get_files_and_folders()
                    if self.scroll_offset + self.items_per_page < len(items):
                        self.scroll_offset += 1
                
                # Check file/folder items
                if hasattr(self, 'item_rects'):
                    for item_type, item_name, item_path, item_rect in self.item_rects:
                        if item_rect.collidepoint(mouse_pos):
                            try:
                                # Normalize and get absolute path to handle spaces/special chars
                                normalized_path = os.path.normpath(os.path.abspath(item_path))
                                
                                # Skip macOS metadata files
                                if os.path.basename(normalized_path).startswith('._'):
                                    break
                                
                                if item_type == "folder":
                                    # Enter folder - verify it exists and is accessible
                                    if os.path.exists(normalized_path) and os.path.isdir(normalized_path):
                                        self.current_path = normalized_path
                                        self.scroll_offset = 0
                                        self.selected_file = None
                                else:
                                    # Select file - verify it exists and is accessible
                                    if os.path.exists(normalized_path) and os.path.isfile(normalized_path):
                                        # Skip empty files and metadata files
                                        if os.path.getsize(normalized_path) > 0:
                                            self.selected_file = normalized_path
                            except (OSError, ValueError, UnicodeDecodeError, PermissionError) as e:
                                # Skip if path is invalid
                                print(f"Error accessing {item_path}: {e}")
                                pass
                            break
                
                # Check Open button
                if hasattr(self, 'open_button_rect') and self.open_button_rect.collidepoint(mouse_pos):
                    if self.selected_file:
                        try:
                            # Ensure file path is absolute and valid
                            abs_path = os.path.normpath(os.path.abspath(self.selected_file))
                            if os.path.exists(abs_path) and os.path.isfile(abs_path) and os.path.getsize(abs_path) > 0:
                                # Skip metadata files
                                if not os.path.basename(abs_path).startswith('._'):
                                    return ("file_selected", abs_path)
                        except (OSError, ValueError):
                            pass
                
                # Check Cancel button
                if hasattr(self, 'cancel_button_rect') and self.cancel_button_rect.collidepoint(mouse_pos):
                    return "cancel"
        
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll with mouse wheel
            items = self.get_files_and_folders()
            if event.y > 0:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 3)
            else:  # Scroll down
                if self.scroll_offset + self.items_per_page < len(items):
                    self.scroll_offset += 3
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "cancel"
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.selected_file:
                    try:
                        # Ensure file path is absolute and valid
                        abs_path = os.path.normpath(os.path.abspath(self.selected_file))
                        if os.path.exists(abs_path) and os.path.isfile(abs_path) and os.path.getsize(abs_path) > 0:
                            # Skip metadata files
                            if not os.path.basename(abs_path).startswith('._'):
                                return ("file_selected", abs_path)
                    except (OSError, ValueError):
                        pass
        
        return None
    
    def update(self):
        """Update file browser"""
        pass
