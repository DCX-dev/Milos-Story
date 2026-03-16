from .game_platform import Platform
from .enemy import Enemy

# Colors
BROWN = (139, 69, 19)
GREEN = (100, 200, 100)
BLUE = (100, 150, 255)
GRAY = (128, 128, 128)
RED = (255, 100, 100)
PURPLE = (150, 100, 200)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
DARK_RED = (150, 0, 0)

def get_level_background(level_num):
    """Get background color for a specific level"""
    backgrounds = {
        1: (135, 206, 235),  # Sky blue - tutorial
        2: (100, 150, 200),  # Ocean blue
        3: (200, 220, 255),  # Light purple-blue
        4: (180, 150, 200),  # Purple
        5: (255, 200, 150),  # Sunset orange
        6: (255, 150, 150),  # Red/pink
        7: (150, 150, 180),  # Gray-blue
        8: (255, 220, 180),  # Peach
        9: (200, 180, 255),  # Lavender
        10: (50, 50, 80),    # Dark purple - boss arena
    }
    return backgrounds.get(level_num, (135, 206, 235))

def create_level(level_num, screen_height, screen_width):
    """Create platforms, enemies, and lava for a specific level"""
    platforms = []
    enemies = []
    lava_zones = []
    
    if level_num == 1:
        # Level 1: Simple horizontal platforms - tutorial level
        platforms = [
            Platform(0, screen_height - 40, 250, 40, BROWN),
            Platform(400, screen_height - 40, 250, 40, BROWN),
            Platform(800, screen_height - 40, 250, 40, BROWN),
            Platform(1200, screen_height - 40, 250, 40, BROWN),
            Platform(1600, screen_height - 40, 250, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1450, "y": screen_height - 30, "width": 150, "height": 30},
        ]
        enemies = [
            Enemy(450, screen_height - 40, gravity=0.7, speed=1.5),
            Enemy(1250, screen_height - 40, gravity=0.7, speed=1.5),
        ]
        world_width = 1850
    
    elif level_num == 2:
        # Level 2: Stepping stone pattern - varying heights
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(300, screen_height - 120, 150, 20, GREEN),
            Platform(500, screen_height - 200, 150, 20, GREEN),
            Platform(700, screen_height - 280, 150, 20, GREEN),
            Platform(900, screen_height - 200, 150, 20, GREEN),
            Platform(1100, screen_height - 120, 150, 20, GREEN),
            Platform(1300, screen_height - 40, 200, 40, BROWN),
            Platform(1600, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 850, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1250, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1500, "y": screen_height - 30, "width": 100, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 120, gravity=0.7, speed=2.0),
            Enemy(750, screen_height - 280, gravity=0.7, speed=2.0),
            Enemy(1150, screen_height - 120, gravity=0.7, speed=2.0),
        ]
        world_width = 1800
    
    elif level_num == 3:
        # Level 3: Zigzag pattern - alternating high and low platforms
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(300, screen_height - 180, 180, 20, BLUE),
            Platform(550, screen_height - 40, 180, 40, BROWN),
            Platform(800, screen_height - 220, 180, 20, BLUE),
            Platform(1050, screen_height - 40, 180, 40, BROWN),
            Platform(1300, screen_height - 200, 180, 20, BLUE),
            Platform(1550, screen_height - 40, 180, 40, BROWN),
            Platform(1800, screen_height - 240, 180, 20, BLUE),
            Platform(2050, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 480, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 730, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 980, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1230, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1480, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1730, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1980, "y": screen_height - 30, "width": 70, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 180, gravity=0.7, speed=1.8),
            Enemy(850, screen_height - 220, gravity=0.7, speed=1.8),
            Enemy(1350, screen_height - 200, gravity=0.7, speed=1.8),
            Enemy(1850, screen_height - 240, gravity=0.7, speed=1.8),
        ]
        world_width = 2250
    
    elif level_num == 4:
        # Level 4: Vertical tower challenge - platforms going up
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(300, screen_height - 150, 150, 20, PURPLE),
            Platform(500, screen_height - 250, 150, 20, PURPLE),
            Platform(700, screen_height - 350, 150, 20, PURPLE),
            Platform(900, screen_height - 450, 150, 20, PURPLE),
            Platform(1100, screen_height - 350, 150, 20, PURPLE),
            Platform(1300, screen_height - 250, 150, 20, PURPLE),
            Platform(1500, screen_height - 150, 150, 20, PURPLE),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 850, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1250, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1650, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 150, gravity=0.7, speed=2.2),
            Enemy(750, screen_height - 350, gravity=0.7, speed=2.2),
            Enemy(1150, screen_height - 350, gravity=0.7, speed=2.2),
            Enemy(1550, screen_height - 150, gravity=0.7, speed=2.2),
        ]
        world_width = 1900
    
    elif level_num == 5:
        # Level 5: Wide gaps with floating platforms
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(400, screen_height - 180, 120, 20, ORANGE),
            Platform(600, screen_height - 40, 200, 40, BROWN),
            Platform(900, screen_height - 220, 120, 20, ORANGE),
            Platform(1200, screen_height - 40, 200, 40, BROWN),
            Platform(1500, screen_height - 200, 120, 20, ORANGE),
            Platform(1800, screen_height - 40, 200, 40, BROWN),
            Platform(2100, screen_height - 240, 120, 20, ORANGE),
            Platform(2400, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 200, "height": 30},
            {"x": 520, "y": screen_height - 30, "width": 80, "height": 30},
            {"x": 800, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1020, "y": screen_height - 30, "width": 80, "height": 30},
            {"x": 1400, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1620, "y": screen_height - 30, "width": 80, "height": 30},
            {"x": 2000, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 2220, "y": screen_height - 30, "width": 80, "height": 30},
        ]
        enemies = [
            Enemy(450, screen_height - 180, gravity=0.7, speed=2.0),
            Enemy(950, screen_height - 220, gravity=0.7, speed=2.0),
            Enemy(1550, screen_height - 200, gravity=0.7, speed=2.0),
            Enemy(2150, screen_height - 240, gravity=0.7, speed=2.0),
        ]
        world_width = 2600
    
    elif level_num == 6:
        # Level 6: Narrow platforms challenge
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(350, screen_height - 40, 80, 40, BROWN),
            Platform(500, screen_height - 180, 80, 20, RED),
            Platform(650, screen_height - 40, 80, 40, BROWN),
            Platform(800, screen_height - 220, 80, 20, RED),
            Platform(950, screen_height - 40, 80, 40, BROWN),
            Platform(1100, screen_height - 200, 80, 20, RED),
            Platform(1250, screen_height - 40, 80, 40, BROWN),
            Platform(1400, screen_height - 240, 80, 20, RED),
            Platform(1550, screen_height - 40, 80, 40, BROWN),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 430, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 580, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 730, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 880, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1030, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1180, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1330, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1480, "y": screen_height - 30, "width": 70, "height": 30},
            {"x": 1630, "y": screen_height - 30, "width": 70, "height": 30},
        ]
        enemies = [
            Enemy(380, screen_height - 40, gravity=0.7, speed=2.5),
            Enemy(680, screen_height - 40, gravity=0.7, speed=2.5),
            Enemy(980, screen_height - 40, gravity=0.7, speed=2.5),
            Enemy(1280, screen_height - 40, gravity=0.7, speed=2.5),
            Enemy(1580, screen_height - 40, gravity=0.7, speed=2.5),
        ]
        world_width = 1900
    
    elif level_num == 7:
        # Level 7: Spiral staircase pattern
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(300, screen_height - 120, 150, 20, GRAY),
            Platform(500, screen_height - 200, 150, 20, GRAY),
            Platform(700, screen_height - 280, 150, 20, GRAY),
            Platform(900, screen_height - 360, 150, 20, GRAY),
            Platform(1100, screen_height - 280, 150, 20, GRAY),
            Platform(1300, screen_height - 200, 150, 20, GRAY),
            Platform(1500, screen_height - 120, 150, 20, GRAY),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 850, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1250, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1650, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 120, gravity=0.7, speed=2.2),
            Enemy(750, screen_height - 280, gravity=0.7, speed=2.2),
            Enemy(1150, screen_height - 280, gravity=0.7, speed=2.2),
            Enemy(1550, screen_height - 120, gravity=0.7, speed=2.2),
        ]
        world_width = 1900
    
    elif level_num == 8:
        # Level 8: Maze-like with multiple paths
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(300, screen_height - 40, 150, 40, BROWN),
            Platform(500, screen_height - 180, 100, 20, ORANGE),
            Platform(650, screen_height - 40, 150, 40, BROWN),
            Platform(850, screen_height - 220, 100, 20, ORANGE),
            Platform(1000, screen_height - 40, 150, 40, BROWN),
            Platform(1200, screen_height - 200, 100, 20, ORANGE),
            Platform(1350, screen_height - 40, 150, 40, BROWN),
            Platform(1550, screen_height - 180, 100, 20, ORANGE),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 600, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 800, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 950, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1150, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1300, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1500, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1650, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 40, gravity=0.7, speed=2.8),
            Enemy(700, screen_height - 40, gravity=0.7, speed=2.8),
            Enemy(1050, screen_height - 40, gravity=0.7, speed=2.8),
            Enemy(1400, screen_height - 40, gravity=0.7, speed=2.8),
        ]
        world_width = 1900
    
    elif level_num == 9:
        # Level 9: Final challenge - extreme platforming
        platforms = [
            Platform(0, screen_height - 40, 200, 40, BROWN),
            Platform(350, screen_height - 150, 100, 20, PURPLE),
            Platform(500, screen_height - 40, 100, 40, BROWN),
            Platform(650, screen_height - 250, 100, 20, PURPLE),
            Platform(800, screen_height - 40, 100, 40, BROWN),
            Platform(950, screen_height - 300, 100, 20, PURPLE),
            Platform(1100, screen_height - 40, 100, 40, BROWN),
            Platform(1250, screen_height - 200, 100, 20, PURPLE),
            Platform(1400, screen_height - 40, 100, 40, BROWN),
            Platform(1550, screen_height - 280, 100, 20, PURPLE),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 200, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 600, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 750, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 900, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1200, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1350, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1500, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 1650, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(400, screen_height - 150, gravity=0.7, speed=3.0),
            Enemy(700, screen_height - 40, gravity=0.7, speed=3.0),
            Enemy(1000, screen_height - 300, gravity=0.7, speed=3.0),
            Enemy(1300, screen_height - 40, gravity=0.7, speed=3.0),
            Enemy(1600, screen_height - 280, gravity=0.7, speed=3.0),
        ]
        world_width = 1900
    
    elif level_num == 10:
        # Level 10: Boss fight arena - no lava, just boss
        platforms = [
            Platform(0, screen_height - 40, screen_width, 40, BROWN),
            Platform(200, screen_height - 200, 150, 20, RED),
            Platform(850, screen_height - 200, 150, 20, RED),
            Platform(500, screen_height - 400, 200, 20, PURPLE),
        ]
        enemies = []
        lava_zones = []
        world_width = screen_width
    
    else:
        # Default level
        platforms = [
            Platform(0, screen_height - 40, screen_width, 40, BROWN),
        ]
        enemies = []
        lava_zones = []
        world_width = screen_width
    
    return platforms, enemies, lava_zones, world_width
