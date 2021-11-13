import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.misc.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import get_db
from app.database.base import Base
from pytest import fixture

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
  user_data = { "email": "testboy@gmail.com",
                "password": "testboypassword" }
  res = client.post("/users/", json = user_data )
  new_user = res.json()
  new_user['password'] = user_data['password']
  return new_user