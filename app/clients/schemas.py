from typing import Optional

from pydantic import BaseModel


class SClientNew(BaseModel):
    username: str


class SClientDelete(BaseModel):
    id: int
