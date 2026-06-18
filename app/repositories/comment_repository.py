from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment_model import Comment


class CommentRepository:
    @staticmethod
    def create(db: Session, **kwargs: dict) -> Comment:
        comment = Comment(**kwargs)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_by_id(db: Session, comment_id: int) -> Comment | None:
        return db.get(Comment, comment_id)

    @staticmethod
    def get_by_task(db: Session, task_id: int) -> list[Comment]:
        return db.execute(
            select(Comment)
            .where(Comment.task_id == task_id)
            .order_by(Comment.created_at.desc())
        ).scalars().all()

    @staticmethod
    def delete(db: Session, comment: Comment) -> None:
        db.delete(comment)
        db.commit()
