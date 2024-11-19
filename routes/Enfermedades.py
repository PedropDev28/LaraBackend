from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Enfermedades import Enfermedades

router = APIRouter()

@router.get("/", response_model=List[Enfermedades])
async def get_enfermedades():
    enfermedades = await db["enfermedades"].find().to_list(100)
    return enfermedades

@router.post("/", response_model=Enfermedades)
async def create_enfermedades(enfermedades: Enfermedades):
    result = await db["enfermedades"].insert_one(enfermedades.model_dump(by_alias=True))
    enfermedades.id = str(result.inserted_id)
    return enfermedades

@router.get("/{enfermedades_id}", response_model=Enfermedades)
async def get_enfermedades(enfermedades_id: str):
    enfermedades = await db["enfermedades"].find_one({"_id": ObjectId(enfermedades_id)})
    if not enfermedades:
        raise HTTPException(status_code=404, detail="Enfermedad no encontrada")
    return enfermedades

@router.put("/{enfermedades_id}", response_model=Enfermedades)
async def update_enfermedades(enfermedades_id: str, enfermedades: Enfermedades):
    result = await db["enfermedades"].update_one(
        {"_id": ObjectId(enfermedades_id)}, {"$set": enfermedades.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Enfermedad no encontrada")
    enfermedades.id = enfermedades_id
    return enfermedades

@router.delete("/{enfermedades_id}")
async def delete_enfermedades(enfermedades_id: str):
    result = await db["enfermedades"].delete_one({"_id": ObjectId(enfermedades_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enfermedad no encontrada")
    return {"message": "Enfermedad eliminada"}