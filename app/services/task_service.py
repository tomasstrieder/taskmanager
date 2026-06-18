import logging
from datetime import date

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.task_model import TaskPriority, TaskStatus
from app.models.user_model import User
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task_schema import TaskResponse

logger = logging.getLogger(__name__)


class TaskService:
    @staticmethod
    def create_task(db: Session, current_user: User, title: str, **data: dict) -> TaskResponse:
        if data.get("assigned_to"):
            assigned_user = UserRepository.get_by_id(db, data["assigned_to"])
            if not assigned_user or not assigned_user.is_active:
                raise NotFoundError("Assigned user not found")
        task = TaskRepository.create(db, title=title, created_by=current_user.id, **data)
        logger.info("Task created id=%s by user id=%s", task.id, current_user.id)
        return TaskResponse.model_validate(task)

    @staticmethod
    def get_task(db: Session, task_id: int) -> TaskResponse:
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError("Task not found")
        return TaskResponse.model_validate(task)

    @staticmethod
    def list_tasks(
        db: Session,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assigned_to: int | None = None,
        due_before: date | None = None,
        due_after: date | None = None,
    ) -> list[TaskResponse]:
        tasks = TaskRepository.list_tasks(
            db,
            status=status,
            priority=priority,
            assigned_to=assigned_to,
            due_before=due_before,
            due_after=due_after,
        )
        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    def update_task(
        db: Session, task_id: int, current_user: User, **updates: dict
    ) -> TaskResponse:
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError("Task not found")
        if task.created_by != current_user.id:
            logger.warning("User id=%s attempted to update task id=%s", current_user.id, task_id)
            raise PermissionDeniedError("Cannot update task you didn't create")
        if "assigned_to" in updates and updates["assigned_to"]:
            assigned_user = UserRepository.get_by_id(db, updates["assigned_to"])
            if not assigned_user or not assigned_user.is_active:
                raise NotFoundError("Assigned user not found")
        updated_task = TaskRepository.update(db, task, **updates)
        logger.info("Task updated id=%s by user id=%s", task_id, current_user.id)
        return TaskResponse.model_validate(updated_task)

    @staticmethod
    def delete_task(db: Session, task_id: int, current_user: User) -> dict:
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError("Task not found")
        if task.created_by != current_user.id:
            logger.warning("User id=%s attempted to delete task id=%s", current_user.id, task_id)
            raise PermissionDeniedError("Cannot delete task you didn't create")
        TaskRepository.delete(db, task)
        logger.info("Task deleted id=%s by user id=%s", task_id, current_user.id)
        return {"message": "Task deleted successfully"}
