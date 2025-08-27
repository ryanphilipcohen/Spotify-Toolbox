import React, { useEffect, useState } from "react";
import { loginWithSpotifyClick } from "../lib/apis/spotify_auth";
import { getUserData, isTokenExpired } from "../lib/apis/spotify";

interface Props {}

export const UserInfo: React.FC<Props> = () => {
  const [_, setToken] = useState<string | null>(null);
  const [valid, setValid] = useState<boolean | null>(null); // null = loading
  const [userInfo, setUserInfo] = useState<any | null>(null);

  useEffect(() => {
    const checkToken = async () => {
      const storedToken = localStorage.getItem("app_access_token");
      setToken(storedToken);

      const expired = await isTokenExpired();
      setValid(!expired);

      if (!expired) {
        const data = await getUserData();
        setUserInfo(data);
      } else {
        setUserInfo(null);
      }
    };

    checkToken();
    const interval = setInterval(checkToken, 10 * 60 * 1000); // 10 minutes
    return () => clearInterval(interval);
  }, []);

  if (valid === null) {
    return <div className="text-white p-4">Loading...</div>;
  }

  return (
    <div className="text-white p-4">
      {valid ? (
        userInfo ? (
          <div>
            <button className="flex items-center space-x-4">
              <img
                className="w-8"
                src={userInfo?.images?.[0]?.url}
                alt="Profile"
              />
              <div>{userInfo?.display_name}</div>
            </button>
          </div>
        ) : (
          <div>Loading user info...</div>
        )
      ) : (
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          onClick={loginWithSpotifyClick}
        >
          Login with Spotify
        </button>
      )}
    </div>
  );
};
