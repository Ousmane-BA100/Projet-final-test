from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.weather_controller import router as weather_router
from src.routers.cache_router import router as cache_router
from src.monitoring import setup_logging, setup_metrics, add_health_check
from src.config.redis import init_redis, get_redis
import logging
import os

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Démarrage
    try:
        redis = await init_redis()
        logger.info("✅ Connecté à Redis avec succès")
        yield
    except Exception as e:
        logger.error(f"❌ Erreur de connexion à Redis: {str(e)}")
        raise
    finally:
        # Arrêt
        try:
            if 'redis' in locals():
                await redis.aclose()  # Utilisation de aclose() au lieu de close()
                logger.info("Connexion Redis fermée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture de Redis: {str(e)}")

app = FastAPI(
    title="API Météo",
    description="API d'agrégation de données météorologiques",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Utilisation du gestionnaire de cycle de vie moderne
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
app.include_router(weather_router, prefix="/api")
app.include_router(cache_router, prefix="/api")

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Bienvenue sur l'API Météo",
        "documentation": "/docs",
        "health_check": "/health",
        "status": "ok"
    }