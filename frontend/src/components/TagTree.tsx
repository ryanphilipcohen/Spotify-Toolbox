import React, { useEffect, useState } from "react";
import { getTagsHierarchy, deleteTag } from "../lib/apis/web";
import { type Tag } from "../types/tag";
import { useNavigate } from "react-router-dom";

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
  refreshSignal = 0,
  onTagDeleted = () => {},
}) => {
  const [tagRoot, setTagRoot] = useState<Tag | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedTagIds, setExpandedTagIds] = useState<Record<number, boolean>>(
    {}
  );
  const navigate = useNavigate();

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

  const handleAddTag = (parentTag: Tag | null) => {
    navigate("/tags/create", { state: { parentTag } });
  };

  const renderTagChildren = (tags: Tag[], depth: number) => (
    <div>{tags.map((tag) => renderTagNode(tag, depth))}</div>
  );

  const renderTagNode = (tag: Tag, depth: number) => {
    const isExpanded = expandedTagIds[tag.id] ?? false;
    const hasChildren = tag.children && tag.children.length > 0;

    return (
      <div key={tag.id}>
        <div
          style={{
            marginLeft: depth * 20,
            display: "flex",
            alignItems: "center",
            border: "1px solid gray",
            width: "fit-content",
          }}
          className="tag-tree-node"
        >
          <button
            onClick={() => hasChildren && toggleTagExpansion(tag.id)}
            style={{ marginRight: 8 }}
            disabled={!hasChildren}
            className="tag-tree-expand-btn"
          >
            {hasChildren ? (isExpanded ? "v" : ">") : "*"}
          </button>
          <span
            onClick={() => onTagClick(tag)}
            style={{ cursor: "pointer" }}
            className="tag-tree-name"
          >
            {tag.name}
          </span>
          {includeAddButtons && (
            <button
              className="tag-tree-add-btn ml-2"
              onClick={() => handleAddTag(tag)}
            >
              +
            </button>
          )}
          {includeDeleteButtons && (
            <button
              className="tag-tree-delete-btn ml-2"
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
        {isExpanded && renderTagChildren(tag.children || [], depth + 1)}
      </div>
    );
  };

  if (loading) return <p></p>;
  if (error) return <p>{error}</p>;
  if (!tagRoot) return <p>No tags found.</p>;

  return (
    <div className="tag-tree-root">
      {/* Render children if they exist */}
      {renderTagChildren(tagRoot.children || [], 1)}

      {/* Root-level add button always visible */}
      {includeAddButtons && (
        <button
          className="tag-tree-add-btn"
          onClick={() => handleAddTag(tagRoot)}
        >
          +
        </button>
      )}
    </div>
  );
};

export default TagTree;
