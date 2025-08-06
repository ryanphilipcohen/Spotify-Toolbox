import { transformTrackList } from "../spotify/transform";
import { getAllSavedTracks } from "../spotify";

export async function getCurrentUser(): Promise<any> {
  const token = localStorage.getItem("app_access_token");
  if (!token) throw new Error("App access token not found.");
  const res = await fetch("http://localhost:8000/user/current", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to fetch current user: ${error.error}`);
  }
  const data = await res.json();
  return data.user;
}

export async function getTags(): Promise<string[]> {
  const token = localStorage.getItem("app_access_token");
  if (!token) throw new Error("App access token not found.");
  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");
  const res = await fetch("http://localhost:8000/tag/tags", {
    headers: {
      Authorization: `Bearer ${token}`,
      "user-id": user.id,
    },
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to fetch tags: ${error.error}`);
  }
  const data = await res.json();
  return data;
}

export async function getTagsHierarchy(): Promise<any[]> {
  const token = localStorage.getItem("app_access_token");
  if (!token) throw new Error("App access token not found.");

  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");
  const res = await fetch("http://localhost:8000/tag/tags_hierarchy", {
    headers: {
      Authorization: `Bearer ${token}`,
      "user-id": user.id,
    },
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to fetch tags hierarchy: ${error.error}`);
  }
  const data = await res.json();
  return data;
}

export async function syncTracks() {
  const app_token = localStorage.getItem("app_access_token");
  if (!app_token) throw new Error("You must log in to the app first.");
  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");

  let savedTracks = await getAllSavedTracks();
  let savedTracksObjects = await transformTrackList(savedTracks);

  const res = await fetch("http://localhost:8000/track/sync-tracks", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${app_token}`,
      "Content-Type": "application/json",
      "user-id": user.id.toString(),
    },
    body: JSON.stringify(savedTracksObjects),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to sync tracks: ${error.error}`);
  }

  const data = await res.json();
  return data;
}

export async function getTracks(
  start: number = 0,
  end: number = 10,
  sort_by: string = "added_at",
  order: "asc" | "desc" = "desc"
): Promise<any[]> {
  const token = localStorage.getItem("app_access_token");
  if (!token) throw new Error("App access token not found.");
  const user = await getCurrentUser();
  if (!user) throw new Error("User not found.");
  const res = await fetch(
    `http://localhost:8000/track/tracks?start=${start}&end=${end}&sort_by=${sort_by}&order=${order}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "user-id": user.id.toString(),
      },
    }
  );
  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Failed to fetch tracks: ${error.error}`);
  }

  const data = await res.json();
  return data;
}
