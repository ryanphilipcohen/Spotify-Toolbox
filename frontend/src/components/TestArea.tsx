import React from "react";
import { syncTracks } from "../lib/apis/web";
import { getSavedTracks } from "../lib/apis/spotify";
const TestArea: React.FC = () => {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
      <button
        onClick={async () => {
          await syncTracks();
          console.log("done");
        }}
      >
        sync
      </button>
      <button
        onClick={async () => {
          await console.log(getSavedTracks(5));
        }}
      >
        get tracks
      </button>
    </div>
  );
};

export default TestArea;
