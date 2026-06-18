from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependency import get_current_user
from app.database.session import get_db
from app.models.user_model import User
from app.schemas.comment_schema import CommentResponse, CreateCommentRequest
from app.services.comment_service import CommentService

router = APIRouter(tags=["Comments"])


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    task_id: int,
    payload: CreateCommentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CommentResponse:
    return CommentService.create_comment(db, task_id, current_user, payload.content)


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(
    task_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CommentResponse]:
    return CommentService.list_comments(db, task_id)


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    return CommentService.delete_comment(db, comment_id, current_user)
