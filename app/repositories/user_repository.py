from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User


class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    @staticmethod
    def exists_by_email(db: Session, email: str) -> bool:
        return (
            db.execute(select(User).where(User.email == email)).scalar_one_or_none()
            is not None
        )

    @staticmethod
    def create(db: Session, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session, user: User, **updates: dict) -> User:
        for key, value in updates.items():
            if value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(db: Session, user: User) -> User:
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

