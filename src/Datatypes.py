import uuid


class Track:
    def __init__(
        self, name: str, image: str, artist: str, track_id: str, duration: float
    ):
        self.name = name
        self.image = image
        self.artist = artist
        self.track_id = track_id
        self.duration = duration

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "image": self.image,
            "artist": self.artist,
            "track_id": self.track_id,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        return (
            f"  Track Name: {self.name}\n"
            f"  Artist: {self.artist}\n"
            f"  ID: {self.track_id}\n"
            f"  Duration: {self.duration} seconds\n"
            f"  Image: {self.image}\n"
        )

    def short_repr(self) -> str:
        return f"{self.name} by {self.artist} ({self.track_id})"

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return (
            self.track_id == other.track_id
        )  # Assuming track_id uniquely identifies a track


class Tag:
    def __init__(
        self, name: str, creator: str = "user", tracks: list = None, tag_id: str = None
    ):
        self.name = name
        self.creator = creator
        self.tracks = tracks if tracks is not None else []
        self.id = tag_id or str(uuid.uuid4())

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "tracks": self.tracks}

    def __repr__(self) -> str:
        track_list = (
            "\n    ".join(track.short_repr() for track in self.tracks)
            if self.tracks
            else "No tracks"
        )
        return (
            f"  Tag Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Tracks:\n"
            f"    {track_list}\n"
        )

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.tracks == other.tracks
        )


class Template:
    def __init__(
        self,
        name: str,
        creator: str = "user",
        contents: list = None,
        template_id: str = None,
    ):
        self.name = name
        self.creator = creator
        self.contents = contents if contents is not None else []
        self.id = template_id or str(uuid.uuid4())

    def __repr__(self):
        contents_list = (
            "\n    ".join(str(content) for content in self.contents)
            if self.contents
            else "No contents"
        )
        return (
            f"  Template Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Contents:\n"
            f"    {contents_list}\n"
        )

    def __eq__(self, other):
        if not isinstance(other, Template):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.contents == other.contents
        )


class Playlist:
    def __init__(
        self,
        name: str,
        creator: str = "user",
        tracks: list = None,
        playlist_id: str = None,
        spotify_id: str = None,
    ):
        self.name = name
        self.creator = creator
        self.tracks = tracks if tracks is not None else []
        self.spotify_id = spotify_id
        self.id = playlist_id or str(uuid.uuid4())

    def __repr__(self) -> str:
        track_list = (
            "\n    ".join(track.short_repr() for track in self.tracks)
            if self.tracks
            else "No tracks"
        )
        return (
            f"  Playlist Name: {self.name}\n"
            f"  ID: {self.id}\n"
            f"  Tracks:\n"
            f"    {track_list}\n"
        )

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.tracks == other.tracks
            and self.spotify_id == other.spotify_id
        )
