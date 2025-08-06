// modified from https://www.geeksforgeeks.org/reactjs/implementing-pagination-and-infinite-scrolling-with-react-hooks/

import React, { useState, useEffect } from "react";
import { getTracks } from "../lib/apis/web/index";

const pageSize = 100;

function InfiniteScroll() {
  const [loadedData, setLoadedData] = useState([]);
  const [start, setStart] = useState(0);
  const [loading, setLoading] = useState(false);
  const [moreData, setMoreData] = useState(true);

  const GetData = async (startIndex, pageSize) => {
    const endIndex = startIndex + pageSize;
    return await getTracks(startIndex, endIndex);
  };

  const loadMoreData = async () => {
    if (loading || !moreData) return;
    setLoading(true);
    try {
      const newData = await GetData(start, pageSize);
      if (Array.isArray(newData) && newData.length > 0) {
        setLoadedData((prev) => [...prev, ...newData]);
        setStart((prev) => prev + newData.length);
        if (newData.length < pageSize) setMoreData(false); // no more pages
      } else {
        setMoreData(false);
      }
    } catch (err) {
      console.error("Error loading data", err);
      setMoreData(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMoreData(); // initial load
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      const nearBottom =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (nearBottom && !loading && moreData) {
        loadMoreData();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [loading, moreData]);

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
      {loading && <div>Loading...</div>}
      {!loading && !moreData && <div>No more data</div>}
    </div>
  );
}

export default InfiniteScroll;
