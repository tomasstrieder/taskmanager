from datetime import date, datetime

from pydantic import BaseModel

from app.models.task_model import TaskPriority, TaskStatus
from app.schemas.comment_schema import CommentResponse
from app.schemas.user_schema import UserResponse


class CreateTaskRequest(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: date | None = None
    assigned_to: int | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None
    assigned_to: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    creator: UserResponse
    assignee: UserResponse | None
    comments: list[CommentResponse]

    model_config = {"from_attributes": True}
