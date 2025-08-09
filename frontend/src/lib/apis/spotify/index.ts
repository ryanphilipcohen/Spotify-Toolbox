export async function getSavedTracks(limit = 10, offset = 0): Promise<any[]> {
  const token = localStorage.getItem("spotify_access_token");
  if (!token) throw new Error("Access token not found.");

  const res = await fetch(
    `https://api.spotify.com/v1/me/tracks?limit=${limit}&offset=${offset}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to fetch tracks: ${error.error.message}`);
  }

  const data = await res.json();
  return data.items; // each item includes a `.track` object
}

export async function getAllSavedTracks(): Promise<any[]> {
  let allTracks: any[] = [];
  let offset = 0;
  const limit = 50; // Spotify API max limit per request

  while (true) {
    const tracks = await getSavedTracks(limit, offset);
    if (tracks.length === 0) break; // No more tracks to fetch
    allTracks = allTracks.concat(tracks);
    offset += limit;
  }

  return allTracks;
}

export async function isTokenExpired() {
  const spotify_token = localStorage.getItem("spotify_access_token");
  if (!spotify_token) {
    console.log("no spotify token");
    return false;
  }
  const app_token = localStorage.getItem("app_access_token");
  if (!app_token) {
    console.log("no app token");
    return false;
  }

  try {
    const response = await fetch("https://api.spotify.com/v1/me", {
      headers: {
        Authorization: `Bearer ${spotify_token}`,
      },
    });

    if (response.status === 401) {
      console.log("Token expired or unauthorized");
      return true;
    }

    if (!response.ok) {
      console.log("Unexpected error", response.status);
      return true;
    }
    return false;
  } catch (err) {
    return true;
  }
}

export async function getUserData() {
  const spotifyToken = localStorage.getItem("spotify_access_token");
  const response = await fetch("https://api.spotify.com/v1/me", {
    method: "GET",
    headers: { Authorization: "Bearer " + spotifyToken },
  });

  return await response.json();
}
