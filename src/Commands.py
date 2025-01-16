from Datatypes import *
import spotipy, math, json, time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pathlib import Path
import os

CONFIG_PATH = Path("data/config.json")
with open(CONFIG_PATH, "r") as file:
    config = json.load(file)
DEFAULT_JSON_PATH = config["DEFAULT_JSON_PATH"]
DEFAULT_TRACKS_PATH = config["DEFAULT_TRACKS_PATH"]
DEFAULT_TAGS_PATH = config["DEFAULT_TAGS_PATH"]
DEFAULT_TEMPLATES_PATH = config["DEFAULT_TEMPLATES_PATH"]
DEFAULT_PLAYLISTS_PATH = config["DEFAULT_PLAYLISTS_PATH"]

'''
FILE USE:
Functions for general library purpose
Functionality will be used in GUI version
'''

# JSON OPERATIONS

def load_tracks_json(input_path: Path = DEFAULT_TRACKS_PATH) -> list[Track]:
    with open(input_path, "r") as f:
        file = json.load(f)
    return [Track(**track) for track in file.get("tracks", [])]

def load_tags_json(input_json_path: Path = DEFAULT_TAGS_PATH) -> list[Tag]:
    with open(input_json_path, 'r', encoding='utf-8') as file:
        tags_data = json.load(file)
        return [Tag(tag["name"], [Track(**track) for track in tag["tracks"]], tag["id"]) for tag in tags_data["tags"]]

def save_tags_json(tags: list[Tag], output_json_path: Path = DEFAULT_TAGS_PATH) -> None:
    tags_array = [{"name": tag.name, "tracks": [track.to_dict() for track in tag.tracks], "id": tag.id} for tag in tags]
    tags_dict = {"tags": tags_array}
    
    with open(output_json_path, "w") as f:
        json.dump(tags_dict, f, indent=4)

def load_templates_json(input_json_path: Path = DEFAULT_TEMPLATES_PATH) -> list[Template]:
    def dict_to_tag(tag_data):
        return Tag(
            name=tag_data["name"],
            tracks=[Track(**track) for track in tag_data["contents"]],
            tag_id=tag_data["id"]
        )
    
    with open(input_json_path, 'r', encoding='utf-8') as file:
        templates_data = json.load(file)
        return [
            Template(
                name=template["name"],
                contents=[
                    [
                        {
                            "item": Track(**item["item"]) if item["type"] == "track" else dict_to_tag(item["item"]),
                            "probability": item["probability"]
                        }
                        for item in index_items
                    ]
                    for index_items in template["contents"]
                ],
                template_id=template["id"]  # Updated to use `template_id`
            )
            for template in templates_data["templates"]
        ]

    
def save_templates_json(templates: list, output_json_path: Path = DEFAULT_TEMPLATES_PATH) -> None:
    def tag_to_dict(tag):
        return {
            "id": tag.id,
            "name": tag.name,
            "contents": [track.__dict__ for track in tag.tracks]
        }

    templates_array = [
        {
            "name": template.name,
            "id": template.id,
            "contents": [
                [
                    {
                        "item": track["item"].__dict__ if isinstance(track["item"], Track) else tag_to_dict(track["item"]),
                        "probability": track["probability"],
                        "type": "track" if isinstance(track["item"], Track) else "tag"
                    }
                    for track in index_items
                ]
                for index_items in template.contents
            ]
        }
        for template in templates
    ]
    
    templates_dict = {"templates": templates_array}
    
    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump(templates_dict, f, indent=4)

def load_playlists_json(input_json_path: Path = DEFAULT_PLAYLISTS_PATH) -> list[Playlist]:
    with open(input_json_path, 'r', encoding='utf-8') as file:
        playlists_data = json.load(file)
        return [Playlist(playlist["name"], [Track(**track) for track in playlist["tracks"]], playlist["id"], playlist["spotify_id"]) for playlist in playlists_data["playlists"]]

def save_playlists_json(playlists: list[Playlist], output_json_path: Path = DEFAULT_PLAYLISTS_PATH) -> None:
    playlists_array = [{"name": playlist.name, "tracks": [track.to_dict() for track in playlist.tracks], "id": playlist.id, "spotify_id": playlist.spotify_id} for playlist in playlists]
    playlists_dict = {"playlists": playlists_array}
    
    with open(output_json_path, "w") as f:
        json.dump(playlists_dict, f, indent=4)

def create_json(filename: int, location: Path = Path(DEFAULT_JSON_PATH)) -> None:
    location = Path(location)
    location.mkdir(parents=True, exist_ok=True)
    file_path = location / f"{filename}.json"
    data = {
        filename: []
    }
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# DATA MANAGEMENT / OPERATIONS

# Used for both tags and templates
def remove_duplicate_ids(items: list) -> list:
    seen_ids = set()
    unique_tags = []
    for item in items:
        if item.id not in seen_ids:
            unique_tags.append(item)
            seen_ids.add(item.id)
    return unique_tags

def check_file_for_json_with_key(input_path: str, key: str) -> bool:
    with open(input_path, "r") as f:
        file = json.load(f)
    
    if key not in file:
        print(f"The given file doesn't have the required key: {key}, and can't be read into the program.")
        return False
    
    if not isinstance(file[key], list):
        print(f"The given file has the proper key ({key}), but doesn't have a list associated with it.")
        return False
    
    return True

def find_items_from_attribute(items: list, attribute: str, value: str) -> list:
    matching_items = []
    for item in items:
        if hasattr(item, attribute) and getattr(item, attribute) == value:
            matching_items.append(item)
    return matching_items

def find_num_of_items_with_attribute(items: list, attribute: str, value: str) -> int:
    count = 0
    for item in items:
        if hasattr(item, attribute) and getattr(item, attribute) == value:
            count += 1
    return count

# API COMMUNICATION

def fetch_tracks_from_API(output_path: Path = DEFAULT_TRACKS_PATH):
    start_time = time.time()

    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://localhost/', scope="user-library-read"))

    savedTracks = sp.current_user_saved_tracks() #first request of saved tracks just to get the total number of tracks. i could also use this as part of my call to make it more efficient
    totalSavedTracks = savedTracks['total']
    currentTracksComplete = 0
    tracksAtATime = 50 # API won't accept numbers larger than 50 for personal use
    trackData = {"tracks": []} #create a dictionary that will be filled with my array of tracks

    for x in range(math.floor(totalSavedTracks/tracksAtATime)):
        savedTracks = sp.current_user_saved_tracks(limit = tracksAtATime, offset=currentTracksComplete)
        for trackItem in savedTracks["items"]: #using a normal loop instead of enumerate because i don't need to use the index
            track = trackItem['track']
            trackData["tracks"].append({"name": track['name'], "image": track['album']['images'][0]['url'], "artist": track['artists'][0]['name'], "id": track['id'], "duration": track['duration_ms']})

        currentTracksComplete = currentTracksComplete + tracksAtATime

    if not totalSavedTracks%tracksAtATime == 0:
        savedTracks = sp.current_user_saved_tracks(limit = totalSavedTracks-currentTracksComplete, offset=currentTracksComplete)
        for trackItem in savedTracks["items"]: #using a normal loop instead of enumerate because i don't need to use the index
            track = trackItem['track']
            trackData["tracks"].append({"name": track['name'], "image": track['album']['images'][0]['url'], "artist": track['artists'][0]['name'], "id": track['id'], "duration": track['duration_ms']})
        currentTracksComplete = currentTracksComplete + (totalSavedTracks-currentTracksComplete) #this line could be deleted, but may be useful for testing

    with open(output_path, "w") as f:
        json.dump(trackData, f, indent=4)

    return round((time.time() - start_time), 2)

def upload_playlist_to_spotify(playlist: Playlist) -> None:
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://localhost/', scope="playlist-modify-public playlist-modify-private"))

    user_id = sp.current_user()['id']

    if playlist.spotify_id:
        try:
            existing_playlist = sp.playlist(playlist.spotify_id)
            print(f"Playlist '{playlist.name}' already exists.")

            sp.playlist_replace_items(existing_playlist['id'], [])
            print("Removed all tracks from the existing playlist.")

        except spotipy.exceptions.SpotifyException:
            print(f"Playlist ID not found, creating a new playlist '{playlist.name}'.")

    if not playlist.spotify_id or 'existing_playlist' not in locals():
        spotify_playlist = sp.user_playlist_create(user_id, playlist.name, public=False)
        print(f"Created new playlist: {spotify_playlist['name']}")

        playlist.spotify_id = spotify_playlist['id']

    track_ids = [track.id for track in playlist.tracks]
    sp.user_playlist_add_tracks(user_id, playlist.spotify_id, track_ids)
    print(f"Added {len(track_ids)} new tracks to the playlist.")

# OTHER UTILITIES

def create_json(filename: int, location: Path = Path(DEFAULT_JSON_PATH)) -> None:
    location = Path(location)
    location.mkdir(parents=True, exist_ok=True)
    file_path = location / f"{filename}.json"
    data = {
        filename: []
    }
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_config(config_path="data/config.json"):
    config_path = Path(config_path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    
    with open(config_path, "r") as file:
        return json.load(file)