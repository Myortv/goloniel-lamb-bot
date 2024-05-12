from typing import Optional, List
from datetime import datetime


from pydantic import BaseModel


class Group(BaseModel):
    id: int
    master_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    created_at: datetime
    user_profiles_id: Optional[List[int]] = None
    messages: Optional[dict] = None
    is_full: bool

    def __str__(self):
        return (
            f'id: {self.id} '
            f'master_id: {self.master_id}'
            f'title: {self.title} '
            f'description: {self.description} '
            f'created: {self.created_at} '
        )


class GroupUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    is_full: bool
