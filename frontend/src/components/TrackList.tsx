// modified from https://www.geeksforgeeks.org/reactjs/implementing-pagination-and-infinite-scrolling-with-react-hooks/

import React, { useState, useEffect, useRef } from "react";
import { getTracks } from "../lib/apis/web/index";

const pageSize = 10;

interface TrackListProps {
  refreshSignal?: number;
}

const TrackList: React.FC<TrackListProps> = ({ refreshSignal = 0 }) => {
  const [loadedData, setLoadedData] = useState<any[]>([]);
  const [moreData, setMoreData] = useState(true);

  const startRef = useRef(0);
  const loadingRef = useRef(false);

  const loadMoreData = async () => {
    if (loadingRef.current || !moreData) return;
    loadingRef.current = true;

    const currentStart = startRef.current;

    try {
      const newData = await getTracks(currentStart, currentStart + pageSize);

      if (Array.isArray(newData) && newData.length > 0) {
        setLoadedData((prev) => [...prev, ...newData]);
        startRef.current += newData.length;

        if (newData.length < pageSize) setMoreData(false);
      } else {
        setMoreData(false);
      }
    } catch (err) {
      console.error("Error loading data", err);
      setMoreData(false);
    } finally {
      loadingRef.current = false;
    }
  };

  // Reset when refreshSignal changes
  useEffect(() => {
    setLoadedData([]);
    startRef.current = 0;
    setMoreData(true);
    loadMoreData(); // reload first page
  }, [refreshSignal]);

  // Infinite scroll
  useEffect(() => {
    const handleScroll = () => {
      const nearBottom =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (nearBottom) {
        loadMoreData();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div>
      {loadedData.map((item, index) => (
        <div key={index} className="infiniteScroll">
          <h3>Spotify ID: {item.spotify_id}</h3>
          <h4>Name: {item.name}</h4>
          <p>Added at: {item.added_at}</p>
          <img src={item.image} alt={item.name} width={100} />
          <hr />
        </div>
      ))}
      {loadingRef.current && <div>Loading...</div>}
      {!loadingRef.current && !moreData && <div>No more data</div>}
    </div>
  );
};

export default TrackList;
