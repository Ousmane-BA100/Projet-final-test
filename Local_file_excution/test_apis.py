import asyncio
import os
from dotenv import load_dotenv
from src.services.weather_service import WeatherService

# Charger les variables d'environnement
load_dotenv(override=True)

# Afficher un aperçu des clés chargées
def get_key_preview(key: str) -> str:
    if not key:
        return "NON DÉFINIE"
    return f"{key[:3]}...{key[-3:]}" if len(key) > 6 else "******"

print("Configuration des clés API :")
print(f"OpenWeather: {get_key_preview(os.getenv('OPENWEATHER_API_KEY'))}")
print(f"WeatherAPI: {get_key_preview(os.getenv('WEATHERAPI_KEY'))}")

async def main():
    service = WeatherService()
    await service.test_apis()

if __name__ == "__main__":
    asyncio.run(main())