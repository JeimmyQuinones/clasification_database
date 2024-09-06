from pydantic import BaseModel


class AuthToken(BaseModel):
    sub: str | None = None
