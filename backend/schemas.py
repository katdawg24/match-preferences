from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import date as Date

# region Auth, tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class HashedPassword(BaseModel):
     hashed_password: str

# endregion


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    password: str
    num_preferences: int
    direct_matches: bool
    additional_prefs_allowed: bool = False

class GroupUpdate(GroupBase):
    name: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None
    num_preferences: Optional[int] = None
    direct_matches: Optional[bool] = None
    additional_prefs_allowed: Optional[bool] = None

class GroupToReturn(GroupBase):
    id: int
    num_preferences: int
    direct_matches: bool
    additional_prefs_allowed: bool = False
    match_complete: bool = False
    match_date: Optional[Date] = None
    is_deleted: bool = False

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    group_ids: List[int] = []
    is_admin: bool

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    group_ids: Optional[List[int]] = None
    is_admin: Optional[bool] = None
    is_deleted: Optional[bool] = None

class UserToReturn(UserBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True

class GroupMemberBase(BaseModel):
    group_id: int
    group_member_id: int
    account_id: int

class GroupMemberCreate(GroupMemberBase):
    group_id: int
    group_member_id: int
    account_id: int

class GroupMemberUpdate(GroupMemberBase):
    group_id: Optional[int] = None
    group_member_id: Optional[int] = None
    account_id: Optional[int] = None
    is_deleted: Optional[bool] = None

class GroupMemberToReturn(GroupMemberBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    group_id: int
    name: str
    description: Optional[str] = None
    group_task_id: int
    min_assignment_count: int
    max_assignment_count: int

class TaskCreate(TaskBase):
    group_id: int
    name: str
    description: Optional[str] = None
    group_task_id: int
    min_assignment_count: int
    max_assignment_count: int

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    group_task_id: Optional[int] = None
    min_assignment_count: Optional[int] = None
    max_assignment_count: Optional[int] = None

class TaskToReturn(TaskBase):
    id: int

    class Config:
        from_attributes = True

class TaskPreferenceBase(BaseModel):
    task_id: int
    member_id: int
    rank: int

class TaskPreferenceCreate(TaskPreferenceBase):
    task_id: int
    member_id: int
    rank: int

class TaskPreferenceUpdate(TaskPreferenceBase):
    task_id: Optional[int] = None
    member_id: Optional[int] = None
    rank: Optional[int] = None

class TaskPreferenceToReturn(TaskPreferenceBase):
    id: int

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    task_id: int
    member_id: int

class MatchCreate(MatchBase):
    task_id: int
    member_id: int

class MatchToReturn(MatchBase):
    id: int
    match_date: Optional[Date] = None
    is_deleted: bool = False

    class Config:
        from_attributes = True
