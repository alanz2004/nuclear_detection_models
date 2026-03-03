from fastapi import APIRouter, HTTPException
from app.services.model_manager import model_manager

router = APIRouter(prefix="/models", tags=["models"])

# ==============================
# List all available models
# ==============================
@router.get("/")
async def list_models():
    models = model_manager.list_models()
    return {"available_models": models}

# ==============================
# Get info for a specific model by name
# ==============================
@router.get("/{model_name}")
async def get_model_info(model_name: str):
    info = model_manager.get_info_by_name(model_name)
    if not info:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")
    return info

# ==============================
# Get info for all models (full JSON objects)
# ==============================
@router.get("/all/info")
async def get_all_models_info():
    all_infos = model_manager.get_all_infos()  # returns list of JSON info dicts
    if not all_infos:
        raise HTTPException(status_code=404, detail="No model info available.")
    return {"models_info": all_infos}