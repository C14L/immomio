from datetime import datetime
from pydantic import BaseModel

class Artist(BaseModel):
    id: int
    spotify_id: str | None
    name: str
    created: datetime
    updated: datetime
    edited: datetime | None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda x: x.isoformat(" ")}


class WritableArtist(BaseModel):
    name: str
