import React from "react";
import { getTagsHierarchy } from "../lib/apis/web";
import { syncTracks } from "../lib/apis/web";

interface Props {}

const TestArea: React.FC<Props> = (props) => {
  return (
    <div className="flex flex-col">
      <button
        onClick={async () => {
          const tracks = await syncTracks();
        }}
      >
        Sync Tracks
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
