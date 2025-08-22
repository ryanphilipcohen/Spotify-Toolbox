import React, { useState } from "react";
import TagTree from "./TagTree";

const TagLibrary: React.FC = () => {
  const [refreshSignal, setRefreshSignal] = useState(0);

  const handleTagDeleted = () => {
    setRefreshSignal((prev) => prev + 1);
  };
  return (
    <div>
      <TagTree
        onTagClick={() => {
          console.log("Tag clicked");
        }}
        includeAddButtons={true}
        includeDeleteButtons={false}
        refreshSignal={refreshSignal}
        onTagDeleted={handleTagDeleted}
      />
    </div>
  );
};

export default TagLibrary;
