import { getCurrentUser } from "../web";

export function transformSpotifyTrack(item: any, user_id_in: number) {
  const track = item.track;
  return {
    user_id: user_id_in,
    name: track.name,
    artists: track.artists.map((artist: any) => artist.name).join(", "),
    album: track.album.name,
    album_id: track.album.id,
    duration_ms: track.duration_ms,
    explicit: track.explicit,
    popularity: track.popularity,
    track_number: track.track_number,
    release_date: track.album.release_date,
    added_at: item.added_at,
    image: track.album.images[0]?.url || null,
    spotify_id: track.id,
  }; // needs to match the TrackIn model on the backend to be passed in!
  /*     user_id: int
    name: str
    artists: str
    album: str
    album_id: str
    duration_ms: int
    explicit: bool
    popularity: int
    track_number: int
    release_date: str
    added_at: str
    image: str | None = None
    spotify_id: str
    */
}

export async function transformTrackList(items: any[]) {
  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");

  return items.map((item) => transformSpotifyTrack(item, user.id));
}
