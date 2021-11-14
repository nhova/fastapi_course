from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user import router as user_router
from app.routers.post import router as post_router
from app.routers.auth import router as auth_router
from app.routers.vote import router as vote_router

CORS_ORIGINS = ["*"]

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = CORS_ORIGINS,
  allow_credentials = True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(vote_router)

@app.get("/")
def root():
  return {"message": "CI/CD BABY!!!!!!"}

