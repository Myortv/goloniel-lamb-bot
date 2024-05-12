from typing import Optional

from pydantic import BaseModel


class Master(BaseModel):
    id: int
    user_id: int
    is_approved: Optional[bool] = False

    title: str
    description: Optional[str] = None
    cover_picture: Optional[str] = None
    user_id: int
    rating: Optional[float] = 0
    approvals_amount: Optional[int] = 0


class MasterCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_picture: Optional[str] = None
    user_id: int
    is_approved: Optional[bool] = False
    approvals_amount: Optional[int] = 0


class MasterUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_picture: Optional[str] = None
    user_id: int
    is_approved: Optional[bool] = False
    approvals_amount: Optional[int] = 0

# class AdminMasterUpdate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     cover_picture: Optional[str] = None
#     user_id: int
#     is_approved: Optional[bool] = False
#     approvals_amount: Optional[int] = 0
