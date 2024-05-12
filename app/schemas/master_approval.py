from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class Approval(BaseModel):
    user_id: int
    master_id: int
    created_at: datetime


class ApprovalCreate(BaseModel):
    user_id: int
    master_id: int


class ApprovalRequest(BaseModel):
    master_id: int
    state: Optional[str]
    reason: Optional[str]
    created_at: datetime


class ApprovalRequestCreate(BaseModel):
    master_id: int
    # state: Optional[str]
    # reason: Optional[str]
    # created_at: datetime

# class ApprovalRequestUpdateByAdmin(BaseModel):
#     state: Optional[str]
#     reason: Optional[str]
