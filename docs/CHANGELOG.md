# Changelog

## [1.0.1] - 2025-02-10
### Added
- **Loading/Saving:** All tracks, tags, templates, and playlists now load on startup, and prompt you to save before quitting the program when changes are made.
- Added **'backup'** and **'backup [location]'** commands to save all tags, templates, and playlists quickly to a specific location
- Generating tags based on attributes of your loaded tracks:
    - Track duration: **'generate tags duration'**
    - Track artist: **'generate tags artist'**
- Added **'help'** function, displaying all commands and uses
- Added **'remove tags'** function, to quickly delete all tags loaded
- Added **'clear tag [tag]'** function, removing all tracks from a tag

### Documentation
- Formatted and linted code
- Wrote docstrings for all functions
- Moved dev scripts outside of the repo

### Fixes
- Fixed issue where names with uppercase letters wouldn't delete or load properly
- Removed duplicate function 'create_json'

## [1.0] - 2025-01-15

### Added
- Built core features including:
    - Downloading liked tracks from the user's Spotify account
    - Viewing and managing tracks
    - Adding/removing tags and templates
    - Generating playlists from templates
    - Uploading playlists to Spotify to the user's Spotify account
- Developed error handling for JSON files to prevent crashes when files are missing or improperly formatted.

### Testing
- Ensured commands work as expected, including when JSONs aren't loaded.
- Wrote input validation to ensure smooth handling of invalid input and edge cases.

### Documentation
- Wrote a comprehensive `README.md` with extra scripts such as `create_env_file.py` to help the user set up their environment to run the program
- Created `requirements.txt` file for project dependencies.
- Wrote `overview.md` to provide detailed information about the capabilities and possible use cases of the project.