from .game_platform import Platform
from .enemy import Enemy
from .chest import Chest

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
    """Create platforms, enemies, lava, and chests for a specific level"""
    platforms = []
    enemies = []
    lava_zones = []
    chests = []
    
    if level_num == 1:
        # Level 1: Simple horizontal platforms - tutorial level (extended)
        platforms = [
            Platform(0, screen_height - 40, 250, 40, BROWN),
            Platform(400, screen_height - 40, 250, 40, BROWN),
            Platform(800, screen_height - 40, 250, 40, BROWN),
            Platform(1200, screen_height - 40, 250, 40, BROWN),
            Platform(1600, screen_height - 40, 250, 40, BROWN),
            Platform(2000, screen_height - 40, 250, 40, BROWN),
            Platform(2400, screen_height - 40, 250, 40, BROWN),
            Platform(2800, screen_height - 40, 250, 40, BROWN),
            Platform(3200, screen_height - 40, 250, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1450, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1850, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 2250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 2650, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 3050, "y": screen_height - 30, "width": 150, "height": 30},
        ]
        enemies = [
            Enemy(450, screen_height - 40, gravity=0.7, speed=1.5),
            Enemy(1250, screen_height - 40, gravity=0.7, speed=1.5),
            Enemy(2050, screen_height - 40, gravity=0.7, speed=1.5),
            Enemy(2850, screen_height - 40, gravity=0.7, speed=1.5),
        ]
        chests = [
            Chest(550, screen_height - 80, "arrows"),
            Chest(1350, screen_height - 80, "arrows"),
            Chest(2150, screen_height - 80, "arrows"),
        ]
        world_width = 3450
    
    elif level_num == 2:
        # Level 2: EXPLORATION - Two paths: high route (upper platforms) or low route (ground). Both reach the end.
        # Central hub with branching paths - explore left/right/up
        platforms = [
            # Start area - ground
            Platform(0, screen_height - 40, 300, 40, BROWN),
            # Low path (ground level) - can go straight across
            Platform(500, screen_height - 40, 200, 40, BROWN),
            Platform(900, screen_height - 40, 200, 40, BROWN),
            Platform(1300, screen_height - 40, 200, 40, BROWN),
            Platform(1700, screen_height - 40, 200, 40, BROWN),
            # High path - upper route (alternative)
            Platform(350, screen_height - 200, 180, 20, GREEN),
            Platform(550, screen_height - 320, 180, 20, GREEN),
            Platform(750, screen_height - 200, 180, 20, GREEN),
            Platform(950, screen_height - 320, 180, 20, GREEN),
            Platform(1150, screen_height - 200, 180, 20, GREEN),
            Platform(1350, screen_height - 320, 180, 20, GREEN),
            Platform(1550, screen_height - 200, 180, 20, GREEN),
            Platform(1750, screen_height - 320, 180, 20, GREEN),
            Platform(1950, screen_height - 200, 180, 20, GREEN),
            # Connector platforms - switch between high and low
            Platform(700, screen_height - 120, 100, 20, GREEN),
            Platform(1100, screen_height - 120, 100, 20, GREEN),
            Platform(1500, screen_height - 120, 100, 20, GREEN),
            # End area - both paths converge
            Platform(2150, screen_height - 40, 250, 40, BROWN),
            Platform(2500, screen_height - 150, 150, 20, GREEN),
            Platform(2700, screen_height - 40, 200, 40, BROWN),
            Platform(3000, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 300, "y": screen_height - 30, "width": 200, "height": 30},
            {"x": 700, "y": screen_height - 30, "width": 200, "height": 30},
            {"x": 1100, "y": screen_height - 30, "width": 200, "height": 30},
            {"x": 1500, "y": screen_height - 30, "width": 200, "height": 30},
            {"x": 1900, "y": screen_height - 30, "width": 250, "height": 30},
            {"x": 2400, "y": screen_height - 30, "width": 100, "height": 30},
        ]
        enemies = [
            Enemy(600, screen_height - 40, gravity=0.7, speed=2.0),
            Enemy(450, screen_height - 200, gravity=0.7, speed=2.0),
            Enemy(1000, screen_height - 320, gravity=0.7, speed=2.0),
            Enemy(1400, screen_height - 200, gravity=0.7, speed=2.0),
            Enemy(2300, screen_height - 40, gravity=0.7, speed=2.0),
        ]
        chests = [
            Chest(400, screen_height - 90, "arrows"),
            Chest(1200, screen_height - 340, "arrows"),
            Chest(2200, screen_height - 90, "damage"),
        ]
        world_width = 3200
    
    elif level_num == 3:
        # Level 3: EXPLORATION - Vertical chambers. Go up into rooms, explore, multiple routes down.
        # Canyon with upper and lower chambers - explore the heights
        platforms = [
            # Ground floor
            Platform(0, screen_height - 40, 250, 40, BROWN),
            Platform(400, screen_height - 40, 150, 40, BROWN),
            Platform(800, screen_height - 40, 150, 40, BROWN),
            Platform(1200, screen_height - 40, 150, 40, BROWN),
            Platform(1600, screen_height - 40, 250, 40, BROWN),
            # Left chamber - climb up and explore
            Platform(250, screen_height - 180, 120, 20, BLUE),
            Platform(350, screen_height - 300, 120, 20, BLUE),
            Platform(250, screen_height - 420, 150, 20, BLUE),
            Platform(400, screen_height - 300, 100, 20, BLUE),
            # Center upper area - bridge between sides
            Platform(550, screen_height - 250, 200, 20, BLUE),
            Platform(600, screen_height - 400, 120, 20, BLUE),
            Platform(750, screen_height - 250, 150, 20, BLUE),
            # Right chamber - mirror exploration
            Platform(1050, screen_height - 180, 120, 20, BLUE),
            Platform(950, screen_height - 300, 120, 20, BLUE),
            Platform(1050, screen_height - 420, 150, 20, BLUE),
            Platform(900, screen_height - 300, 100, 20, BLUE),
            # Connectors - stairs between levels
            Platform(450, screen_height - 120, 80, 20, BLUE),
            Platform(650, screen_height - 120, 80, 20, BLUE),
            Platform(1050, screen_height - 120, 80, 20, BLUE),
            # End section
            Platform(1900, screen_height - 40, 200, 40, BROWN),
            Platform(2200, screen_height - 150, 150, 20, BLUE),
            Platform(2400, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 550, "y": screen_height - 30, "width": 250, "height": 30},
            {"x": 950, "y": screen_height - 30, "width": 250, "height": 30},
            {"x": 1350, "y": screen_height - 30, "width": 250, "height": 30},
            {"x": 1850, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(300, screen_height - 300, gravity=0.7, speed=1.8),
            Enemy(650, screen_height - 400, gravity=0.7, speed=1.8),
            Enemy(1000, screen_height - 420, gravity=0.7, speed=1.8),
            Enemy(700, screen_height - 250, gravity=0.7, speed=1.8),
            Enemy(2100, screen_height - 40, gravity=0.7, speed=1.8),
        ]
        chests = [
            Chest(320, screen_height - 450, "arrows"),
            Chest(700, screen_height - 450, "arrows"),
            Chest(1100, screen_height - 480, "damage"),
        ]
        world_width = 2600
    
    elif level_num == 4:
        # Level 4: EXPLORATION - Twin towers with crossover. Climb left tower OR right tower, jump across at top.
        # Or take the middle path - multiple ways to reach the end
        platforms = [
            # Start
            Platform(0, screen_height - 40, 250, 40, BROWN),
            # Left tower - climb this side
            Platform(200, screen_height - 150, 120, 20, PURPLE),
            Platform(250, screen_height - 280, 120, 20, PURPLE),
            Platform(200, screen_height - 410, 150, 20, PURPLE),
            Platform(350, screen_height - 280, 100, 20, PURPLE),
            # Right tower - or climb this side
            Platform(450, screen_height - 150, 120, 20, PURPLE),
            Platform(400, screen_height - 280, 120, 20, PURPLE),
            Platform(450, screen_height - 410, 150, 20, PURPLE),
            Platform(300, screen_height - 280, 100, 20, PURPLE),
            # Bridge between towers at top
            Platform(200, screen_height - 530, 350, 20, PURPLE),
            # Middle path - ground route (harder, more lava)
            Platform(650, screen_height - 40, 150, 40, BROWN),
            Platform(900, screen_height - 120, 100, 20, PURPLE),
            Platform(1050, screen_height - 40, 150, 40, BROWN),
            # Right side - descend from bridge or climb up
            Platform(600, screen_height - 250, 120, 20, PURPLE),
            Platform(750, screen_height - 380, 120, 20, PURPLE),
            Platform(900, screen_height - 250, 120, 20, PURPLE),
            Platform(1050, screen_height - 380, 120, 20, PURPLE),
            # End section
            Platform(1250, screen_height - 40, 200, 40, BROWN),
            Platform(1550, screen_height - 150, 150, 20, PURPLE),
            Platform(1800, screen_height - 40, 250, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 400, "height": 30},
            {"x": 800, "y": screen_height - 30, "width": 250, "height": 30},
            {"x": 1200, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(280, screen_height - 410, gravity=0.7, speed=2.2),
            Enemy(500, screen_height - 410, gravity=0.7, speed=2.2),
            Enemy(350, screen_height - 530, gravity=0.7, speed=2.2),
            Enemy(800, screen_height - 250, gravity=0.7, speed=2.2),
            Enemy(1650, screen_height - 40, gravity=0.7, speed=2.2),
        ]
        chests = [
            Chest(250, screen_height - 470, "arrows"),
            Chest(450, screen_height - 470, "arrows"),
            Chest(650, screen_height - 300, "damage"),
        ]
        world_width = 2050
    
    elif level_num == 5:
        # Level 5: EXPLORATION - Open arena with 3 distinct routes. North (high), South (low), or zigzag middle.
        # Large explorable area - find your preferred path
        platforms = [
            # Start
            Platform(0, screen_height - 40, 250, 40, BROWN),
            # South route (ground) - safe but longer
            Platform(400, screen_height - 40, 180, 40, BROWN),
            Platform(750, screen_height - 40, 180, 40, BROWN),
            Platform(1100, screen_height - 40, 180, 40, BROWN),
            Platform(1450, screen_height - 40, 180, 40, BROWN),
            # North route (high) - risky but fast
            Platform(350, screen_height - 250, 200, 20, ORANGE),
            Platform(550, screen_height - 400, 200, 20, ORANGE),
            Platform(750, screen_height - 250, 200, 20, ORANGE),
            Platform(950, screen_height - 400, 200, 20, ORANGE),
            Platform(1150, screen_height - 250, 200, 20, ORANGE),
            Platform(1350, screen_height - 400, 200, 20, ORANGE),
            Platform(1550, screen_height - 250, 200, 20, ORANGE),
            # Middle zigzag - connectors
            Platform(500, screen_height - 150, 100, 20, ORANGE),
            Platform(700, screen_height - 150, 100, 20, ORANGE),
            Platform(900, screen_height - 150, 100, 20, ORANGE),
            Platform(1100, screen_height - 150, 100, 20, ORANGE),
            Platform(1300, screen_height - 150, 100, 20, ORANGE),
            # End
            Platform(1700, screen_height - 40, 250, 40, BROWN),
            Platform(2000, screen_height - 180, 150, 20, ORANGE),
            Platform(2200, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 580, "y": screen_height - 30, "width": 170, "height": 30},
            {"x": 930, "y": screen_height - 30, "width": 170, "height": 30},
            {"x": 1280, "y": screen_height - 30, "width": 170, "height": 30},
            {"x": 1630, "y": screen_height - 30, "width": 70, "height": 30},
        ]
        enemies = [
            Enemy(450, screen_height - 250, gravity=0.7, speed=2.0),
            Enemy(850, screen_height - 400, gravity=0.7, speed=2.0),
            Enemy(1200, screen_height - 250, gravity=0.7, speed=2.0),
            Enemy(600, screen_height - 40, gravity=0.7, speed=2.0),
            Enemy(2100, screen_height - 40, gravity=0.7, speed=2.0),
        ]
        chests = [
            Chest(400, screen_height - 460, "arrows"),
            Chest(1200, screen_height - 460, "arrows"),
            Chest(1700, screen_height - 90, "damage"),
        ]
        world_width = 2400
    
    elif level_num == 6:
        # Level 6: EXPLORATION - Ruins with upper balcony and lower passages. Loop around or go straight.
        # Ancient ruins - explore the upper walkway or the lower tunnels
        platforms = [
            # Start
            Platform(0, screen_height - 40, 220, 40, BROWN),
            # Lower passage - go through the "tunnels"
            Platform(350, screen_height - 40, 100, 40, BROWN),
            Platform(550, screen_height - 40, 100, 40, BROWN),
            Platform(750, screen_height - 40, 100, 40, BROWN),
            Platform(950, screen_height - 40, 100, 40, BROWN),
            Platform(1150, screen_height - 40, 100, 40, BROWN),
            Platform(1350, screen_height - 40, 100, 40, BROWN),
            # Upper balcony - explore above, overlook the level
            Platform(300, screen_height - 220, 250, 20, RED),
            Platform(400, screen_height - 360, 150, 20, RED),
            Platform(600, screen_height - 220, 200, 20, RED),
            Platform(800, screen_height - 360, 150, 20, RED),
            Platform(1000, screen_height - 220, 200, 20, RED),
            Platform(1200, screen_height - 360, 150, 20, RED),
            Platform(1400, screen_height - 220, 200, 20, RED),
            # Connectors - pillars to climb up/down
            Platform(450, screen_height - 120, 80, 20, RED),
            Platform(850, screen_height - 120, 80, 20, RED),
            Platform(1250, screen_height - 120, 80, 20, RED),
            # End
            Platform(1550, screen_height - 40, 220, 40, BROWN),
            Platform(1820, screen_height - 150, 120, 20, RED),
            Platform(2050, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 220, "y": screen_height - 30, "width": 130, "height": 30},
            {"x": 450, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 650, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 850, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1050, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1250, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1450, "y": screen_height - 30, "width": 100, "height": 30},
            {"x": 1770, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(350, screen_height - 360, gravity=0.7, speed=2.5),
            Enemy(700, screen_height - 220, gravity=0.7, speed=2.5),
            Enemy(1100, screen_height - 360, gravity=0.7, speed=2.5),
            Enemy(600, screen_height - 40, gravity=0.7, speed=2.5),
            Enemy(1950, screen_height - 40, gravity=0.7, speed=2.5),
        ]
        chests = [
            Chest(350, screen_height - 280, "arrows"),
            Chest(1200, screen_height - 380, "arrows"),
            Chest(1500, screen_height - 280, "damage"),
        ]
        world_width = 2250
    
    elif level_num == 7:
        # Level 7: EXPLORATION - Spiral tower. Climb up one side, cross at top, descend other side. Or find shortcuts.
        # Clockwise or counter-clockwise - your choice
        platforms = [
            # Start
            Platform(0, screen_height - 40, 220, 40, BROWN),
            # Left spiral - climb up
            Platform(200, screen_height - 150, 120, 20, GRAY),
            Platform(250, screen_height - 290, 120, 20, GRAY),
            Platform(200, screen_height - 430, 120, 20, GRAY),
            Platform(350, screen_height - 290, 100, 20, GRAY),
            # Right spiral - or climb this side
            Platform(500, screen_height - 150, 120, 20, GRAY),
            Platform(450, screen_height - 290, 120, 20, GRAY),
            Platform(500, screen_height - 430, 120, 20, GRAY),
            Platform(350, screen_height - 290, 100, 20, GRAY),
            # Top platform - cross over
            Platform(200, screen_height - 570, 400, 20, GRAY),
            # Center connectors - shortcuts
            Platform(350, screen_height - 120, 80, 20, GRAY),
            Platform(350, screen_height - 450, 80, 20, GRAY),
            # Descend - either side
            Platform(650, screen_height - 430, 120, 20, GRAY),
            Platform(700, screen_height - 290, 120, 20, GRAY),
            Platform(650, screen_height - 150, 120, 20, GRAY),
            # End
            Platform(850, screen_height - 40, 220, 40, BROWN),
            Platform(1100, screen_height - 180, 150, 20, GRAY),
            Platform(1300, screen_height - 40, 200, 40, BROWN),
        ]
        lava_zones = [
            {"x": 220, "y": screen_height - 30, "width": 630, "height": 30},
            {"x": 1070, "y": screen_height - 30, "width": 230, "height": 30},
        ]
        enemies = [
            Enemy(280, screen_height - 430, gravity=0.7, speed=2.2),
            Enemy(550, screen_height - 430, gravity=0.7, speed=2.2),
            Enemy(400, screen_height - 570, gravity=0.7, speed=2.2),
            Enemy(700, screen_height - 290, gravity=0.7, speed=2.2),
            Enemy(1200, screen_height - 40, gravity=0.7, speed=2.2),
        ]
        chests = [
            Chest(250, screen_height - 630, "arrows"),
            Chest(500, screen_height - 630, "arrows"),
            Chest(500, screen_height - 150, "damage"),
        ]
        world_width = 1500
    
    elif level_num == 8:
        # Level 8: EXPLORATION - Maze with 4 quadrants. Multiple routes - explore to find the exit.
        # Each quadrant has different paths - discover which way works for you
        platforms = [
            # Start (quadrant 1)
            Platform(0, screen_height - 40, 220, 40, BROWN),
            # Q1 - upper path
            Platform(250, screen_height - 180, 150, 20, ORANGE),
            Platform(350, screen_height - 320, 120, 20, ORANGE),
            # Q1 - lower path
            Platform(400, screen_height - 40, 120, 40, BROWN),
            Platform(600, screen_height - 120, 100, 20, ORANGE),
            # Bridge to Q2
            Platform(750, screen_height - 40, 150, 40, BROWN),
            # Q2 - explore up or around
            Platform(850, screen_height - 200, 120, 20, ORANGE),
            Platform(950, screen_height - 340, 120, 20, ORANGE),
            Platform(1100, screen_height - 200, 120, 20, ORANGE),
            Platform(750, screen_height - 200, 100, 20, ORANGE),
            # Q3 - crossover
            Platform(1250, screen_height - 40, 120, 40, BROWN),
            Platform(1350, screen_height - 180, 150, 20, ORANGE),
            Platform(1250, screen_height - 320, 120, 20, ORANGE),
            Platform(1450, screen_height - 180, 100, 20, ORANGE),
            # Q4 - final approach
            Platform(1600, screen_height - 40, 150, 40, BROWN),
            Platform(1800, screen_height - 200, 150, 20, ORANGE),
            Platform(2000, screen_height - 40, 220, 40, BROWN),
        ]
        lava_zones = [
            {"x": 220, "y": screen_height - 30, "width": 180, "height": 30},
            {"x": 520, "y": screen_height - 30, "width": 230, "height": 30},
            {"x": 900, "y": screen_height - 30, "width": 350, "height": 30},
            {"x": 1370, "y": screen_height - 30, "width": 230, "height": 30},
            {"x": 1750, "y": screen_height - 30, "width": 50, "height": 30},
        ]
        enemies = [
            Enemy(400, screen_height - 320, gravity=0.7, speed=2.8),
            Enemy(1000, screen_height - 340, gravity=0.7, speed=2.8),
            Enemy(1320, screen_height - 320, gravity=0.7, speed=2.8),
            Enemy(650, screen_height - 40, gravity=0.7, speed=2.8),
            Enemy(1900, screen_height - 40, gravity=0.7, speed=2.8),
        ]
        chests = [
            Chest(320, screen_height - 380, "arrows"),
            Chest(1100, screen_height - 380, "arrows"),
            Chest(1500, screen_height - 240, "damage"),
        ]
        world_width = 2220
    
    elif level_num == 9:
        # Level 9: EXPLORATION - Final arena. Large open space with islands - go any direction to find the exit.
        # Boss gate approach - explore the arena, multiple routes to the gate
        platforms = [
            # Start
            Platform(0, screen_height - 40, 250, 40, BROWN),
            # Central island - hub to explore from
            Platform(400, screen_height - 200, 200, 20, PURPLE),
            Platform(400, screen_height - 350, 180, 20, PURPLE),
            # North route - high path
            Platform(300, screen_height - 500, 150, 20, PURPLE),
            Platform(500, screen_height - 500, 150, 20, PURPLE),
            Platform(650, screen_height - 350, 120, 20, PURPLE),
            # South route - low path
            Platform(650, screen_height - 40, 150, 40, BROWN),
            Platform(900, screen_height - 120, 120, 20, PURPLE),
            Platform(1100, screen_height - 40, 150, 40, BROWN),
            # East route - middle
            Platform(700, screen_height - 200, 150, 20, PURPLE),
            Platform(950, screen_height - 280, 150, 20, PURPLE),
            Platform(1200, screen_height - 200, 150, 20, PURPLE),
            # West loop - optional exploration
            Platform(200, screen_height - 350, 120, 20, PURPLE),
            Platform(150, screen_height - 200, 100, 20, PURPLE),
            # All paths lead to end
            Platform(1400, screen_height - 40, 200, 40, BROWN),
            Platform(1550, screen_height - 180, 150, 20, PURPLE),
            Platform(1750, screen_height - 40, 250, 40, BROWN),
        ]
        lava_zones = [
            {"x": 250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 600, "y": screen_height - 30, "width": 50, "height": 30},
            {"x": 800, "y": screen_height - 30, "width": 300, "height": 30},
            {"x": 1250, "y": screen_height - 30, "width": 150, "height": 30},
            {"x": 1650, "y": screen_height - 30, "width": 100, "height": 30},
        ]
        enemies = [
            Enemy(450, screen_height - 350, gravity=0.7, speed=3.0),
            Enemy(350, screen_height - 500, gravity=0.7, speed=3.0),
            Enemy(1000, screen_height - 280, gravity=0.7, speed=3.0),
            Enemy(700, screen_height - 40, gravity=0.7, speed=3.0),
            Enemy(1650, screen_height - 40, gravity=0.7, speed=3.0),
        ]
        chests = [
            Chest(450, screen_height - 410, "arrows"),
            Chest(250, screen_height - 560, "arrows"),
            Chest(1200, screen_height - 340, "damage"),
        ]
        world_width = 2000
    
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
        chests = []
        world_width = screen_width
    
    else:
        # Default level
        platforms = [
            Platform(0, screen_height - 40, screen_width, 40, BROWN),
        ]
        enemies = []
        lava_zones = []
        chests = []
        world_width = screen_width
    
    return platforms, enemies, lava_zones, world_width, chests
