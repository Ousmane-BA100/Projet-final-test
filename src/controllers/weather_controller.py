from fastapi import APIRouter, HTTPException, status, Depends
from ..services.weather_service import WeatherService
from ..models.weather_models import WeatherData
from typing import Optional

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Non trouvé"}}
)

weather_service = WeatherService()

@router.get(
    "/current/{city}",
    response_model=WeatherData,
    summary="Obtenir la météo actuelle",
    description="Récupère les données météorologiques actuelles pour une ville donnée",
    responses={
        200: {"description": "Données météorologiques récupérées avec succès"},
        404: {"description": "Ville non trouvée"},
        503: {"description": "Service météo indisponible"}
    }
)
async def get_current_weather(city: str):
    """
    Récupère les données météorologiques actuelles pour une ville spécifique.
    
    - **city**: Nom de la ville (ex: Paris, London, New York)
    """
    return await weather_service.get_current_weather(city)