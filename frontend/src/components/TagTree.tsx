import React, { useEffect, useState } from "react";
import { getTagsHierarchy, deleteTag } from "../lib/apis/web";
import { type Tag } from "../types/tag";

interface TagTreeProps {
  onTagClick: (tag: Tag) => void; // Function to handle tag click events is defined by the parent component
  includeAddButtons?: boolean; // Whether to include "Add Tag Here" buttons
  includeDeleteButtons?: boolean; // Whether to include "Delete" buttons for tags
  refreshSignal?: number;
  onTagDeleted?: (deletedTagId: number) => void;
}

const TagTree: React.FC<TagTreeProps> = ({
  onTagClick,
  includeAddButtons = false,
  includeDeleteButtons = true,
  refreshSignal = 0, // default 0
  onTagDeleted = () => {},
}) => {
  // reminder: these constants act just like variables, but require a set function to update their values
  // they are used to store the "state" of the component
  // useState is a React hook that allows you to add state to functional components
  // it returns an array with two elements: the current state and a function to update it
  // the first element is the current state, the second element is a function to update the state
  const [tagRoot, setTagRoot] = useState<Tag | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedTagIds, setExpandedTagIds] = useState<Record<number, boolean>>(
    {}
  );

  const fetchTags = async () => {
    setLoading(true);
    try {
      const data = await getTagsHierarchy();
      setTagRoot(data);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTags();
  }, [refreshSignal]);

  const toggleTagExpansion = (id: number) => {
    setExpandedTagIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleAddTag = (parentId: number | null) => {
    // TODO
    console.log(`Add tag under parent ID: ${parentId}`);
  };

  const renderTagChildren = (
    tags: Tag[],
    parentId: number | null,
    depth: number
  ) => (
    <div>
      {tags.map((tag) => renderTagNode(tag, depth))}
      {includeAddButtons && (
        // temporary styling
        <div style={{ marginLeft: depth * 20 }}>
          <button onClick={() => handleAddTag(parentId)}>Add Tag Here</button>
        </div>
      )}
    </div>
  );

  const renderTagNode = (tag: Tag, depth: number) => {
    const isExpanded = expandedTagIds[tag.id] ?? false;
    const hasChildren = tag.children && tag.children.length > 0;

    return (
      <div key={tag.id}>
        <div
          style={{
            // temporary styling
            marginLeft: depth * 20,
            display: "flex",
            alignItems: "center",
          }}
        >
          <button
            onClick={() => hasChildren && toggleTagExpansion(tag.id)}
            style={{ marginRight: 8 }}
            disabled={!hasChildren}
          >
            {hasChildren ? (isExpanded ? "v" : ">") : "*"}
          </button>
          <span onClick={() => onTagClick(tag)} style={{ cursor: "pointer" }}>
            {tag.name}
          </span>
          {includeDeleteButtons && (
            <button
              className="ml-2"
              onClick={async () => {
                await deleteTag(tag.id);
                const data = await getTagsHierarchy();
                setTagRoot(data);
                onTagDeleted(tag.id);
              }}
            >
              X
            </button>
          )}
        </div>
        {isExpanded && renderTagChildren(tag.children || [], tag.id, depth + 1)}
      </div>
    );
  };

  if (loading) return <p></p>;
  if (error) return <p>{error}</p>;
  if (!tagRoot) return <p>No tags found.</p>;

  return (
    <div>
      {renderTagChildren(tagRoot.children || [], tagRoot.id, 1)}
      {includeAddButtons && (
        <button
          style={{ marginLeft: 10 }}
          onClick={() => handleAddTag(tagRoot.id)}
        >
          Add Tag Here
        </button>
      )}
    </div>
  );
};

export default TagTree;
