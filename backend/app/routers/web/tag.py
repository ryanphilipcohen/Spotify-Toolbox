from fastapi import APIRouter, Header
from backend.app.models.web.tag import TagIn, TagOut
from backend.database import get_connection

router = APIRouter()


@router.post("/")
def create_tag(tag: TagIn):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tag (user_id, name, type, parent, locked) VALUES (?, ?, ?, ?, ?)
            """,
        (tag.user_id, tag.name, tag.type, tag.parent, tag.locked),
    )

    conn.commit()
    conn.close()

    return TagOut(
        id=tag.id,
        user_id=tag.user_id,
        name=tag.name,
        type=tag.type,
        parent=tag.parent,
        locked=tag.locked,
    )


@router.get("/")
def get_tag(tag: TagIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, type, locked FROM tag WHERE user_id = ? AND id = ?
        """,
        (tag.user_id, tag.id),
    )
    tag_data = cursor.fetchone()

    conn.commit()
    conn.close()
    return (
        TagOut(
            id=tag.id,
            user_id=tag.user_id,
            name=tag_data[1],
            type=tag_data[2],
            parent=tag_data[3],
            locked=tag_data[4],
        )
        if tag_data
        else None
    )


@router.get("/tags")
def get_tags(user_id: int = Header(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, type, parent, locked FROM tag WHERE user_id = ?
        """,
        (user_id,),
    )
    tags = cursor.fetchall()

    conn.close()
    return [
        TagOut(
            id=tag[0],
            user_id=user_id,
            name=tag[1],
            type=tag[2],
            parent=tag[3],
            locked=tag[4],
        )
        for tag in tags
    ]


@router.get("/tags_hierarchy")
def get_tags_hierarchy(user_id: int = Header(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, type, parent, locked FROM tag WHERE user_id = ?
        """,
        (user_id,),
    )
    tags = cursor.fetchall()
    conn.close()

    tags = [
        {
            "id": tag[0],
            "name": tag[1],
            "type": tag[2],
            "parent": tag[3],
            "locked": tag[4],
            "user_id": user_id,
        }
        for tag in tags
    ]

    tag_map = {tag["id"]: {**tag, "children": []} for tag in tags}
    root_children = []

    for tag in tags:
        parent_id = tag["parent"]
        if parent_id is None:
            root_children.append(tag_map[tag["id"]])
        else:
            if parent_id in tag_map:
                tag_map[parent_id]["children"].append(tag_map[tag["id"]])
            else:
                # Parent tag not found — optionally treat as root
                root_children.append(tag_map[tag["id"]])

    # Create synthetic root
    root_tag = {
        "id": 0,
        "name": "Root",
        "type": "group",
        "parent": None,
        "locked": False,
        "user_id": user_id,
        "children": root_children,
    }

    return root_tag


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """        SELECT locked FROM tag WHERE id = ? AND user_id = ?
        """,
        (tag_id, user_id),
    )
    result = cursor.fetchone()
    if not result:
        conn.close()
        return {"error": "Tag not found"}
    if result[0]:
        conn.close()
        return {"error": "Tag is locked and cannot be deleted"}
    cursor.execute(
        """
        DELETE FROM tag WHERE id = ?
        """,
        (tag_id,),
    )
    conn.commit()
    conn.close()
    return {"message": "Tag deleted successfully"}
