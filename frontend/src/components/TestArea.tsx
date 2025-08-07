import React, { useState } from "react";
import TagTree from "./TagTree";
import { type Tag } from "../types/tag";

interface Props {}

const TestArea: React.FC<Props> = (props) => {
  const [selectedTag, setSelectedTag] = useState<Tag | null>(null);

  const handleTagClick = (tag: Tag) => {
    setSelectedTag(tag);
  };

  return (
    <div>
      <div style={{ paddingLeft: "220px" }}>
        <TagTree onTagClick={handleTagClick} />
        {selectedTag ? (
          <div>Selected Tag: {selectedTag.name}</div>
        ) : (
          <p>No tag selected.</p>
        )}
      </div>
    </div>
  );
};

export default TestArea;
