from pydantic import BaseModel


class SPayMethod(BaseModel):
    name: str
