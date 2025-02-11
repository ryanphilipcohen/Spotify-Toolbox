import math
import json
import time
import os
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

from datatypes import Track, Tag, Template, Playlist


def load_config(config_path: str = "data/config.json") -> dict:
    """Load configuration file from given path and return as dictionary.

    Contains default paths for JSON files and backup location.

    Args:
        config_path (str, optional): The path to the configuration file. Defaults to "data/config.json".

    Raises:
        FileNotFoundError: If the configuration file is not found at the given path.

    Returns:
        dict: The configuration file as a dictionary.
    """
    config_path = Path(config_path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


CONFIG_PATH = Path("data/config.json")
config = load_config(CONFIG_PATH)
DEFAULT_BACKUP_PATH = Path(config["DEFAULT_BACKUP_PATH"])
DEFAULT_JSON_PATH = Path(config["DEFAULT_JSON_PATH"])
DEFAULT_TRACKS_PATH = Path(config["DEFAULT_TRACKS_PATH"])
DEFAULT_TAGS_PATH = Path(config["DEFAULT_TAGS_PATH"])
DEFAULT_TEMPLATES_PATH = Path(config["DEFAULT_TEMPLATES_PATH"])
DEFAULT_PLAYLISTS_PATH = Path(config["DEFAULT_PLAYLISTS_PATH"])

"""
FILE USE:
Functions for general library purpose
Functionality will be used in GUI version
"""

# JSON OPERATIONS


def load_tracks_json(input_path: Path = DEFAULT_TRACKS_PATH) -> list[Track]:
    """Load tracks from a JSON file and return as a list of Track objects.

    Args:
        input_path (Path, optional): The path to the tracks JSON file. Defaults to DEFAULT_TRACKS_PATH.

    Returns:
        list[Track]: A list of Track objects.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        file = json.load(f)
    return [Track(**track) for track in file.get("tracks", [])]


def save_tracks_json(
    tracks: list[Track], output_path: Path = DEFAULT_TRACKS_PATH
) -> None:
    """Save a list of Track objects to a JSON file.

    Args:
        tracks (list[Track]): A list of Track objects.
        output_path (Path, optional): The path to save the JSON file. Defaults to DEFAULT_TRACKS_PATH.
    """
    data = {"tracks": [track.__dict__ for track in tracks]}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_tags_json(input_json_path: Path = DEFAULT_TAGS_PATH) -> list[Tag]:
    """Load tags from a JSON file and return as a list of Tag objects.

    Args:
        input_json_path (Path, optional): The path to the tags JSON file. Defaults to DEFAULT_TAGS_PATH.

    Returns:
        list[Tag]: A list of Tag objects.
    """
    with open(input_json_path, "r", encoding="utf-8") as file:
        tags_data = json.load(file)
        return [
            Tag(
                tag["name"],
                tag["creator"],
                [Track(**track) for track in tag["tracks"]],
                tag["id"],
            )
            for tag in tags_data["tags"]
        ]


def save_tags_json(tags: list[Tag], output_json_path: Path = DEFAULT_TAGS_PATH) -> None:
    """Save a list of Tag objects to a JSON file.

    Args:
        tags (list[Tag]): A list of Tag objects.
        output_json_path (Path, optional): The path to save the JSON file. Defaults to DEFAULT_TAGS_PATH.
    """
    tags_array = [
        {
            "name": tag.name,
            "creator": tag.creator,
            "tracks": [track.to_dict() for track in tag.tracks],
            "id": tag.id,
        }
        for tag in tags
    ]
    tags_dict = {"tags": tags_array}

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(tags_dict, f, indent=4)


def load_templates_json(
    input_json_path: Path = DEFAULT_TEMPLATES_PATH,
) -> list[Template]:
    """Load templates from a JSON file and return as a list of Template objects.

    Args:
        input_json_path (Path, optional): The path to the templates JSON file. Defaults to DEFAULT_TEMPLATES_PATH.

    Returns:
        list[Template]: A list of Template objects.
    """

    def dict_to_tag(tag_data):
        return Tag(
            name=tag_data["name"],
            creator=tag_data["creator"],
            tracks=[Track(**track) for track in tag_data["contents"]],
            tag_id=tag_data["id"],
        )

    with open(input_json_path, "r", encoding="utf-8") as file:
        templates_data = json.load(file)
        return [
            Template(
                name=template["name"],
                creator=template["creator"],
                contents=[
                    [
                        {
                            "item": (
                                Track(**item["item"])
                                if item["type"] == "track"
                                else dict_to_tag(item["item"])
                            ),
                            "probability": item["probability"],
                        }
                        for item in index_items
                    ]
                    for index_items in template["contents"]
                ],
                template_id=template["id"],  # Updated to use `template_id`
            )
            for template in templates_data["templates"]
        ]


def save_templates_json(
    templates: list, output_json_path: Path = DEFAULT_TEMPLATES_PATH
) -> None:
    """Save a list of Template objects to a JSON file.

    Args:
        templates (list): A list of Template objects.
        output_json_path (Path, optional): The path to save the JSON file. Defaults to DEFAULT_TEMPLATES_PATH.
    """

    def tag_to_dict(tag):
        return {
            "name": tag.name,
            "creator": tag.creator,
            "contents": [track.__dict__ for track in tag.tracks],
            "id": tag.id,
        }

    templates_array = [
        {
            "name": template.name,
            "creator": template.creator,
            "contents": [
                [
                    {
                        "item": (
                            track["item"].__dict__
                            if isinstance(track["item"], Track)
                            else tag_to_dict(track["item"])
                        ),
                        "probability": track["probability"],
                        "type": "track" if isinstance(track["item"], Track) else "tag",
                    }
                    for track in index_items
                ]
                for index_items in template.contents
            ],
            "id": template.id,
        }
        for template in templates
    ]

    templates_dict = {"templates": templates_array}

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(templates_dict, f, indent=4)


def load_playlists_json(
    input_json_path: Path = DEFAULT_PLAYLISTS_PATH,
) -> list[Playlist]:
    """Load playlists from a JSON file and return as a list of Playlist objects.

    Args:
        input_json_path (Path, optional): The path to the playlists JSON file. Defaults to DEFAULT_PLAYLISTS_PATH.

    Returns:
        list[Playlist]: A list of Playlist objects.
    """
    with open(input_json_path, "r", encoding="utf-8") as file:
        playlists_data = json.load(file)
        return [
            Playlist(
                playlist["name"],
                playlist["creator"],
                [Track(**track) for track in playlist["tracks"]],
                playlist["id"],
                playlist["spotify_id"],
            )
            for playlist in playlists_data["playlists"]
        ]


def save_playlists_json(
    playlists: list[Playlist], output_json_path: Path = DEFAULT_PLAYLISTS_PATH
) -> None:
    """Save a list of Playlist objects to a JSON file.

    Args:
        playlists (list[Playlist]): A list of Playlist objects.
        output_json_path (Path, optional): The path to save the JSON file. Defaults to DEFAULT_PLAYLISTS_PATH.
    """

    playlists_array = [
        {
            "name": playlist.name,
            "creator": playlist.creator,
            "tracks": [track.to_dict() for track in playlist.tracks],
            "id": playlist.id,
            "spotify_id": playlist.spotify_id,
        }
        for playlist in playlists
    ]

    playlists_dict = {"playlists": playlists_array}

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(playlists_dict, f, indent=4)


def backup(
    tracks: list[Track],
    tags: list[Tag],
    templates: list[Template],
    playlists: list[Playlist],
    output_path: Path = DEFAULT_BACKUP_PATH,
) -> None:
    """Backup the current state of the program data to JSON files.

    Args:
        tracks (list[Track]): List of Track objects to backup.
        tags (list[Tag]): List of Tag objects to backup.
        templates (list[Template]): List of Template objects to backup.
        playlists (list[Playlist]): List of Playlist objects to backup.
        output_path (Path, optional): The path to save the backup files. Defaults to DEFAULT_BACKUP_PATH.
    """
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    save_tracks_json(tracks, output_path / "tracks.json")
    save_tags_json(tags, output_path / "tags.json")
    save_templates_json(templates, output_path / "templates.json")
    save_playlists_json(playlists, output_path / "playlists.json")


# DATA MANAGEMENT / OPERATIONS


def remove_duplicate_ids(items: list) -> list:
    """Given a list of items, remove any duplicates based on the item's ID.

    ID refers to either a uuid or a Spotify ID.

    Args:
        items (list): A list of items where each item has an 'id' attribute.

    Returns:
        list: A list of items with duplicates removed.
    """
    seen_ids = set()
    unique_items = []
    for item in items:
        if item.id not in seen_ids:
            unique_items.append(item)
            seen_ids.add(item.id)
    return unique_items


def remove_duplicate_names(items: list) -> list:
    """Given a list of items, remove any duplicates with the same name.

    Main use is for auto-generated tags when generating tags than have already exist,
    preventing duplicates.

    Args:
        items (list): A list of items where each item has a 'name' attribute.

    Returns:
        list: A list of items with duplicates removed.
    """
    seen_names = set()
    unique_items = []
    for item in items:
        if item.name not in seen_names:
            unique_items.append(item)
            seen_names.add(item.name)
    return unique_items


def check_file_for_json_with_key(input_path: str, key: str) -> bool:
    """Check if a JSON file has a key and if the key has a list associated with it.

    Main use is to check files to prevent errors when the JSON is misstructured.

    Args:
        input_path (str): The path to the JSON file.
        key (str): The key to check for in the JSON file.

    Returns:
        bool: True if the key exists and has a list associated with it, False otherwise.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        file = json.load(f)

    if key not in file:
        print(
            f"The given file doesn't have the required key: {key}, and can't be read into the program."
        )
        return False

    if not isinstance(file[key], list):
        print(
            f"The given file has the proper key ({key}), but doesn't have a list associated with it."
        )
        return False

    return True


def find_items_from_attribute(items: list, attribute: str, value: str) -> list:
    """Find items in a list that have a specific attribute with a specific value.

    Example use: check the track list for all tracks with the artist "The Black Keys".

    Args:
        items (list): A list of items to search through.
        attribute (str): The attribute to search for.
        value (str): The value to search for in the attribute.

    Returns:
        list: A list of items that have the attribute with the given value.
    """
    matching_items = []
    for item in items:
        if hasattr(item, attribute) and getattr(item, attribute) == value:
            matching_items.append(item)
    return matching_items


def find_num_of_items_with_attribute(items: list, attribute: str, value: str) -> int:
    """Find the number of items in a list that have a specific attribute with a specific value.

    Example use: check the track list for the number of tracks with the artist "The Black Keys".

    Args:
        items (list): A list of items to search through.
        attribute (str): The attribute to search for.
        value (str): The value to search for in the attribute.

    Returns:
        int: The number of items that have the attribute with the given value.
    """
    count = 0
    for item in items:
        if hasattr(item, attribute) and getattr(item, attribute) == value:
            count += 1
    return count


def changes_made_to_data(
    current_tag_list: list[Tag],
    saved_tag_list: list[Tag],
    current_template_list: list[Template],
    saved_template_list: list[Template],
    current_playlist_list: list[Playlist],
    saved_playlist_list: list[Playlist],
) -> bool:
    """Check if changes have been made to the data since the last save.

    Args:
        current_tag_list (list[Tag]): Tag list storing the changes made since the most recent save.
        saved_tag_list (list[Tag]): Tag list from the most recent save.
        current_template_list (list[Template]): Template list storing the changes made since the most recent save.
        saved_template_list (list[Template]): Template list from the most recent save.
        current_playlist_list (list[Playlist]): Playlist list storing the changes made since the most recent save.
        saved_playlist_list (list[Playlist]): Playlist list from the most recent save.

    Returns:
        bool: True if changes have been made, False otherwise.
    """
    return (
        current_tag_list != saved_tag_list
        or current_template_list != saved_template_list
        or current_playlist_list != saved_playlist_list
    )


def generate_tags_by_artist(tracks: list[Track]) -> list[Tag]:
    """Generate tags by artist from a list of tracks.

    Args:
        tracks (list[Track]): A list of Track objects.

    Returns:
        list[Tag]: A list of Tag objects with names of artists, each containing tracks by the artist.
    """
    artists = {track.artist for track in tracks}
    return [
        Tag(artist, "auto", [track for track in tracks if track.artist == artist])
        for artist in artists
    ]


def generate_tags_by_duration(tracks: list[Track]) -> list[Tag]:
    """Generate tags by duration from a list of tracks.

    NOTE: that this function is currently hardcoded with values that work with my liked songs dataset
    Short: 0-3 minutes
    Medium: 3-5 minutes
    Long: 5+ minutes

    Args:
        tracks (list[Track]): A list of Track objects.

    Returns:
        list[Tag]: A list of Tag objects with names of durations, each containing tracks of that duration.
    """
    short_tracks = [track for track in tracks if track.duration <= 180000]
    medium_tracks = [track for track in tracks if 180000 < track.duration <= 300000]
    long_tracks = [track for track in tracks if track.duration > 300000]

    return [
        Tag("Short Tracks", "auto", short_tracks),
        Tag("Medium Tracks", "auto", medium_tracks),
        Tag("Long Tracks", "auto", long_tracks),
    ]


# API COMMUNICATION


def fetch_tracks_from_API(output_path: Path = DEFAULT_TRACKS_PATH) -> float:
    """Fetch tracks from the Spotify API and save to a JSON file.

    Restrained to the free tier of the Spotify API, fetching the user's liked songs in batches of 50.

    Args:
        output_path (Path, optional): The path to save the JSON file. Defaults to DEFAULT_TRACKS_PATH.

    Returns:
        float: Time taken to fetch tracks from the API.
    """
    start_time = time.time()

    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost/",
            scope="user-library-read",
        )
    )

    saved_tracks = (
        sp.current_user_saved_tracks()
    )  # first request of saved tracks just to get the total number of tracks.
    total_saved_tracks = saved_tracks["total"]
    current_tracks_complete = 0
    tracks_at_a_time = 50  # API won't accept numbers larger than 50 for personal use
    track_data = {
        "tracks": []
    }  # create a dictionary that will be filled with my array of tracks

    for _ in range(math.floor(total_saved_tracks / tracks_at_a_time)):
        saved_tracks = sp.current_user_saved_tracks(
            limit=tracks_at_a_time, offset=current_tracks_complete
        )
        for track_item in saved_tracks[
            "items"
        ]:  # using a normal loop instead of enumerate because i don't need to use the index
            track = track_item["track"]
            track_data["tracks"].append(
                {
                    "name": track["name"],
                    "image": track["album"]["images"][0]["url"],
                    "artist": track["artists"][0]["name"],
                    "track_id": track["id"],
                    "duration": track["duration_ms"],
                }
            )

        current_tracks_complete = current_tracks_complete + tracks_at_a_time

    if not total_saved_tracks % tracks_at_a_time == 0:
        saved_tracks = sp.current_user_saved_tracks(
            limit=total_saved_tracks - current_tracks_complete,
            offset=current_tracks_complete,
        )
        for track_item in saved_tracks[
            "items"
        ]:  # using a normal loop instead of enumerate because i don't need to use the index
            track = track_item["track"]
            track_data["tracks"].append(
                {
                    "name": track["name"],
                    "image": track["album"]["images"][0]["url"],
                    "artist": track["artists"][0]["name"],
                    "track_id": track["id"],
                    "duration": track["duration_ms"],
                }
            )
        current_tracks_complete = current_tracks_complete + (
            total_saved_tracks - current_tracks_complete
        )  # this line could be deleted, but may be useful for testing

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(track_data, f, indent=4)

    return round((time.time() - start_time), 2)


def upload_playlist_to_spotify(playlist: Playlist) -> None:
    """Upload a playlist to Spotify using the Spotify API.

    Args:
        playlist (Playlist): The playlist to upload to Spotify.
    """
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost/",
            scope="playlist-modify-public playlist-modify-private",
        )
    )

    user_id = sp.current_user()["id"]

    if playlist.spotify_id:
        try:
            existing_playlist = sp.playlist(playlist.spotify_id)
            print(f"Playlist '{playlist.name}' already exists.")

            sp.playlist_replace_items(existing_playlist["id"], [])
            print("Removed all tracks from the existing playlist.")

        except spotipy.exceptions.SpotifyException:
            print(f"Playlist ID not found, creating a new playlist '{playlist.name}'.")

    if not playlist.spotify_id or "existing_playlist" not in locals():
        spotify_playlist = sp.user_playlist_create(user_id, playlist.name, public=False)
        print(f"Created new playlist: {spotify_playlist['name']}")

        playlist.spotify_id = spotify_playlist["id"]

    track_ids = [track.track_id for track in playlist.tracks]
    sp.user_playlist_add_tracks(user_id, playlist.spotify_id, track_ids)
    print(f"Added {len(track_ids)} new tracks to the playlist.")


# OTHER UTILITIES


def create_json(filename: int, location: Path = DEFAULT_JSON_PATH) -> None:
    """Create a JSON file with a given filename at a given location.

    Args:
        filename (int): Name of the JSON file to create.
        location (Path, optional): Location to save the JSON file. Defaults to DEFAULT_JSON_PATH.
    """
    location = Path(location)
    location.mkdir(parents=True, exist_ok=True)
    file_path = location / f"{filename}.json"
    data = {filename: []}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
