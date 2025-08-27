import React, { useState } from "react";
import { syncTracks } from "../lib/apis/web";
import TrackList from "./TrackList";

const TrackLibrary: React.FC = () => {
  const [refreshSignal, setRefreshSignal] = useState(0);
  return (
    <div>
      <button
        onClick={async () => {
          await syncTracks();
          setRefreshSignal((prev) => prev + 1);
        }}
      >
        sync
      </button>
      <TrackList />
    </div>
  );
};

export default TrackLibrary;
