from pydantic import BaseModel


class SUserAuth(BaseModel):
    name: str
    password: str


class SUserToken(BaseModel):
    access_token: str
