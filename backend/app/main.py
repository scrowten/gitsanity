import logging
import time
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app.config import settings
from app.database import AsyncSessionLocal
from app.limiter import limiter
from app.routers import auth, feed, saved

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


async def _check_db() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    logger.info("Starting %s…", settings.app_name)
    try:
        await _check_db()
        logger.info("Database connection OK")
    except Exception as exc:
        logger.critical("Database connection FAILED: %s", exc)
        raise RuntimeError("Cannot connect to database — check DATABASE_URL") from exc
    yield
    # Shutdown (nothing to clean up currently)
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="Personalized GitHub repository discovery platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

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


@app.middleware("http")
async def log_requests(request: Request, call_next: object) -> Response:
    start = time.perf_counter()
    response: Response = await call_next(request)  # type: ignore[operator]
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s → %d (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.app_name}
