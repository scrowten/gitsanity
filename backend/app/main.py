from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, feed, saved

app = FastAPI(
    title=settings.app_name,
    description="Personalized GitHub repository discovery platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(feed.router)
app.include_router(saved.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.app_name}
