from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependency import get_current_user
from app.database.session import get_db
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and receive a JWT token",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return AuthService.login(db, payload.email, payload.password)


@router.post(
    "/logout",
    summary="Invalidate current session (symbolic)",
)
def logout(_: User = Depends(get_current_user)) -> dict[str, str]:
    return {"message": "Successfully logged out"}
