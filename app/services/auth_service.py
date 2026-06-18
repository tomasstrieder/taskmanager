import logging

from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import TokenResponse

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def login(db: Session, email: str, password: str) -> TokenResponse:
        logger.info("Login attempt for email: %s", email)
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning("Failed login attempt for email: %s", email)
            raise AuthenticationError("Invalid credentials")
        if not user.is_active:
            logger.warning("Login attempt by inactive user id=%s", user.id)
            raise PermissionDeniedError("Inactive user")
        token = create_access_token(data={"sub": str(user.id)})
        logger.info("Successful login for user id=%s", user.id)
        return TokenResponse(access_token=token)
