import logging

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, PermissionDeniedError
from app.core.security import hash_password
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(db: Session, name: str, email: str, password: str) -> UserResponse:
        if UserRepository.exists_by_email(db, email):
            logger.warning("Registration attempt with duplicate email: %s", email)
            raise ConflictError("Email already registered")
        hashed_password = hash_password(password)
        user = UserRepository.create(db, name, email, hashed_password)
        logger.info("User created id=%s email=%s", user.id, user.email)
        return UserResponse.model_validate(user)

    @staticmethod
    def get_user(db: Session, user_id: int) -> UserResponse:
        user = UserRepository.get_by_id(db, user_id)
        if not user or not user.is_active:
            raise NotFoundError("User not found")
        return UserResponse.model_validate(user)

    @staticmethod
    def update_user(
        db: Session, user_id: int, current_user: User, **updates: dict
    ) -> UserResponse:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        if user.id != current_user.id:
            logger.warning("User id=%s attempted to update user id=%s", current_user.id, user_id)
            raise PermissionDeniedError("Cannot update another user's profile")
        if "email" in updates and updates["email"]:
            if updates["email"] != user.email and UserRepository.exists_by_email(db, updates["email"]):
                raise ConflictError("Email already registered")
        if "password" in updates and updates["password"]:
            updates["hashed_password"] = hash_password(updates["password"])
            del updates["password"]
        updated_user = UserRepository.update(db, user, **updates)
        logger.info("User updated id=%s", user_id)
        return UserResponse.model_validate(updated_user)

    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> dict:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        if user.id != current_user.id:
            logger.warning("User id=%s attempted to delete user id=%s", current_user.id, user_id)
            raise PermissionDeniedError("Cannot delete another user's profile")
        UserRepository.soft_delete(db, user)
        logger.info("User soft-deleted id=%s", user_id)
        return {"message": "User deleted successfully"}
