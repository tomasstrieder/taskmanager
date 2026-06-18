from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependency import get_current_user
from app.database.session import get_db
from app.models.user_model import User
from app.schemas.metrics_schema import MetricsResponse
from app.services.metrics_service import MetricsService

router = APIRouter(tags=["Metrics"])


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MetricsResponse:
    return MetricsService.get_metrics(db)
