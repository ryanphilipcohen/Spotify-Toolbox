import React, { useState } from "react";
import TagTree from "./TagTree";
import { type Tag } from "../types/tag";
import { addTag, getCurrentUser } from "../lib/apis/web";
import { useLocation, useNavigate } from "react-router-dom";

const TagCreationForm: React.FC = () => {
  const navigate = useNavigate();

  const location = useLocation();
  const parentTag = (location.state as { parentTag?: Tag | null })?.parentTag;

  const rootTag: Tag = {
    id: 1,
    name: "root",
    type: "string",
    parent: null,
    locked: true,
    user_id: 0,
    children: [],
  };

  const [selectedParent, setSelectedParent] = useState<Tag>(
    parentTag ?? rootTag
  );

  const [entry, setEntry] = useState("");
  const [showTagTree, setShowTagTree] = useState(false);
  const [refreshSignal, setRefreshSignal] = useState(0);

  const updateNameInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEntry(e.target.value);
  };

  const updateParentSelection = (parent: Tag) => {
    setSelectedParent(parent);
    setShowTagTree(false);
  };

  const setParentToRoot = () => setSelectedParent(rootTag);

  const handleTagDeleted = (deletedTagId: number) => {
    if (selectedParent.id === deletedTagId) {
      setParentToRoot();
    }
    // Optionally, also refresh tag tree if needed (or rely on refreshSignal)
    setRefreshSignal((prev) => prev + 1);
  };

  return (
    <div className="text-white p-4 rounded border border-gray-700 max-w-sm mx-auto">
      <div>
        Name: <input value={entry} onChange={updateNameInput}></input>
      </div>
      <div>
        Parent:
        <button
          className="border border-gray-700 mx-2"
          onClick={() => setShowTagTree(!showTagTree)}
        >
          {selectedParent.name === "root" ? "None" : selectedParent.name}
        </button>
        <button onClick={setParentToRoot}>X</button>
        {showTagTree && (
          <TagTree
            onTagClick={updateParentSelection}
            includeAddButtons={false}
            includeDeleteButtons={false}
            selectedTag={selectedParent}
            refreshSignal={refreshSignal}
            onTagDeleted={handleTagDeleted}
          />
        )}
      </div>
      <button
        onClick={async () => {
          const user = await getCurrentUser();
          if (!user) {
            console.error("User not found.");
            return;
          }

          const tag = {
            name: entry,
            type: "string",
            parent: selectedParent.id,
            locked: false,
            user_id: user.id,
          };
          setRefreshSignal((prev) => prev + 1); // possibly not needed since I'm swapping pages
          await addTag(tag);
          navigate(-1);
        }}
      >
        Create Tag
      </button>
    </div>
  );
};

export default TagCreationForm;
