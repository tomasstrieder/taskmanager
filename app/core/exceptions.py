class NotFoundError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class PermissionDeniedError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class AuthenticationError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
