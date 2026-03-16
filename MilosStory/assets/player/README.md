# Player Animations

Place your player animation GIFs in this folder:

- **walking.gif** - Animation for when the player is moving left/right
- **standing.gif** - Animation for when the player is idle/standing still
- **falling.gif** - Animation for when the player is falling/jumping

The game will automatically detect which animation to use based on the player's movement state.

## Notes:
- GIFs will be automatically loaded and animated
- If a GIF is missing, a simple fallback sprite will be used
- Animations will flip horizontally based on the direction the player is facing
