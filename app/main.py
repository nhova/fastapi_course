from fastapi import FastAPI
from .database.base import init_db
from .routers.user import router as user_router
from .routers.post import router as post_router
from .routers.auth import router as auth_router

init_db()

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

@app.get("/")
def root():
  return {"message": "Here be dragons!"}

