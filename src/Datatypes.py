import uuid

class Track():
    def __init__(self, name, image, artist, id, duration):
        self.name = name
        self.image = image
        self.artist = artist
        self.id = id
        self.duration = duration

    def to_dict(self):
        return {
            "name": self.name,
            "image": self.image,
            "artist": self.artist,
            "id": self.id,
            "duration": self.duration
        }

    def __repr__(self):
        return (
            f"  Track Name: {self.name}\n"
            f"  Artist: {self.artist}\n"
            f"  ID: {self.id}\n"
            f"  Duration: {self.duration} seconds\n"
            f"  Image: {self.image}\n"
        )
    
    def list_repr(self):
        return f"{self.name} by {self.artist} ({self.id})"
    
class Tag():
    def __init__(self, name: str, tracks: list = None, tag_id: str = None):
        self.id = tag_id or str(uuid.uuid4())
        self.name = name
        self.tracks = tracks if tracks is not None else []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "tracks": self.tracks
        }

    def __repr__(self) -> str:
        track_list = "\n    ".join(track.list_repr() for track in self.tracks) if self.tracks else "No tracks"
        return (
            f"  Tag Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Tracks:\n"
            f"    {track_list}\n"
        )

class Template:
    def __init__(self, name: str, contents: list = [], template_id: str = None):
        self.name = name
        self.contents = contents
        self.id = template_id or str(uuid.uuid4())

    def __repr__(self):
        contents_list = "\n    ".join(str(content) for content in self.contents) if self.contents else "No contents"
        return (
            f"  Template Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Contents:\n"
            f"    {contents_list}\n"
        )
    
class Playlist:
    def __init__(self, name: str, tracks: list[Track] = [], playlist_id: str = None, spotify_id: str = None):
        self.name = name
        self.tracks = tracks
        self.id = playlist_id or str(uuid.uuid4())
        self.spotify_id = spotify_id

    def __repr__(self) -> str:
        track_list = "\n    ".join(track.list_repr() for track in self.tracks) if self.tracks else "No tracks"
        return (
            f"  Playlist Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Tracks:\n"
            f"    {track_list}\n"
        )