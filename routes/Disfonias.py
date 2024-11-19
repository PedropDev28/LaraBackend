from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Disfonias import Disfonias


router = APIRouter()

@router.get("/", response_model=List[Disfonias])
async def get_disfonias():
    disfonias = await db["disfonias"].find().to_list(100)
    return disfonias

@router.post("/", response_model=Disfonias)
async def create_disfonias(disfonias: Disfonias):
    result = await db["disfonias"].insert_one(disfonias.model_dump(by_alias=True))
    disfonias.id = str(result.inserted_id)
    return disfonias

@router.get("/{disfonias_id}", response_model=Disfonias)
async def get_disfonias(disfonias_id: str):
    disfonias = await db["disfonias"].find_one({"_id": ObjectId(disfonias_id)})
    if not disfonias:
        raise HTTPException(status_code=404, detail="Disfonia no encontrado")
    return disfonias

@router.put("/{disfonias_id}", response_model=Disfonias)
async def update_disfonias(disfonias_id: str, disfonias: Disfonias):
    result = await db["disfonias"].update_one(
        {"_id": ObjectId(disfonias_id)}, {"$set": disfonias.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Disfonia no encontrado")
    disfonias.id = disfonias_id
    return disfonias

@router.delete("/{disfonias_id}")
async def delete_disfonias(disfonias_id: str):
    result = await db["disfonias"].delete_one({"_id": ObjectId(disfonias_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Disfonia no encontrado")
    return {"message": "Disfonia eliminado"}
