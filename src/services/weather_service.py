import httpx
from typing import Optional, Dict, Any
from ..models.weather_models import WeatherData, Temperature
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

class WeatherService:
    def __init__(self):
        self.open_meteo_url = os.getenv("OPENMETEO_URL", "https://api.open-meteo.com/v1")
        self.timeout = 10.0

    async def _get_coordinates(self, city: str) -> Dict[str, float]:
        """Convertit un nom de ville en coordonnées géographiques"""
        # Pour simplifier, nous utilisons des coordonnées fixes
        # En production, utilisez un service de géocodage comme Nominatim
        coordinates = {
            "paris": {"lat": 48.8566, "lon": 2.3522},
            "london": {"lat": 51.5074, "lon": -0.1278},
            "new york": {"lat": 40.7128, "lon": -74.0060},
            "tokyo": {"lat": 35.6762, "lon": 139.6503},
        }
        
        city_lower = city.lower()
        if city_lower not in coordinates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coordonnées non trouvées pour la ville: {city}"
            )
        return coordinates[city_lower]

    async def get_current_weather(self, city: str) -> WeatherData:
        """Récupère les données météorologiques actuelles pour une ville donnée"""
        try:
            # Obtenir les coordonnées de la ville
            coords = await self._get_coordinates(city)
            
            # Paramètres de la requête
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,weather_code",
                "timezone": "auto"
            }
            
            # Faire la requête à l'API Open-Meteo
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.open_meteo_url}/forecast",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
            current = data.get("current", {})
            
            # Convertir le code météo en description lisible
            weather_codes = {
                0: "Ciel dégagé",
                1: "Principalement clair",
                2: "Partiellement nuageux",
                3: "Couvert",
                45: "Brouillard",
                48: "Brouillard givrant",
                51: "Bruine légère",
                53: "Bruine modérée",
                55: "Bruine dense",
                56: "Bruine verglaçante légère",
                57: "Bruine verglaçante dense",
                61: "Pluie légère",
                63: "Pluie modérée",
                65: "Pluie forte",
                66: "Pluie verglaçante légère",
                67: "Pluie verglaçante forte",
                71: "Chute de neige légère",
                73: "Chute de neige modérée",
                75: "Chute de neige forte",
                77: "Grains de neige",
                80: "Averses de pluie légères",
                81: "Averses de pluie modérées",
                82: "Averses de pluie violentes",
                85: "Averses de neige légères",
                86: "Averses de neige fortes",
                95: "Orage modéré ou fort",
                96: "Orage avec grêle légère",
                99: "Orage avec grêle forte"
            }
            
            weather_code = current.get("weather_code", 0)
            description = weather_codes.get(weather_code, "Inconnu")
            
            return WeatherData(
                city=city.capitalize(),
                temperature=Temperature(
                    current=current.get("temperature_2m", 0),
                    feels_like=current.get("temperature_2m", 0)  # Open-Meteo ne fournit pas cette donnée
                ),
                humidity=current.get("relative_humidity_2m", 0),
                wind_speed=current.get("wind_speed_10m", 0),
                wind_direction=current.get("wind_direction_10m", 0),
                weather_description=description,
                source="open-meteo"
            )
                
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erreur lors de l'appel à l'API météo: {str(e)}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Impossible de se connecter au service météo: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur inattendue: {str(e)}"
            )