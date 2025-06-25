import asyncio
import os
from dotenv import load_dotenv
from src.services.weather_service import WeatherService

# Charger les variables d'environnement
load_dotenv(override=True)

# Afficher la clé chargée
print(f"Clé chargée: {os.getenv('WEATHERAPI_KEY')}")

async def test_weatherapi_service():
    service = WeatherService()
    try:
        print("\nTest WeatherAPI depuis le service...")
        data = await service._get_weather_from_weatherapi("Paris")
        if data:
            print(f"✓ Données reçues: {data.temperature.current}°C")
            print(f"Description: {data.weather_description}")
        else:
            print("✗ Aucune donnée reçue")
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_weatherapi_service())