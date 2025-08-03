import React from "react";
import { getSavedTracks } from "../lib/apis/spotify";
import { getTagsHierarchy } from "../lib/apis/web";

interface Props {}

const TestArea: React.FC<Props> = (props) => {
  return (
    <div className="flex flex-col">
      <button
        onClick={async () => {
          const tracks = await getSavedTracks();
          console.log(tracks);
        }}
      >
        Log Tracks From Spotify
      </button>
      <button
        onClick={async () => {
          const tags = await getTagsHierarchy();
          console.log(tags);
        }}
      >
        Log Tags From Database
      </button>
    </div>
  );
};

export default TestArea;
