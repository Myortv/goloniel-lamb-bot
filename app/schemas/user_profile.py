from typing import Optional

from pydantic import BaseModel


class BasicProfile(BaseModel):
    id: int
    discord_id: Optional[str]
    role: str


# class MasterUserProfile(BasicProfile):
#     master_id: int

