import asyncio
import os
from src.services.weather_service import WeatherService
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(override=True)

# Afficher la clé chargée (pour débogage)
print(f"Clé chargée: {os.getenv('OPENWEATHER_API_KEY')}")

async def test_openweather_service():
    service = WeatherService()
    try:
        print("\nTest OpenWeatherMap depuis le service...")
        data = await service._get_weather_from_openweather("Paris")
        if data:
            print(f"✓ Données reçues: {data.temperature.current}°C")
            print(f"Description: {data.weather_description}")
        else:
            print("✗ Aucune donnée reçue")
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openweather_service())