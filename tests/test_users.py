from jose import jwt
from app.misc.config import settings
from app.schemas.user import UserResponse, Token
#from tests.database import client, session


## Basic test no DB ##
# def test_root(client):
#   res = client.get("/")
#   assert res.json().get('message') == 'Here be many dragons!!!!!'
#   assert res.status_code == 200



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