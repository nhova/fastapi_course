import pytest
from jose import jwt
from app.misc.config import settings
from app.schemas.user import UserResponse, Token

def test_create_user(client):
  res = client.post("/users/", json={"email":"pops1@gmail.com", "password":"startdust"})
  new_user = UserResponse(**res.json())
  assert new_user.email == "pops1@gmail.com"
  assert res.status_code == 201

def test_login_user(client, test_user):
  res = client.post( "/login", data ={"username": test_user["email"], "password": test_user["password"]})
  valid_res = Token(**res.json())
  payload = jwt.decode(valid_res.access_token, settings.jwt_key, algorithms=[settings.jwt_alg])
  id = payload.get("user_id")
  assert id == test_user["id"]
  assert valid_res.token_type == "bearer"
  assert res.status_code == 200

@pytest.mark.parametrize( "user, passwd, status, detail", [
    ("wrongdude@gmail.com", "wrongpass", 401, "Invalid credentials"),
    ("wronguser@gmail.com", "testboypassword", 401, "Invalid credentials"),
    ("testboy@gmail.com", "wrongpass", 401, "Invalid credentials"),
    ('wrongdude@gmail.com', 'wrongpass', 401, "Invalid credentials"),
    (None, "wrongpass", 422, None),
    ("wronguser@gmail.com", None, 422, None),
    (None, None, 422, None)
  ])
def test_incorrect_login(client, test_user, user, passwd, status, detail):
  res = client.post( "/login", data ={"username": user, "password": passwd})
  assert res.status_code == status
  if detail:
    assert res.json().get("detail") == detail