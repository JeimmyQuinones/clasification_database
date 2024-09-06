from pydantic import BaseModel


class UserEntity(BaseModel):
    username: str
    password: str
    id: int | None = None
