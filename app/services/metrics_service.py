from sqlalchemy.orm import Session

from app.repositories.metrics_repository import MetricsRepository
from app.schemas.metrics_schema import MetricsResponse


class MetricsService:
    @staticmethod
    def get_metrics(db: Session) -> MetricsResponse:
        counts = MetricsRepository.count_by_status(db)
        tasks_per_user = MetricsRepository.count_per_user(db)
        avg_completion = MetricsRepository.average_completion_time_days(db)

        return MetricsResponse(
            total_tasks=sum(counts.values()),
            completed_tasks=counts.get("done", 0),
            pending_tasks=counts.get("todo", 0),
            in_progress_tasks=counts.get("in_progress", 0),
            tasks_per_user=tasks_per_user,
            average_completion_time_days=avg_completion,
        )
