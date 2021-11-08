from pydantic import BaseSettings

class Settings(BaseSettings):
  db_host: str
  db_port: str
  db_name: str
  db_user: str
  db_pass: str 
  jwt_key: str
  jwt_alg: str
  jwt_exp: int

  class Config:
    env_file = ".env"

settings = Settings()