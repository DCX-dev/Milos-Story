import json
import os
from datetime import datetime

from .paths import get_data_path

class SaveSystem:
    def __init__(self):
        try:
            data_path = get_data_path()
            self.save_folder = os.path.normpath(os.path.join(data_path, "save_data"))
            os.makedirs(self.save_folder, exist_ok=True)
        except Exception:
            data_path = os.path.join(os.path.expanduser("~"), "MilosStory_saves")
            self.save_folder = os.path.normpath(os.path.join(data_path, "save_data"))
            os.makedirs(self.save_folder, exist_ok=True)
        self.max_slots = 3
    
    def get_save_path(self, slot):
        """Get the file path for a save slot"""
        return os.path.normpath(os.path.join(self.save_folder, f"save_{slot}.json"))
    
    def get_save_file_path(self, slot):
        """Get the full path to save file (alias for get_save_path)"""
        return self.get_save_path(slot)
    
    def save_game(self, slot, level, player_x, player_y, arrow_count=20, player_damage=1):
        """Save game data to a slot"""
        save_data = {
            "level": level,
            "player_x": player_x,
            "player_y": player_y,
            "arrow_count": arrow_count,
            "player_damage": player_damage,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            save_path = self.get_save_path(slot)
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot):
        """Load game data from a slot"""
        try:
            save_path = self.get_save_path(slot)
            
            # Skip macOS metadata files
            filename = os.path.basename(save_path)
            if filename.startswith('._') or filename.startswith('.'):
                return None
            
            if not os.path.exists(save_path):
                return None
            
            # Skip if it's a directory
            if not os.path.isfile(save_path):
                return None
            
            # Validate file is readable and not empty
            if os.path.getsize(save_path) == 0:
                return None
            
            # Try to read and parse JSON
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate required fields exist
                if not isinstance(data, dict):
                    return None
                if 'level' not in data or 'player_x' not in data or 'player_y' not in data:
                    return None
                return data
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in save file {slot}: {e}")
            return None
        except (IOError, OSError, PermissionError) as e:
            print(f"Error accessing save file {slot}: {e}")
            return None
        except Exception as e:
            print(f"Error loading game {slot}: {e}")
            return None
    
    def get_save_info(self, slot):
        """Get save file info without loading full data"""
        try:
            save_path = self.get_save_path(slot)
            filename = os.path.basename(save_path)
            
            # Skip macOS metadata files and hidden files
            if filename.startswith('._') or filename.startswith('.'):
                return {"exists": False, "level": 1, "timestamp": ""}
            
            # Check if file exists and is valid
            if not os.path.exists(save_path) or not os.path.isfile(save_path):
                return {"exists": False, "level": 1, "timestamp": ""}
            
            # Try to load save data
            save_data = self.load_game(slot)
            if save_data:
                return {
                    "exists": True,
                    "level": save_data.get("level", 1),
                    "timestamp": save_data.get("timestamp", "")
                }
        except Exception as e:
            print(f"Error getting save info for slot {slot}: {e}")
        
        return {"exists": False, "level": 1, "timestamp": ""}
    
    def delete_save(self, slot):
        """Delete a save file"""
        try:
            save_path = self.get_save_path(slot)
            
            # Skip macOS metadata files
            if os.path.basename(save_path).startswith('._'):
                return False
            
            if os.path.exists(save_path) and os.path.isfile(save_path):
                os.remove(save_path)
                return True
        except Exception as e:
            print(f"Error deleting save: {e}")
        return False
