import React, { useEffect, useState } from "react";
import { getTagsHierarchy } from "../lib/apis/web";
import { type Tag } from "../types/tag";

interface TagTreeProps {
  onTagClick: (tag: Tag) => void;
  includeAddButtons?: boolean;
}

const TagTree: React.FC<TagTreeProps> = ({
  onTagClick,
  includeAddButtons = false,
}) => {
  const [rootTag, setRootTag] = useState<Tag | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const data = await getTagsHierarchy();
        setRootTag(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };
    fetchTags();
  }, []);

  const [openTags, setOpenTags] = useState<Record<number, boolean>>({});

  const toggleTag = (id: number) => {
    setOpenTags((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleAddTag = (parentId: number | null) => {
    console.log(`Add tag under parent ID: ${parentId}`);
  };

  const renderTagList = (
    tags: Tag[],
    parentId: number | null,
    depth: number
  ) => (
    <div>
      {tags.map((tag) => renderTag(tag, depth))}
      {includeAddButtons && (
        <div style={{ marginLeft: depth * 20 }}>
          <button onClick={() => handleAddTag(parentId)}>Add Tag Here</button>
        </div>
      )}
    </div>
  );

  const renderTag = (tag: Tag, depth: number) => {
    const isOpen = openTags[tag.id] ?? false;
    const hasChildren = tag.children && tag.children.length > 0;

    return (
      <div key={tag.id}>
        <div style={{ marginLeft: depth * 20 }}>
          <button
            onClick={() => hasChildren && toggleTag(tag.id)}
            style={{ marginRight: 8 }}
            disabled={!hasChildren}
          >
            {hasChildren ? (isOpen ? "v" : ">") : "*"}
          </button>
          {tag.name}
        </div>
        {isOpen && renderTagList(tag.children || [], tag.id, depth + 1)}
      </div>
    );
  };

  if (loading) return <p>Loading tags...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!rootTag) return <p>No tags found.</p>;

  return (
    <div>
      {renderTagList(rootTag.children || [], rootTag.id, 1)}
      {includeAddButtons && (
        <button
          style={{ marginLeft: 10 }}
          onClick={() => handleAddTag(rootTag.id)}
        >
          Add Tag Here
        </button>
      )}
    </div>
  );
};

export default TagTree;
