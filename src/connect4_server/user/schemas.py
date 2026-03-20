from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UserResponse(BaseModel):
    id: int
    username: str


class UserSearchResult(BaseModel):
    id: int
    username: str
