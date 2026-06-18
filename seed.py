from datetime import date

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.comment_model import Comment
from app.models.task_model import Task, TaskPriority, TaskStatus
from app.models.user_model import User, UserRole

db = SessionLocal()

user1 = User(name="User1", email="user1@test.com", hashed_password=hash_password("123456"), role=UserRole.user)
user2 = User(name="User2", email="user2@test.com", hashed_password=hash_password("123456"), role=UserRole.user)
user3 = User(name="User3", email="user3@test.com", hashed_password=hash_password("123456"), role=UserRole.user)
db.add(user1)
db.add(user2)
db.add(user3)
db.commit()
db.refresh(user1)
db.refresh(user2)
db.refresh(user3)
print(f"Created user1 id={user1.id}, user2 id={user2.id}, user3 id={user3.id}")

task1 = Task(title="Task1", description="Description1", status=TaskStatus.todo,        priority=TaskPriority.low,    created_by=user1.id, assigned_to=user2.id, due_date=date(2026,  7,  1))
task2 = Task(title="Task2", description="Description2", status=TaskStatus.in_progress, priority=TaskPriority.medium, created_by=user1.id, assigned_to=user3.id, due_date=date(2026,  7, 1))
task3 = Task(title="Task3", description="Description3", status=TaskStatus.done,        priority=TaskPriority.high,   created_by=user1.id, assigned_to=user1.id, due_date=date(2026,  7,  1))
task4 = Task(title="Task4", description="Description4", status=TaskStatus.todo,        priority=TaskPriority.medium, created_by=user2.id, assigned_to=user3.id, due_date=date(2026,  7, 1))
task5 = Task(title="Task5", description="Description5", status=TaskStatus.in_progress, priority=TaskPriority.high,   created_by=user2.id, assigned_to=user1.id, due_date=date(2026,  7,  1))
task6 = Task(title="Task6", description="Description6", status=TaskStatus.done,        priority=TaskPriority.low,    created_by=user2.id, assigned_to=user2.id, due_date=date(2026,  7, 1))
task7 = Task(title="Task7", description="Description7", status=TaskStatus.todo,        priority=TaskPriority.high,   created_by=user3.id, assigned_to=user1.id, due_date=date(2026, 7,  1))
task8 = Task(title="Task8", description="Description8", status=TaskStatus.in_progress, priority=TaskPriority.low,    created_by=user3.id, assigned_to=user2.id, due_date=date(2026, 7, 1))
task9 = Task(title="Task9", description="Description9", status=TaskStatus.done,        priority=TaskPriority.medium, created_by=user3.id, assigned_to=user3.id, due_date=date(2026, 7,  1))
db.add(task1); db.add(task2); db.add(task3)
db.add(task4); db.add(task5); db.add(task6)
db.add(task7); db.add(task8); db.add(task9)
db.commit()
db.refresh(task1); db.refresh(task2); db.refresh(task3)
db.refresh(task4); db.refresh(task5); db.refresh(task6)
db.refresh(task7); db.refresh(task8); db.refresh(task9)
print(f"Created 9 tasks")

db.add(Comment(task_id=task1.id, user_id=user1.id, content="Comment1"))
db.add(Comment(task_id=task1.id, user_id=user2.id, content="Comment2"))
db.add(Comment(task_id=task1.id, user_id=user3.id, content="Comment3"))

db.add(Comment(task_id=task2.id, user_id=user2.id, content="Comment1"))
db.add(Comment(task_id=task2.id, user_id=user3.id, content="Comment2"))
db.add(Comment(task_id=task2.id, user_id=user1.id, content="Comment3"))

db.add(Comment(task_id=task3.id, user_id=user3.id, content="Comment1"))
db.add(Comment(task_id=task3.id, user_id=user1.id, content="Comment2"))
db.add(Comment(task_id=task3.id, user_id=user2.id, content="Comment3"))

db.add(Comment(task_id=task4.id, user_id=user1.id, content="Comment1"))
db.add(Comment(task_id=task4.id, user_id=user2.id, content="Comment2"))
db.add(Comment(task_id=task4.id, user_id=user3.id, content="Comment3"))

db.add(Comment(task_id=task5.id, user_id=user2.id, content="Comment1"))
db.add(Comment(task_id=task5.id, user_id=user3.id, content="Comment2"))
db.add(Comment(task_id=task5.id, user_id=user1.id, content="Comment3"))

db.add(Comment(task_id=task6.id, user_id=user3.id, content="Comment1"))
db.add(Comment(task_id=task6.id, user_id=user1.id, content="Comment2"))
db.add(Comment(task_id=task6.id, user_id=user2.id, content="Comment3"))

db.add(Comment(task_id=task7.id, user_id=user1.id, content="Comment1"))
db.add(Comment(task_id=task7.id, user_id=user2.id, content="Comment2"))
db.add(Comment(task_id=task7.id, user_id=user3.id, content="Comment3"))

db.add(Comment(task_id=task8.id, user_id=user2.id, content="Comment1"))
db.add(Comment(task_id=task8.id, user_id=user3.id, content="Comment2"))
db.add(Comment(task_id=task8.id, user_id=user1.id, content="Comment3"))

db.add(Comment(task_id=task9.id, user_id=user3.id, content="Comment1"))
db.add(Comment(task_id=task9.id, user_id=user1.id, content="Comment2"))
db.add(Comment(task_id=task9.id, user_id=user2.id, content="Comment3"))

db.commit()
print("Created 27 comments")

db.close()
print("\nDone. Seed complete.")
