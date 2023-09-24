from pydantic import BaseModel


class SClient(BaseModel):
    username: str
