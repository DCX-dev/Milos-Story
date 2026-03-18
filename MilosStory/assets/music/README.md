# Music Files

Place your music files in this folder with the following naming convention:

- **theme.mp3** (or .wav, .ogg, etc.) - Theme music for title screen and save file selection (by backgroundmusicforvideos)
- **level1.mp3** (or .wav, .ogg, etc.) - Music for Level 1
- **level2.mp3** - Music for Level 2
- **level3.mp3** - Music for Level 3
- ... and so on

## Supported Formats

The game supports common audio formats:
- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)
- M4A (.m4a)
- FLAC (.flac)

## How It Works

- **Theme**: A file named `theme` (e.g., theme.mp3) plays on the title screen and save file selection. Loops continuously. Credited to Maksym Malko (same as Levels 4-10).
- **Levels**: Music files should be named exactly `level{number}` followed by the file extension
- For example: `level1.mp3`, `level2.wav`, `level3.ogg`
- The game will automatically find and play the appropriate music for each level
- Music will loop continuously while playing a level
- Music stops when you die, complete the game, or return to the title screen

## Notes

- If no music file is found for a level, the game will continue without music
- Only one music file per level (the first matching file found will be used)
- Music files are not required - the game works fine without them
