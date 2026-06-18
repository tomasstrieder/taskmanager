from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.task_model import Task, TaskStatus
from app.models.user_model import User


class MetricsRepository:
    @staticmethod
    def count_by_status(db: Session) -> dict[str, int]:
        rows = db.execute(
            select(Task.status, func.count(Task.id).label("count")).group_by(Task.status)
        ).all()
        return {row.status.value: row.count for row in rows}

    @staticmethod
    def count_per_user(db: Session) -> dict[str, int]:
        rows = db.execute(
            select(User.name, func.count(Task.id).label("count"))
            .join(Task, Task.created_by == User.id)
            .group_by(User.name)
        ).all()
        return {row.name: row.count for row in rows}

    @staticmethod
    def average_completion_time_days(db: Session) -> float | None:
        result = db.execute(
            select(
                func.avg(
                    extract("epoch", Task.updated_at - Task.created_at) / 86400
                )
            ).where(Task.status == TaskStatus.done)
        ).scalar()
        return float(result) if result is not None else None
