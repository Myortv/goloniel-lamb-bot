from typing import List, Any, Union, Optional

from datetime import datetime

from pydantic import BaseModel


class LnkGroupUser(BaseModel):
    user_id: int
    squad_id: int
    created_at: datetime


class LnkGroupUserCreate(BaseModel):
    user_id: int
    squad_id: int


class GroupJoinRequestInDB(BaseModel):
    id: int
    user_id: int
    squad_id: int
    state: Optional[str] = None
    is_accepted: bool
    created_at: datetime


class GroupJoinRequestCreate(BaseModel):
    user_id: int
    squad_id: int


class GroupJoinRequestUpdate(BaseModel):
    state: Optional[str]
    is_accepted: Optional[bool] = False


# class GroupMembershipRequestCreate(BaseModel):
#     squad_id: int

# class lnkGroupUserInDB(BaseModel):
#     user_id: int
#     squad_id: int
#     created_at: datetime
