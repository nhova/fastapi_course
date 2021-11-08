from fastapi import FastAPI

from app.database.base import init_db
from app.routers.user import router as user_router
from app.routers.post import router as post_router
from app.routers.auth import router as auth_router

init_db()

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

@app.get("/")
def root():
  return {"message": "Here be dragons!"}

