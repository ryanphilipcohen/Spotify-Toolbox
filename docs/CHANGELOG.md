# Changelog

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