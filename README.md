# Milo's Story

A platformer game built with Pygame. Help Milo navigate through challenging levels, defeat enemies with arrows, and reach the end of each level!

## Features

- 🎮 Classic platformer gameplay with smooth controls
- 🎯 Bow and arrow combat system
- 🎨 Animated character sprites (GIF-based)
- 🎵 Level-specific background music
- 💾 Save system with multiple slots (Milo A, B, C)
- 🎨 Dynamic level generation with varied obstacles
- 👾 Enemy AI with patrol and chase behaviors
- 🏆 Boss battles
- 🎬 Credits screen with music attribution

## Screenshots

*Add screenshots of your game here!*

## Project Structure

```
Milo's Story/
├── main.py              # Game launcher (run this to start the game)
├── src/                 # Core game source code
│   ├── main.py         # Main game loop and logic
│   ├── player.py       # Player class and animations
│   ├── enemy.py        # Enemy AI and behavior
│   ├── boss.py         # Boss enemy class
│   ├── arrow.py        # Arrow projectile system
│   ├── game_platform.py # Platform collision system
│   ├── level_system.py  # Level generation and backgrounds
│   └── save_system.py   # Save/load game functionality
├── screens/            # UI screens
│   ├── title_screen.py      # Title and save slot selection
│   ├── victory_screen.py    # Victory screen
│   ├── credits_screen.py    # Credits screen
│   └── level_selector.py    # Level selector (debug mode)
├── assets/             # Game assets
│   ├── player/         # Player animation GIFs
│   ├── music/          # Level music files (level1.mp3, level2.mp3, etc.)
│   └── background/     # Background images for title/save screens
├── data/               # Game data
│   └── save_data/      # Save game files
├── docs/               # Documentation
│   ├── BUILD.md
│   ├── INSTALL_PYTHON_WINE.md
│   ├── MAC_INSTALL_INSTRUCTIONS.md
│   └── README_BUILD.md
├── scripts/            # Build and utility scripts
│   ├── build_mac.sh
│   ├── build_windows.sh
│   └── ...
└── requirements.txt    # Python dependencies
```

## Running the Game

Run the game from the project root:

```bash
python main.py
```

Or directly:

```bash
python src/main.py
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Asset Organization

- **Player animations**: Place GIF files (`standing.gif`, `walking.gif`, `falling.gif`) in `assets/player/`
- **Music**: Place music files named `level1.mp3`, `level2.mp3`, etc. in `assets/music/`
- **Backgrounds**: Place any image file in `assets/background/` to use as title/save screen background

## Controls

- **Arrow Keys / WASD**: Move left/right
- **Space**: Jump
- **Mouse Click**: Shoot arrow (aims toward mouse cursor)
- **ESC**: Pause/Return to title screen

## Credits

### Music Attribution

- **Level 1**: Music by Viacheslav Starostin from Pixabay
- **Level 2**: Music by HitsLab from Pixabay
- **Level 3**: Music by Mykola Sosin from Pixabay
- **Levels 4-10**: Music by Maksym Malko from Pixabay

All music licensed under Pixabay License.

## Development

### Building

See `docs/BUILD.md` for build instructions.

### Debug Mode

Set `DEBUG_MODE = True` in `src/main.py` to enable level selector for testing.

## License

[Add your license here]

## Contributing

[Add contribution guidelines if desired]

---

**Team Banana Labs Studios**
