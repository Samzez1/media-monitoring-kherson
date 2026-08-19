"""
FastAPI приложение - основной entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database import init_db, seed_national_projects, SessionLocal
from app.api import articles, projects, sources

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


# Lifespan для инициализации при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application...")
    init_db()
    
    # Заполнение Национальных проектов
    db = SessionLocal()
    try:
        seed_national_projects(db)
        logger.info("National projects seeded")
    finally:
        db.close()
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.api_title,
    description="API для мониторинга публикаций о Национальных проектах РФ в Херсонской области",
    version=settings.app_version,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Включение API маршрутов
app.include_router(articles.router, prefix=settings.api_v1_prefix)
app.include_router(projects.router, prefix=settings.api_v1_prefix)
app.include_router(sources.router, prefix=settings.api_v1_prefix)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


# Главная страница
@app.get("/")
async def root():
    """Информация об API"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "Media Monitoring Kherson API",
        "docs": f"{settings.api_v1_prefix}/docs",
        "endpoints": {
            "articles": f"{settings.api_v1_prefix}/articles",
            "projects": f"{settings.api_v1_prefix}/projects",
            "sources": f"{settings.api_v1_prefix}/sources"
        }
    }


# Обработчик исключений
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Обработчик всех исключений"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
