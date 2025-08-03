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
