from pydantic import BaseModel


class SaveDatabaseModel(BaseModel):
    host: str | None = None
    port: int | None = None
    username: str
    password: str
