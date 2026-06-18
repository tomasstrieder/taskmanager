from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task_model import Task, TaskPriority, TaskStatus


class TaskRepository:
    @staticmethod
    def create(db: Session, **kwargs: dict) -> Task:
        task = Task(**kwargs)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Task | None:
        return db.get(Task, task_id)

    @staticmethod
    def list_tasks(
        db: Session,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assigned_to: int | None = None,
        due_before: date | None = None,
        due_after: date | None = None,
    ) -> list[Task]:
        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if assigned_to is not None:
            query = query.where(Task.assigned_to == assigned_to)
        if due_before:
            query = query.where(Task.due_date <= due_before)
        if due_after:
            query = query.where(Task.due_date >= due_after)
        return db.execute(query).scalars().all()

    @staticmethod
    def update(db: Session, task: Task, **updates: dict) -> Task:
        for key, value in updates.items():
            if value is not None:
                setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task: Task) -> None:
        db.delete(task)
        db.commit()
