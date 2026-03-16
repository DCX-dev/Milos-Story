#!/usr/bin/env python3
"""
Milo's Story - Game Launcher
Run this file to start the game.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the game
if __name__ == "__main__":
    from src.main import Game
    game = Game()
    game.run()
