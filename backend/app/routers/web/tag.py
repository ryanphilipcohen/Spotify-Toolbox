from fastapi import APIRouter, HTTPException, Header, Depends
from backend.app.models.web.tag import TagIn, TagOut
from backend.database import get_connection
from backend.auth import get_current_user


router = APIRouter()


"""
All api endpoints will be formatted in the following way, with a decorator, path, and corresponding function.
API calls related to the user must go through the auth process with get_current_user
"""


@router.post("/")
def create_tag(tag: TagIn, user_id: str = Depends(get_current_user)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tag (user_id, name, type, parent, locked) VALUES (?, ?, ?, ?, ?)
            """,
        (user_id, tag.name, tag.type, tag.parent, tag.locked),
    )

    conn.commit()
    conn.close()

    return TagOut(
        id=cursor.lastrowid,
        user_id=tag.user_id,
        name=tag.name,
        type=tag.type,
        parent=tag.parent,
        locked=tag.locked,
    )


@router.get("/")
def get_tag(tag: TagIn, user_id: str = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, type, locked FROM tag WHERE user_id = ? AND id = ?
        """,
        (user_id, tag.id),
    )

    # only one song has this ID, so we're fetching index 0 of size 1
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
def get_tags(user_id: str = Depends(get_current_user)):

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
            user_id=user_id,  # type: ignore
            name=tag[1],
            type=tag[2],
            parent=tag[3],
            locked=tag[4],
        )
        for tag in tags
    ]


@router.get("/tags_hierarchy")
def get_tags_hierarchy(user_id: str = Depends(get_current_user)):
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
                root_children.append(tag_map[tag["id"]])

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
def delete_tag(tag_id: int, user_id: str = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1) Make sure the tag exists for this user and collect root+descendants
        cte_collect = """
        WITH RECURSIVE descendants(id, locked) AS (
            SELECT id, locked FROM tag WHERE id = ? AND user_id = ?
            UNION ALL
            SELECT t.id, t.locked
            FROM tag t
            JOIN descendants d ON t.parent = d.id
            WHERE t.user_id = ?
        )
        SELECT id FROM descendants;
        """
        cursor.execute(cte_collect, (tag_id, user_id, user_id))
        rows = cursor.fetchall()
        if not rows:
            conn.close()
            raise HTTPException(status_code=404, detail="Tag not found")

        ids_to_delete = [r[0] for r in rows]

        # 2) Check whether any of the (root + descendants) are locked
        cte_check_locked = """
        WITH RECURSIVE descendants(id, locked) AS (
            SELECT id, locked FROM tag WHERE id = ? AND user_id = ?
            UNION ALL
            SELECT t.id, t.locked
            FROM tag t
            JOIN descendants d ON t.parent = d.id
            WHERE t.user_id = ?
        )
        SELECT id FROM descendants WHERE locked = 1;
        """
        cursor.execute(cte_check_locked, (tag_id, user_id, user_id))
        locked = cursor.fetchall()
        if locked:
            locked_ids = [r[0] for r in locked]
            conn.close()
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "One or more tags are locked and cannot be deleted",
                    "locked_ids": locked_ids,
                },
            )

        # 3) Delete all collected IDs in a transaction
        cursor.execute("BEGIN")
        cte_delete = """
        WITH RECURSIVE descendants(id) AS (
            SELECT id FROM tag WHERE id = ? AND user_id = ?
            UNION ALL
            SELECT t.id
            FROM tag t
            JOIN descendants d ON t.parent = d.id
            WHERE t.user_id = ?
        )
        DELETE FROM tag WHERE id IN (SELECT id FROM descendants);
        """
        cursor.execute(cte_delete, (tag_id, user_id, user_id))
        conn.commit()

        return {
            "message": "Tags deleted",
            "deleted_count": len(ids_to_delete),
            "deleted_ids": ids_to_delete,
        }

    except HTTPException:
        # re-raise known HTTP errors
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
