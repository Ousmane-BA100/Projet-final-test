import os
from dotenv import load_dotenv

print("Avant load_dotenv():")
print(f"OPENWEATHER_API_KEY: {os.getenv('OPENWEATHER_API_KEY')}")
print(f"WEATHERAPI_KEY: {os.getenv('WEATHERAPI_KEY')}")

load_dotenv(override=True)  # Force le rechargement

print("\nAprès load_dotenv():")
print(f"OPENWEATHER_API_KEY: {os.getenv('OPENWEATHER_API_KEY')}")
print(f"WEATHERAPI_KEY: {os.getenv('WEATHERAPI_KEY')}")