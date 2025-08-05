import { getCurrentUser } from "../web";

export function transformSpotifyTrack(item: any, user_id_in: number) {
  const track = item.track;
  return {
    user_id: user_id_in,
    added_at: item.added_at, // ISO 8601 from Spotify
    name: track.name,
    image: track.album.images?.[0]?.url ?? "", // required by schema
    spotify_id: track.id,
  }; // needs to match the TrackIn model on the backend to be passed in!
}

export async function transformTrackList(items: any[]) {
  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");

  return items.map((item) => transformSpotifyTrack(item, user.id));
}
