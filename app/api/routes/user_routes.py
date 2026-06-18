from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependency import get_current_user
from app.database.session import get_db
from app.models.user_model import User
from app.schemas.user_schema import CreateUserRequest, UpdateUserRequest, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: CreateUserRequest, db: Session = Depends(get_db)
) -> UserResponse:
    return UserService.create_user(db, payload.name, payload.email, payload.password)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserService.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserService.update_user(
        db, user_id, current_user, **payload.model_dump(exclude_unset=True)
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    return UserService.delete_user(db, user_id, current_user)
