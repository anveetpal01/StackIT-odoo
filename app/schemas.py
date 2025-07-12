from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class Tag(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    title: str
    description: str
    tag_ids: List[int]

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    tags: List[Tag]

    class Config:
        orm_mode = True

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    owner_id: int
    is_accepted: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class Notification(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# Auth
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None


class VoteCreate(BaseModel):
    answer_id: int
    value: int  # 1 for upvote, -1 for downvote

class VoteOut(BaseModel):
    answer_id: int
    votes: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    answer_id: int
    content: str

class Comment(BaseModel):
    id: int
    answer_id: int
    owner_id: int
    content: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class PlatformMessageCreate(BaseModel):
    message: str

class PlatformMessage(BaseModel):
    id: int
    message: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
