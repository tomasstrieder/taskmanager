from sqlalchemy import delete

from app.database.session import SessionLocal
from app.models.comment_model import Comment
from app.models.task_model import Task
from app.models.user_model import User

db = SessionLocal()

try:
    db.execute(delete(Comment))
    db.execute(delete(Task))
    db.execute(delete(User))
    db.commit()
    print("Cleared all comments, tasks, and users.")

finally:
    db.close()
