from fastapi import APIRouter, HTTPException
from src.services import weather_service

router = APIRouter(tags=["Cache"])

@router.post("/cache/clear", summary="Vider le cache")
async def clear_cache():
    """Vide le cache des données météo"""
    try:
        await weather_service.clear_cache()
        return {"status": "success", "message": "Cache vidé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))