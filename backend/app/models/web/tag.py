from pydantic import BaseModel

"""
Pydantic models are used for data validation.
It specifies the structure for how a tag object should be sent to and from the API.
This makes JSON data sent to and from the API function more like Java (or other stricter languages) objects
"""


class TagIn(BaseModel):
    id: int | None = None
    user_id: int | None = 1
    name: str
    type: str
    parent: int | None = None
    locked: bool = False


class TagOut(TagIn):
    pass
