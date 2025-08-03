from pydantic import BaseModel


class TagIn(BaseModel):
    id: int | None = None
    user_id: int | None = 1
    name: str
    type: str
    parent: int | None = None
    locked: bool = False


class TagOut(TagIn):
    pass
