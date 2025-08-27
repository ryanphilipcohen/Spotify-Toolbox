import React, { useEffect, useState, useRef, useCallback } from "react";
import { FixedSizeList as List } from "react-window";
import type { ListOnItemsRenderedProps } from "react-window";
import { getTracks } from "../lib/apis/web/index";

const PAGE_SIZE = 20;

interface TrackListProps {
  refreshSignal?: number;
}

const TrackList: React.FC<TrackListProps> = ({ refreshSignal = 0 }) => {
  const [tracks, setTracks] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const startRef = useRef(0);
  const isLoadingRef = useRef(false);
  const hasMoreRef = useRef(true);

  // 🔑 Stable loadMore function
  const loadMore = useCallback(async () => {
    // Check against the current values in the refs
    if (isLoadingRef.current || !hasMoreRef.current) return;

    isLoadingRef.current = true;
    setIsLoading(true);

    try {
      const newTracks = await getTracks(
        startRef.current,
        startRef.current + PAGE_SIZE
      );
      setTracks((prev) => [...prev, ...newTracks]);
      startRef.current += PAGE_SIZE;

      if (newTracks.length < PAGE_SIZE) {
        hasMoreRef.current = false;
        setHasMore(false);
      }
    } finally {
      isLoadingRef.current = false;
      setIsLoading(false);
    }
  }, []); // Empty dependency array makes this function truly stable

  // 🔑 useEffect to handle refresh signal
  useEffect(() => {
    // Reset all state and ref values
    setTracks([]);
    setHasMore(true);
    startRef.current = 0;
    hasMoreRef.current = true;
    // isLoadingRef.current does not need to be reset since it will be false after the previous fetch completes.

    loadMore();
  }, [refreshSignal]); // Now, the effect only runs when refreshSignal changes

  const Row = ({
    index,
    style,
  }: {
    index: number;
    style: React.CSSProperties;
  }) => {
    const item = tracks[index];

    if (!item) {
      return (
        <div style={style} className="track-list__item track-list__loading">
          Loading...
        </div>
      );
    }

    return (
      <div style={style} className="track-list__item">
        <img className="track-list__image" src={item.image} alt={item.name} />
        <div className="track-list__info">
          <h4 className="track-list__name">{item.name}</h4>
          <p className="track-list__artists">{item.artists}</p>
        </div>
        <div className="track-list__duration">{item.duration_ms}</div>
      </div>
    );
  };

  return (
    <div className="track-list">
      <List
        className="track-list__list"
        height={600}
        itemCount={hasMore ? tracks.length + 1 : tracks.length}
        itemSize={70}
        width="100%"
        onItemsRendered={({ visibleStopIndex }: ListOnItemsRenderedProps) => {
          // Use the refs for the check
          if (
            !isLoadingRef.current &&
            hasMoreRef.current &&
            visibleStopIndex >= tracks.length - 5
          ) {
            loadMore();
          }
        }}
      >
        {Row}
      </List>
      {!isLoading && !hasMore && (
        <div className="track-list__end">No more data</div>
      )}
    </div>
  );
};

export default TrackList;
