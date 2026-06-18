import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.user_model import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.comment_schema import CommentResponse

logger = logging.getLogger(__name__)


class CommentService:
    @staticmethod
    def create_comment(
        db: Session, task_id: int, current_user: User, content: str
    ) -> CommentResponse:
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError("Task not found")
        comment = CommentRepository.create(
            db, task_id=task_id, user_id=current_user.id, content=content
        )
        logger.info(
            "Comment created id=%s on task id=%s by user id=%s",
            comment.id, task_id, current_user.id,
        )
        return CommentResponse.model_validate(comment)

    @staticmethod
    def list_comments(db: Session, task_id: int) -> list[CommentResponse]:
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError("Task not found")
        comments = CommentRepository.get_by_task(db, task_id)
        return [CommentResponse.model_validate(comment) for comment in comments]

    @staticmethod
    def delete_comment(db: Session, comment_id: int, current_user: User) -> dict:
        comment = CommentRepository.get_by_id(db, comment_id)
        if not comment:
            raise NotFoundError("Comment not found")
        if comment.user_id != current_user.id:
            logger.warning(
                "User id=%s attempted to delete comment id=%s",
                current_user.id, comment_id,
            )
            raise PermissionDeniedError("Cannot delete another user's comment")
        CommentRepository.delete(db, comment)
        logger.info("Comment deleted id=%s by user id=%s", comment_id, current_user.id)
        return {"message": "Comment deleted successfully"}
