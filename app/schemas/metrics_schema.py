from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    tasks_per_user: dict[str, int]
    average_completion_time_days: float | None
