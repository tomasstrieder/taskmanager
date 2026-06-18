from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependency import get_current_user
from app.database.session import get_db
from app.models.task_model import TaskPriority, TaskStatus
from app.models.user_model import User
from app.schemas.task_schema import CreateTaskRequest, TaskResponse, UpdateTaskRequest
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    return TaskService.create_task(db, current_user, **payload.model_dump())


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    return TaskService.get_task(db, task_id)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    task_status: TaskStatus | None = Query(None, alias="status"),
    priority: TaskPriority | None = Query(None),
    assigned_to: int | None = Query(None, alias="assignedTo"),
    due_before: date | None = Query(None, alias="dueBefore"),
    due_after: date | None = Query(None, alias="dueAfter"),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
    return TaskService.list_tasks(
        db,
        status=task_status,
        priority=priority,
        assigned_to=assigned_to,
        due_before=due_before,
        due_after=due_after,
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: UpdateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    return TaskService.update_task(
        db, task_id, current_user, **payload.model_dump(exclude_unset=True)
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    return TaskService.delete_task(db, task_id, current_user)
