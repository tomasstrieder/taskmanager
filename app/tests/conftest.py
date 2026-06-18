import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401 — registers all models with Base.metadata
from app.core.config import settings
from app.database.base import Base
from app.database.session import get_db
from app.main import app

TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/taskmanager_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE comments, tasks, users RESTART IDENTITY CASCADE"))
        conn.commit()


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user_payload():
    return {"name": "User1", "email": "user1@test.com", "password": "123456"}


@pytest.fixture
def user2_payload():
    return {"name": "User2", "email": "user2@test.com", "password": "123456"}


@pytest.fixture
def created_user(client, user_payload):
    res = client.post("/users", json=user_payload)
    assert res.status_code == 201
    return res.json()


@pytest.fixture
def created_user2(client, user2_payload):
    res = client.post("/users", json=user2_payload)
    assert res.status_code == 201
    return res.json()


@pytest.fixture
def token(client, created_user, user_payload):
    res = client.post("/auth/login", json={
        "email": user_payload["email"],
        "password": user_payload["password"],
    })
    return res.json()["access_token"]


@pytest.fixture
def token2(client, created_user2, user2_payload):
    res = client.post("/auth/login", json={
        "email": user2_payload["email"],
        "password": user2_payload["password"],
    })
    return res.json()["access_token"]


@pytest.fixture
def headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def headers2(token2):
    return {"Authorization": f"Bearer {token2}"}


@pytest.fixture
def created_task(client, headers):
    res = client.post("/tasks", json={"title": "Test Task", "status": "todo"}, headers=headers)
    assert res.status_code == 201
    return res.json()


@pytest.fixture
def created_comment(client, headers, created_task):
    res = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"content": "Test comment"},
        headers=headers,
    )
    assert res.status_code == 201
    return res.json()
