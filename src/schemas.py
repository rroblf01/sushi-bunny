from pydantic import BaseModel


class TableCreate(BaseModel):
    name: str
