from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers.weather_controller import router as weather_router
from .routers.cache_router import router as cache_router
from .monitoring import setup_logging, setup_metrics, add_health_check
from .config.redis import init_redis, get_redis
import logging
import os

logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Météo",
    description="API d'agrégation de données météorologiques",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration
setup_logging()
setup_metrics(app)
add_health_check(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(weather_router)
app.include_router(cache_router, prefix="/api")

# Gestion du cycle de vie
@app.on_event("startup")
async def startup_event():
    try:
        await init_redis()
        logger.info("✅ Connecté à Redis avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur de connexion à Redis: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    try:
        redis = await get_redis()
        if redis:
            await redis.close()
            logger.info("Connexion Redis fermée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la fermeture de Redis: {str(e)}")

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Bienvenue sur l'API Météo",
        "documentation": "/docs",
        "health_check": "/health",
        "status": "ok"
    }