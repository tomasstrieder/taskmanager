from datetime import datetime

from pydantic import BaseModel, field_validator

from app.schemas.user_schema import UserResponse


class CreateCommentRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: UserResponse

    model_config = {"from_attributes": True}

