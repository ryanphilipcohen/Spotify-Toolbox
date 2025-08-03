// Note: This code was adapted from the Spotify Web API documentation
// I Didn't write this code, but I am using it in my project.

import { getUserData } from "../spotify";

const clientId = "735d26afaae14581982ae1e53aee0540";
const redirectUrl = "http://localhost:5173/"; // TODO: make this a configurable environment variable
const authorizationEndpoint = "https://accounts.spotify.com/authorize";
const tokenEndpoint = "https://accounts.spotify.com/api/token";
const scope =
  "user-read-private user-read-email user-library-read user-library-modify";

// Data structure that manages the current active token, caching it in localStorage
const spotifyToken = {
  get access_token() {
    return localStorage.getItem("spotify_access_token") || null;
  },
  get refresh_token() {
    return localStorage.getItem("spotify_refresh_token") || null;
  },
  get expires_in() {
    return localStorage.getItem("spotify_expires_in") || null;
  },
  get expires() {
    return localStorage.getItem("spotify_expires") || null;
  },

  save: function (response) {
    const { access_token, refresh_token, expires_in } = response;
    localStorage.setItem("spotify_access_token", access_token);
    localStorage.setItem("spotify_refresh_token", refresh_token);
    localStorage.setItem("spotify_expires_in", expires_in);

    const now = new Date();
    const expiry = new Date(now.getTime() + expires_in * 1000);
    localStorage.setItem("spotify_expires", expiry.toISOString());
  },
};

// On page load, try to fetch auth code from current browser search URL
const args = new URLSearchParams(window.location.search);
const code = args.get("code");

// If we find a code, we're in a callback, do a token exchange
if (code) {
  const token = await getToken(code);
  spotifyToken.save(token);

  // Remove code from URL so we can refresh correctly.
  const url = new URL(window.location.href);
  url.searchParams.delete("code");

  const updatedUrl = url.search ? url.href : url.href.replace("?", "");
  window.history.replaceState({}, document.title, updatedUrl);
}

// If we have a token, we're logged in, so fetch user data and render logged in template
if (spotifyToken.access_token) {
  const userData = await getUserData();

  // ✅ Step 1: Get the user's Spotify ID
  const spotify_id = userData.id;

  // ✅ Step 2: Send it to your backend to get your own app's token
  const backendResponse = await fetch(
    "http://localhost:8000/user/spotify-login",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ spotify_id }),
    }
  );
  if (backendResponse.ok) {
    const data = await backendResponse.json();
    localStorage.setItem("app_access_token", data.app_access_token);
  } else {
    console.error("Failed to log in with Spotify.");
  }
}

async function redirectToSpotifyAuthorize() {
  const possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const randomValues = crypto.getRandomValues(new Uint8Array(64));
  const randomString = randomValues.reduce(
    (acc, x) => acc + possible[x % possible.length],
    ""
  );

  const code_verifier = randomString;
  const data = new TextEncoder().encode(code_verifier);
  const hashed = await crypto.subtle.digest("SHA-256", data);

  const code_challenge_base64 = btoa(
    String.fromCharCode(...new Uint8Array(hashed))
  )
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");

  window.localStorage.setItem("code_verifier", code_verifier);

  const authUrl = new URL(authorizationEndpoint);
  const params = {
    response_type: "code",
    client_id: clientId,
    scope: scope,
    code_challenge_method: "S256",
    code_challenge: code_challenge_base64,
    redirect_uri: redirectUrl,
  };

  authUrl.search = new URLSearchParams(params).toString();
  window.location.href = authUrl.toString(); // Redirect the user to the authorization server for login
}

// Spotify API Calls
async function getToken(code: string) {
  const code_verifier = localStorage.getItem("code_verifier");

  const response = await fetch(tokenEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      client_id: clientId,
      grant_type: "authorization_code",
      code: code,
      redirect_uri: redirectUrl,
      code_verifier: code_verifier ?? "",
    }),
  });

  return await response.json();
}

async function refreshToken() {
  const response = await fetch(tokenEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      client_id: clientId,
      grant_type: "refresh_token",
      refresh_token: spotifyToken.refresh_token ?? "",
    }),
  });

  return await response.json();
}

// Click handlers
export async function loginWithSpotifyClick() {
  await redirectToSpotifyAuthorize();
}

async function logoutClick() {
  localStorage.clear();
  window.location.href = redirectUrl;
}

export async function sendTokenToBackend() {
  if (!spotifyToken.access_token) {
    console.error("No access token available.");
    return;
  }

  const response = await fetch("/api/spotify_auth/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      access_token: spotifyToken.access_token,
      refresh_token: spotifyToken.refresh_token,
      expires_in: spotifyToken.expires_in,
      expires: spotifyToken.expires,
    }),
  });

  if (!response.ok) {
    console.error("Failed to send token to backend.");
  }
}
