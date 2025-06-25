from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers.weather_controller import router as weather_router
from .routers.cache_router import router as cache_router  # Ajoutez cette ligne
from datetime import datetime  # Ajoutez cette ligne

app = FastAPI(
    title="API Météo",
    description="API d'agrégation de données météorologiques",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(weather_router)
app.include_router(cache_router, prefix="/api")  # Ajoutez cette ligne

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Bienvenue sur l'API Météo",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Vérifie l'état de l'API"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}