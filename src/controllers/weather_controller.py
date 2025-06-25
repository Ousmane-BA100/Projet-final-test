from fastapi import APIRouter, HTTPException
from typing import Optional
from src.services import weather_service

router = APIRouter()

@router.get("/weather/{city}")
async def get_weather(city: str):
    """Récupère les données météo pour une ville donnée (avec cache)"""
    try:
        return await weather_service.get_cached_weather(city)
    except Exception as e:
        # Ajouter un message d'erreur plus descriptif
        raise HTTPException(
            status_code=500,
            detail=f"Impossible de récupérer les données météo pour {city}: {str(e)}"
        )